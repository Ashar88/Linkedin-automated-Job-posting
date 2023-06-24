from playwright.sync_api import sync_playwright
import time
from constant import PATH_EDGE, WEBSITE


class linkedinJob():

    def opening_jobs(self):
        with sync_playwright() as playwright:
            browser_type = playwright.chromium
            browser = browser_type.launch_persistent_context(channel="msedge", user_data_dir= PATH_EDGE, headless=False)
            page = browser.new_page()
            self.page = page

            print("Website Searched!!")
            page.goto(WEBSITE, wait_until="domcontentloaded")

            page.wait_for_selector("//a[contains(@href,'www.linkedin.com/hiring/jobs')][@class = 'app-aware-link ']", timeout=20000)
            jobsCount = page.locator("//a[contains(@href,'www.linkedin.com/hiring/jobs')][@class = 'app-aware-link ']").count()
            print(f"the job count length is len: {jobsCount}")
           
           # Looping through All Jobs
            i = 1
            while i <= jobsCount:
                print(f"\n\n RIGHT NOW on the job({i}) - {jobsCount}")
                page.locator(f"(//a[contains(@href,'www.linkedin.com/hiring/jobs')][@class = 'app-aware-link '])[{i}]").click()
                self.viewApplicants()

                # break
                
                #Coming back to this page Again to check another job
                page.goto(WEBSITE)
                i+=1; jobsCount = page.locator("//a[contains(@href,'www.linkedin.com/hiring/jobs')][@class = 'app-aware-link ']").count()
                print("\nOpening_Jobs page, go back")



    def viewApplicants(self):
        
        #checking whether application is active or not
        countVar = 0
        while True:
            active = self.page.get_by_text("Active", exact=True).is_visible(timeout=5000)
            print(f"active-{countVar}:{active}")
            if active: break
            if countVar >= 5: return
            countVar+=1
            time.sleep(1)
        

        #View All Applicants
        self.page.get_by_role("button", name="View applicants").click()
        self.page.get_by_role("button", name="Ratings").click(timeout=20000)
        self.page.get_by_text("Not a fit").click(timeout=5000)
        self.page.get_by_text("Show results").click(timeout=10000)


        # Application Title
        ApplicationTitle = self.page.locator("//h1[contains(@class, 't-1')]")
        ApplicationTitle = ApplicationTitle.inner_text(timeout=5000)
        ApplicationTitle = ApplicationTitle.split('\n')[1]
        self.ApplicationTitle = ApplicationTitle
        print("The title is :", ApplicationTitle)

        # Total Pages Buttons
        self.page.wait_for_selector("//ul[contains(@class, 'artdeco-pagination__pages--number')]//button", state='visible') 
        allPagesButton = self.page.locator("//ul[contains(@class, 'artdeco-pagination__pages--number')]//button").count()
        
        print(f"the allPagesButton is len: {allPagesButton}")
        
        i = 1
        while i <= allPagesButton:
            self.page.wait_for_selector("//ul[contains(@class, 'artdeco-pagination__pages--number')]//button", state='visible') 
            self.page.locator(f"(//ul[contains(@class, 'artdeco-pagination__pages--number')]//button)[{i}]").click(timeout=10000)
            print(f"allpagesButton number: {i}")
            self.ApplicantsPerPages()

            # break
            i+=1;  allPagesButton = self.page.locator("//ul[contains(@class, 'artdeco-pagination__pages--number')]//button").count()


    def ApplicantsPerPages(self):
        
        #All Aplicants on the current page
        self.page.wait_for_selector("//div[@class='hiring-applicants__list-container']/ul/li/a", state='visible') 
        ApplicantsCount = self.page.locator("//div[@class='hiring-applicants__list-container']/ul/li/a").count()
        
        print(f"the ApplicantsPerPages is len: {ApplicantsCount}")

        i = 1
        while i <= ApplicantsCount:
            self.page.wait_for_selector(f"(//div[@class='hiring-applicants__list-container']/ul/li/a)[{i}]", state='visible') 
            self.page.locator(f"(//div[@class='hiring-applicants__list-container']/ul/li/a)[{i}]").click(timeout=10000)
            
            self.eachApplicantProfile()

            time.sleep(0.04)         
            ApplicantsCount = self.page.locator("//div[@class='hiring-applicants__list-container']/ul/li/a").count()
           
            print(f"Applicant number -  : {i}, {ApplicantsCount}")
            i+=1

   
    def eachApplicantProfile(self):
        
        # Application Header 
        appHeader = self.page.locator("(//div[contains(@class, 'hiring-applicant-header')])[1]")
        Message = None

        # Message already send or not
        alreadyMessageSent = appHeader.get_by_text("Message sent").is_visible(timeout=2000)
        if alreadyMessageSent: return 


        # Applicant Name
        ApplicantName = appHeader.locator("//h1[contains(@class, 't-2')]")
        ApplicantName = ApplicantName.inner_text(timeout=5000)
        ApplicantName = ApplicantName.split('\n')[0]
        ApplicantName = ApplicantName.split("’")[0]
        self.ApplicantName = ApplicantName
        print("The Applicant Name is :", ApplicantName)


        # Message Button clicked
        MsgVisible = appHeader.get_by_role('button', name="Message", exact=True).is_visible()
        if MsgVisible:  
            Message = appHeader.get_by_role('button', name="Message", exact=True)
            print("Message button Visible")
        else:
            moreOptions = appHeader.get_by_role('button', name="More")
            moreOptions.click()
            Message = self.page.get_by_role('button', name="Message", exact=True)
            print("More... button , Message")
        Message.click()

        #Sending Message to Applicant
        self.sendMessage()


        #Closing the Message box and discard button if any
        self.page.locator("//button[span[contains(., 'Close') and contains(., 'conversation')]]").click()
        discardPopup = self.page.get_by_role("button", name = "Discard").is_visible(timeout=3000)
        if discardPopup:
            print("discard Popup")
            self.page.get_by_role("button", name = "Discard").click()
        


    def sendMessage(self):
        messaging = self.page.locator("//div[@aria-label='Messaging' and @role='dialog']")
        msgBox = messaging.get_by_role("textbox")
        msgBox.click()
        msgBox.click()
        
        msgBox.fill(f"Hi there {self.ApplicantName},\nthank you for your interest in the {self.ApplicationTitle} , the opening is with one of our partner companies.\n\nPlease submit your resume through this link: https://app.qureos.com/jobs/647d96908a8cbf001eb145c8?referrer=AS07B To increase your chances of being matched with job opportunities with our partner companies, please complete your profile on Qureos.\n\nOnce you have submitted your application, please let me know so that I can confirm its receipt.")


        




