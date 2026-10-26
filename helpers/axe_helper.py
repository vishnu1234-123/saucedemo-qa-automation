from axe_playwright_python.sync_playwright import Axe

WCAG_TAGS=["wcag2a","wcag2aa","wcag21a","wcag21aa"]

def scan(page)->list[dict]:
    results=Axe().run(page,options={"runOnly":{"type":"tag","values":WCAG_TAGS}})
    return results.response["violations"]

def summarize(violations:list[dict])->str:
    return "\n".join(
        f'{v['id']} [{v["impact"]}] x{len(v["nodes"])}: {v["help"]}' for v in violations
    )

def check_page(page,known:dict[str,str]):
    violations=scan(page)
    unexpected=[v for v in violations if v["id"] not in known]
    assert not unexpected, "New violations:\n"+summarize(unexpected)
