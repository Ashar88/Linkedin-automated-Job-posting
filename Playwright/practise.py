from playwright.sync_api import sync_playwright
import time

def open_edge_with_profile(profile_directory):
    with sync_playwright() as playwright:
        browser_type = playwright.chromium
        browser = browser_type.launch_persistent_context(channel="msedge", user_data_dir=profile_directory, headless=False)
        page = browser.new_page()

        page.goto('https://www.linkedin.com/my-items/posted-jobs/')
        page.wait_for_selector("ul.reusable-search__entity-result-list li")
    

        jobsCount = page.locator("//a[contains(@href,'www.linkedin.com/hiring/jobs')]").count()
        print(f"the length is len: {jobsCount}")

        for i in range(1,jobsCount+1):

            page.locator(f"(//a[contains(@href,'www.linkedin.com/hiring/jobs')])[{i}]").click()
            # time.sleep(10)


            break
            page.go_back()
            time.sleep(10)
            print("go back")
        

        while True:
           command = input("Enter a command (type 'exit' to quit): ")
           if command.lower() == "exit":
                break

        browser.close()

profile_path = 'C:/Users/Syscom/AppData/Local/Microsoft/Edge/User Data'
open_edge_with_profile(profile_path)
