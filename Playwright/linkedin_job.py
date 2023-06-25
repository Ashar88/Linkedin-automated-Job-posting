from playwright.sync_api import sync_playwright
import time
from constant import WEBSITE
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


class linkedinJob():

    def opening_jobs(self, PATH_EDGE):
        with sync_playwright() as playwright:
            browser_type = playwright.chromium
            browser = browser_type.launch_persistent_context(channel="msedge", viewport={"width": 1366, "height": 625}, user_data_dir= PATH_EDGE, headless=False)
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
        # countVar = 0
        # while True:
        #     active = self.page.get_by_text("Active", exact=True).is_visible(timeout=5000)
        #     print(f"active-{countVar}:{active}")
        #     if active: break
        #     if countVar >= 5: return
        #     countVar+=1
        #     time.sleep(1)
        

        #View All Applicants
        self.page.get_by_role("button", name="View applicants").click()
        i = 1
        while i<7:
            try:
                self.page.get_by_role("button", name="Ratings").click(timeout=20000)
                self.page.get_by_text("Not a fit").click(timeout=20000)
                self.page.get_by_text("Show results").click(timeout=10000)
                break
            except:
                i+= 1
                pass


        # Application Title
        ApplicationTitle = self.page.locator("//h1[contains(@class, 't-1')]")
        ApplicationTitle = ApplicationTitle.inner_text(timeout=5000)
        ApplicationTitle = ApplicationTitle.split('\n')[1]
        self.ApplicationTitle = ApplicationTitle
        print("The title is :", ApplicationTitle)

        #Application Job Link
        self.JobLink = self.getRequiredJobLink()
        print("The job link is :", self.JobLink)


        # Total Pages Buttons
        try:
            self.page.wait_for_selector("//ul[contains(@class, 'artdeco-pagination__pages--number')]//button", state='visible') 
            allPagesButton = self.page.locator("//ul[contains(@class, 'artdeco-pagination__pages--number')]//button").count()
        except: 
            pass; allPagesButton = 1

        print(f"the allPagesButton is len: {allPagesButton}")
        i = 1
        while i <= allPagesButton:
            try:
                self.page.wait_for_selector("//ul[contains(@class, 'artdeco-pagination__pages--number')]//button", state='visible') 
                self.page.locator(f"(//ul[contains(@class, 'artdeco-pagination__pages--number')]//button)[{i}]").click()
            except: pass

            print(f"allpagesButton number: {i}")
            self.ApplicantsPerPages()

            # break
            i+=1;  allPagesButton = self.page.locator("//ul[contains(@class, 'artdeco-pagination__pages--number')]//button").count()


    def ApplicantsPerPages(self):
        
        #All Aplicants on the current page
        self.page.wait_for_selector("//div[@class='hiring-applicants__list-container']/ul/li/a", state='visible') 
        ApplicantsCount = self.page.locator("//div[@class='hiring-applicants__list-container']/ul/li/a").count()
        
        print(f"the ApplicantsPerPages is len: {ApplicantsCount}")

        self.Removing_Message_Box_DiscardBtn()

        i = 1
        while i <= ApplicantsCount:
            self.page.wait_for_selector(f"(//div[@class='hiring-applicants__list-container']/ul/li/a)[{i}]", state='visible') 
            self.page.locator(f"(//div[@class='hiring-applicants__list-container']/ul/li/a)[{i}]").click(timeout=10000)
            
            self.eachApplicantProfile()

            time.sleep(1)         
            ApplicantsCount = self.page.locator("//div[@class='hiring-applicants__list-container']/ul/li/a").count()
           
            print(f"Applicant number -  : {i}, {ApplicantsCount}")
            i+=1

   
    def eachApplicantProfile(self):
        
        # Application Header 
        appHeader = self.page.locator("(//div[contains(@class, 'hiring-applicant-header')])[1]")
        Message = None


        ## Message already send or not
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
        self.Removing_Message_Box_DiscardBtn()


    def Removing_Message_Box_DiscardBtn(self):
        
        #Closing the Message box and discard button if any
        boxes = self.page.locator("//button[span[contains(., 'Close') and contains(., 'conversation')]]").count()
       
        while boxes >= 1:
            self.page.locator(f"(//button[span[contains(., 'Close') and contains(., 'conversation')]])[{boxes}]").click()
            discardPopup = self.page.get_by_role("button", name = "Discard").count()
            if discardPopup >= 1:
                print("discard Popup")
                self.page.get_by_role("button", name = "Discard").click()
            boxes -= 1


    def sendMessage(self):
        
        #Sending Message to Each applicant
        messaging = self.page.locator("//div[@aria-label='Messaging' and @role='dialog']")
        msgBox = messaging.get_by_role("textbox")
        msgBox.click()
        messageSentence = f"Hi {self.ApplicantName},\nthank you for your interest in the {self.ApplicationTitle}, the opening is with one of our partner companies.\n\nPlease submit your resume through this link: {self.JobLink} To increase your chances of being matched with job opportunities with our partner companies, Please complete your profile on Qureos.\nOnce you have submitted your application, please let me know so that I can confirm its receipt. \n𝗔 𝗤𝗨𝗜𝗖𝗞 𝗧𝗜𝗣: Boost your odds of success, {self.ApplicantName}: Must Complete your profile to 100% and stand out from the competition!"
        # messageSentence = messageSentence.encode('utf-8').decode('unicode-escape')
        msgBox.fill(messageSentence)

        #Checking Valid link to send msg
        if self.JobLink == '[LINK]':
            print("No link in msgBox")
        else:
            messaging.get_by_role("button", name = 'Send', exact=True).click()
            print("msg sent")
        


    def getRequiredJobLink(self):
        
        #Reading my Assigned Jobs for the week
        df = pd.read_csv("D:\WORK\All_Python_Work\Python Work\PANDAS folder\Qureos\Playwright\My_Jobs_Details.csv")
        job_titles = list(df['Job Title'])
        search_title = self.ApplicationTitle

        # Find the best matching name
        best_match = process.extractOne(search_title, job_titles)

        print(f"Search Name: {search_title}")
        print(f"Best Match: {best_match[0]}")
        print(f"Similarity Score: {best_match[1]}\n\n")

        if best_match[1] < 80:
            print(f" -> NO JOB Title Found with {search_title}")
            return "[LINK]"

        df = df[df['Job Title'] == best_match[0]]
        return list(df['col-Job Description'])[0]

