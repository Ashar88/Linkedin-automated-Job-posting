from playwright.sync_api import sync_playwright
import time
import pandas as pd


class Applicants_Message():

    def MessageBoxClick(self, PATH_EDGE):
        self.WEBSITE = "https://www.linkedin.com/feed/"
        with sync_playwright() as playwright:
            browser_type = playwright.chromium
            browser = browser_type.launch_persistent_context(channel="msedge", viewport={"width": 1366, "height": 625}, user_data_dir= PATH_EDGE, headless=False)
            page = browser.new_page()
            self.page = page

            print("Website Searched!!")
            page.goto(self.WEBSITE, wait_until="domcontentloaded")

            page.wait_for_selector("//li-icon[@type='chevron-up' and @class = 'artdeco-button__icon']", timeout=20000)
            page.locator("//li-icon[@type='chevron-up' and @class = 'artdeco-button__icon']").click()
        
# You are on the messaging overlay. Press enter to open the list of conversations.

PATH_EDGE = 'C:/Users/Syscom/AppData/Local/Microsoft/Edge/User Data'
app = Applicants_Message()
app.MessageBoxClick(PATH_EDGE)



  
