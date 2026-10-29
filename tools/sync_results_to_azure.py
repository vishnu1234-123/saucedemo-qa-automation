#!/usr/bin/env python3
"""Send pytest results (JUnit XML) to Azure DevOps Test Plans.

Each Azure test case has a title starting with its ID (for example
"TC-LOGIN-01 Valid login ..."). case_map.json says which pytest tests belong to
which case. The script works out one outcome per case and, unless --dry-run is
given, records it in a new test run on the plan.

Outcome rules for one case (all its matching tests, all browsers):
  any failure or error                 -> Failed (a real regression)
  any expected failure (xfail)         -> Failed, comment names the known bug
  at least one pass, nothing else bad  -> Passed
  only skips                           -> not reported
  no matching tests (manual checks)    -> left untouched

Usage:
  python tools/sync_results_to_azure.py --junit "test-results/*.xml" --dry-run
  ADO_PAT=... python tools/sync_results_to_azure.py --junit "test-results/*.xml" \
      --org https://dev.azure.com/YOUR_ORG --project A11y-QA-Capstone --plan 123 --only TC-LOGIN-01
"""
import argparse
import base64
import fnmatch
import glob
import json
import os
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

API = "api-version=7.1"


BROWSERS = ("chromium", "firefox", "webkit")


def normalize(name):
    """Drop the browser from the parameter list, wherever it sits.
    test_x[chromium-case] -> test_x[case];  test_x[case-chromium] -> test_x[case];
    test_x[chromium] -> test_x"""
    m = re.match(r"^(.*?)\[(.*)\]$", name)
    if not m:
        return name
    base, params = m.groups()
    kept = [p for p in params.split("-") if p not in BROWSERS]
    return "%s[%s]" % (base, "-".join(kept)) if kept else base


def read_junit(patterns):
    files = sorted({f for p in patterns for f in glob.glob(p)})
    if not files:
        sys.exit("No JUnit files found for: %s" % patterns)
    results = []
    for path in files:
        for tc in ET.parse(path).getroot().iter("testcase"):
            module = tc.get("classname", "").split(".")[-1]
            status, message = "passed", ""
            for child in tc:
                if child.tag in ("failure", "error"):
                    status, message = "failed", child.get("message", "")
                elif child.tag == "skipped":
                    is_xfail = child.get("type") == "pytest.xfail" or "xfail" in (child.get("type") or "")
                    status, message = ("xfail" if is_xfail else "skipped"), child.get("message", "")
            results.append({"key": "%s::%s" % (module, normalize(tc.get("name", ""))),
                            "status": status, "message": message, "file": os.path.basename(path)})
    return files, results


def matches(pattern, key):
    if "*" in pattern:
        return fnmatch.fnmatchcase(key, pattern)
    if "[" in pattern:
        return key == pattern
    return key == pattern or key.startswith(pattern + "[")


def case_outcomes(case_map, results):
    out = {}
    for case, patterns in case_map.items():
        tests = [r for r in results if any(matches(p, r["key"]) for p in patterns)]
        if not tests:
            out[case] = {"outcome": None, "comment": "no matching automated tests", "tests": 0}
            continue
        c = {s: sum(1 for t in tests if t["status"] == s) for s in ("passed", "failed", "xfail", "skipped")}
        bugs = sorted({b for t in tests if t["status"] == "xfail" for b in re.findall(r"ADO-(\d+)", t["message"])}, key=int)
        summary = "%d passed, %d expected failures, %d failed, %d skipped across %d test runs" % (
            c["passed"], c["xfail"], c["failed"], c["skipped"], len(tests))
        if c["failed"]:
            first = next(t for t in tests if t["status"] == "failed")
            out[case] = {"outcome": "Failed", "comment": "REGRESSION: " + summary + ". " + first["message"][:300], "tests": len(tests)}
        elif c["xfail"]:
            bug_txt = " Known defect: bug %s." % ", ".join(bugs) if bugs else " Known defect."
            out[case] = {"outcome": "Failed", "comment": summary + "." + bug_txt, "tests": len(tests)}
        elif c["passed"]:
            out[case] = {"outcome": "Passed", "comment": summary, "tests": len(tests)}
        else:
            out[case] = {"outcome": None, "comment": "only skipped: " + summary, "tests": len(tests)}
    return out


def call(method, url, pat, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Basic " + base64.b64encode((":" + pat).encode()).decode())
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        sys.exit("HTTP %s for %s %s\n%s" % (e.code, method, url, e.read().decode()[:1500]))


def points_by_case(base, plan, pat):
    """Return {case code: [test point ids]} for every suite in the plan."""
    suites = call("GET", "%s/_apis/testplan/Plans/%s/suites?%s" % (base, plan, API), pat)["value"]
    found = {}
    for s in suites:
        pts = call("GET", "%s/_apis/testplan/Plans/%s/Suites/%s/TestPoint?%s" % (base, plan, s["id"], API), pat)["value"]
        for p in pts:
            name = (p.get("testCaseReference") or {}).get("name", "")
            m = re.match(r"(TC-[A-Z0-9]+-\d+[a-z]?)", name)
            if m:
                found.setdefault(m.group(1), []).append(str(p["id"]))
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--junit", nargs="+", required=True, help="JUnit XML file(s) or glob(s)")
    ap.add_argument("--map", default=os.path.join(os.path.dirname(__file__), "case_map.json"))
    ap.add_argument("--dry-run", action="store_true", help="print outcomes, send nothing")
    ap.add_argument("--org", default=os.environ.get("ADO_ORG_URL"), help="https://dev.azure.com/<org>")
    ap.add_argument("--project", default=os.environ.get("ADO_PROJECT", "A11y-QA-Capstone"))
    ap.add_argument("--plan", default=os.environ.get("ADO_PLAN_ID"), help="test plan id (number in the plan URL)")
    ap.add_argument("--only", nargs="*", help="only these case IDs, e.g. TC-LOGIN-01")
    ap.add_argument("--run-name", default="Automated results from pytest")
    args = ap.parse_args()

    case_map = json.load(open(args.map))
    files, results = read_junit(args.junit)
    outcomes = case_outcomes(case_map, results)
    if args.only:
        outcomes = {k: v for k, v in outcomes.items() if k in args.only}

    print("Read %d test results from %d file(s)\n" % (len(results), len(files)))
    for case, o in outcomes.items():
        print("%-14s %-8s %s" % (case, o["outcome"] or "-", o["comment"]))
    to_send = {k: v for k, v in outcomes.items() if v["outcome"]}
    counts = {x: sum(1 for v in to_send.values() if v["outcome"] == x) for x in ("Passed", "Failed")}
    print("\nWould report: %d Passed, %d Failed; %d cases untouched" % (counts["Passed"], counts["Failed"], len(outcomes) - len(to_send)))
    mapped = {r["key"] for r in results for p in case_map.values() for pat in p if matches(pat, r["key"])}
    unmapped = sorted({r["key"] for r in results} - mapped)
    if unmapped:
        print("\npytest tests not mapped to any case (%d):" % len(unmapped))
        for k in unmapped[:40]:
            print("  ", k)
    if args.dry_run:
        return

    pat = os.environ.get("ADO_PAT")
    if not (pat and args.org and args.plan):
        sys.exit("Set ADO_PAT and pass --org and --plan (or use --dry-run).")
    base = "%s/%s" % (args.org.rstrip("/"), args.project)
    points = points_by_case(base, args.plan, pat)
    missing = [c for c in to_send if c not in points]
    if missing:
        print("\nNo test point in the plan for: %s (skipped)" % ", ".join(missing))
    point_to_case = {pid: c for c, ids in points.items() for pid in ids if c in to_send}
    if not point_to_case:
        sys.exit("Nothing to report.")

    run = call("POST", "%s/_apis/test/runs?%s" % (base, API), pat,
               {"name": args.run_name, "plan": {"id": str(args.plan)}, "pointIds": [int(p) for p in point_to_case]})
    run_id = run["id"]
    res = call("GET", "%s/_apis/test/Runs/%s/results?%s" % (base, run_id, API), pat)["value"]
    updates = []
    for r in res:
        case = point_to_case.get(str((r.get("testPoint") or {}).get("id")))
        if case:
            o = to_send[case]
            updates.append({"id": r["id"], "outcome": o["outcome"], "state": "Completed", "comment": o["comment"]})
    call("PATCH", "%s/_apis/test/Runs/%s/results?%s" % (base, run_id, API), pat, updates)
    call("PATCH", "%s/_apis/test/runs/%s?%s" % (base, run_id, API), pat, {"state": "Completed"})
    print("\nRecorded %d results in run %s" % (len(updates), run_id))


if __name__ == "__main__":
    main()