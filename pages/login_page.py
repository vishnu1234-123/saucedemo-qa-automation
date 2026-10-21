from playwright.sync_api import Page

class LoginPage:
    def __init__(self,page:Page):
        self.page=page
        self.username=page.locator('[data-test="username"]')
        self.password=page.locator('[data-test="password"]')
        self.login_button=page.locator('[data-test="login-button"]')
        self.error=page.locator('[data-test="error"]')
        self.error_close=page.locator('[data-test="error-button"]')
    
    def open(self):
        self.page.goto("https://www.saucedemo.com/")
        return self
    
    def login(self,username:str,password:str):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()

    def dismiss_error(self):
        self.error_close.click()
    def password_type(self)->str:
        return self.password.get_attribute("type")
    
