from playwright.sync_api import sync_playwright
import time
from constant import WEBSITE
import pandas as pd
from fuzzywuzzy import process
from nameparser import HumanName
import numpy as np


class linkedinJob():

    def __init__(self) -> None:
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKCYAN = '\033[96m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.WHITE = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'


    def opening_jobs(self, PATH_EDGE):
        with sync_playwright() as playwright:
            browser_type = playwright.chromium
            browser = browser_type.launch_persistent_context(channel="msedge", viewport={"width": 1366, "height": 625}, user_data_dir= PATH_EDGE, headless=False)
            page = browser.new_page()
            
            # Delete the navigator.webdriver property using page.add_init_script
            page.add_init_script("delete Object.getPrototypeOf(navigator).webdriver")

            self.page = page

            print("Website Searched!!")
            # WEBSITE = "https://bot.sannysoft.com/" # for checking bots
            page.goto(WEBSITE, wait_until="domcontentloaded", timeout=100000)

            page.wait_for_selector("//a[contains(@href,'www.linkedin.com/hiring/jobs')][@class = 'app-aware-link ']", timeout=50000)
            jobsCount = page.locator("//a[contains(@href,'www.linkedin.com/hiring/jobs')][@class = 'app-aware-link ']").count()
            print(f"the job count length is len: {jobsCount}")
        
           # Looping through All Jobs
            i = 1
            while i <= jobsCount:

                self.Removing_Message_Box_DiscardBtn()
                self.Removing_Message_Box_DiscardBtn()
                self.Removing_Message_Box_DiscardBtn()

                print(f"\n\n  RIGHT NOW on the job({i}) - {jobsCount}")

                Job = page.locator(f"(//a[contains(@href,'www.linkedin.com/hiring/jobs')][@class = 'app-aware-link '])[{i}]")
                Job.wait_for(timeout=20000)
                Job.scroll_into_view_if_needed(timeout=20000)
                Job.click(timeout=10000)
                self.viewApplicants()

                #Coming back to this page Again to check another job
                page.goto(WEBSITE, wait_until="domcontentloaded", timeout=200000)
                i+=1; 

                page.wait_for_selector("//a[contains(@href,'www.linkedin.com/hiring/jobs')][@class = 'app-aware-link ']", timeout=500000)
                jobsCount = page.locator("//a[contains(@href,'www.linkedin.com/hiring/jobs')][@class = 'app-aware-link ']").count()

                print("\nOpening_Jobs page, go back")
                break



    def viewApplicants(self):
        
        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()

        ### ******************************* 1 ********************************
        # checking whether application is active/paused or not
        # countVar = 0
        # while True:
        #     active = self.page.get_by_text("Active", exact=True).is_visible(timeout=5000)
        #     if not active:
        #         active = self.page.get_by_text("Paused", exact=True).is_visible(timeout=5000)
        #     print(f"active/paused-{countVar}:{active}")
        #     if active: break
        #     if countVar >= 10: return
        #     countVar+=1
        #     time.sleep(1)
        

        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()
        
        #View All Applicants
        self.page.get_by_role("button", name="View applicants").click(timeout=200000)
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

        
        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()

        # Application Title
        ApplicationTitle = self.page.locator("//h1[contains(@class, 't-1')]")
        ApplicationTitle = ApplicationTitle.inner_text(timeout=5000)
        ApplicationTitle = ApplicationTitle.split('\n')[1]
        self.ApplicationTitle = ApplicationTitle
        print("The title is :", ApplicationTitle)

        #Application Job Link
        self.JobLink = self.getRequiredJobLink()
        print("The job link is :", self.JobLink)

        
        # Closing the Appeared popups
        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()

        # Total Pages Buttons
        try:
            self.page.wait_for_selector("//ul[contains(@class, 'artdeco-pagination__pages--number')]//button", state='visible') 
            allPagesButton = self.page.locator("//ul[contains(@class, 'artdeco-pagination__pages--number')]//button").count()
        except: 
            pass; allPagesButton = 1

        print(f"\nthe allPagesButton is len: {allPagesButton}")
        i = 1
        while i <= allPagesButton:
            try:
                time.sleep(0.5)
                # self.page.wait_for_selector("//ul[contains(@class, 'artdeco-pagination__pages--number')]//button", state='visible') 
                self.page.locator(f"(//ul[contains(@class, 'artdeco-pagination__pages--number')]//button)[{i}]").click(timeout=200)
            except: pass

            print(f"\nallpagesButton number: {i}")
            time.sleep(1)
            self.ApplicantsPerPages()

            # break
            i+=1;  allPagesButton = self.page.locator("//ul[contains(@class, 'artdeco-pagination__pages--number')]//button").count()


    def ApplicantsPerPages(self):
        
        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()
        
        #All Aplicants on the current page
        self.page.wait_for_selector("//div[@class='hiring-applicants__list-container']/ul/li/a", state='visible')
        self.page.locator("//div[@class='hiring-applicants__list-container']/ul/li/a").first.wait_for(timeout=30000) 
        ApplicantsCount = self.page.locator("//div[@class='hiring-applicants__list-container']/ul/li/a").count()
        
        print(f"\nthe ApplicantsPerPages is len: {ApplicantsCount}")

        self.Removing_Message_Box_DiscardBtn()

        i = 1
        while i <= ApplicantsCount:
            
            self.Removing_Message_Box_DiscardBtn()
            self.Removing_Message_Box_DiscardBtn()
            self.Removing_Message_Box_DiscardBtn()

            time.sleep(1.5)
            
            self.page.locator(f"(//div[@class='hiring-applicants__list-container']/ul/li/a)[{i}]").wait_for(timeout=30000)       
            self.page.locator(f"(//div[@class='hiring-applicants__list-container']/ul/li/a)[{i}]").click(timeout=10000)
            
            print(f"\n{self.OKBLUE}Applicant number -  : {i}, {ApplicantsCount}")
            print(self.WHITE,end=' ')
            
            self.eachApplicantProfile()
            
            time.sleep(0.7)  
            ApplicantsCount = self.page.locator("//div[@class='hiring-applicants__list-container']/ul/li/a").count()
           
            i+=1

   
    def eachApplicantProfile(self):
        

        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()

        # Application Header 
        appHeader = self.page.locator("(//div[contains(@class, 'hiring-applicant-header')])[1]")
        Message = None


        ### ******************************* 2 ********************************
        ## Message already send or not
        alreadyMessageSent = appHeader.get_by_text("Message sent").is_visible(timeout=2000)
        if alreadyMessageSent: return 

        # Applicant Name
        ApplicantName = appHeader.locator("//h1[contains(@class, 't-2')]")
        ApplicantName = ApplicantName.inner_text(timeout=5000)
        ApplicantName = ApplicantName.split('\n')[0]
        ApplicantName = ApplicantName.split("’")[0]
        
        
        #Selecting Appropriate Name for the Applicant
        applicant = ""
        try:
            fullName = " ".join([name.capitalize() for name in ApplicantName.split()])
            name = HumanName(fullName)
            first , middle, last = name['first'], name['middle'], name['last']
            
             # Not Allowed names
            notAlloweds = ["muhammad", "mohammad", "mohammed", "muhammed", "mohamed", "muhamed"]
           
            for notAllowed in notAlloweds:     
                if notAllowed in first.lower() : first = ""
                if notAllowed in middle.lower() : middle = ""
            
            
            listed = [first , middle, last]
            applicant = listed[ np.argmax([len(first), len(middle), len(last)-3]) ]
        except:
            applicant = ApplicantName
        
        
        self.ApplicantName = applicant
        print(f"The Applicant Name is : {self.ApplicantName}  ( {ApplicantName} )")


        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()


        # Message Button clicked
        MsgVisible = None
        for _ in range(30):
            MsgVisible = appHeader.get_by_role('button', name="Message", exact=True).is_visible()
        
        if MsgVisible:  
            Message = appHeader.get_by_role('button', name="Message", exact=True)
            print("Message button Visible")
        else:
            moreOptions = appHeader.get_by_role('button', name="More")
            moreOptions.click(timeout=100000)
            Message = self.page.get_by_role('button', name="Message", exact=True)
            print("More... button , Message")

        
        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()
        

        #Sending Message to Applicant
        Message.wait_for(timeout=20000)
        Message.click(timeout=10000)
        self.sendMessage()
        
        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()
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
            boxes = self.page.locator("//button[span[contains(., 'Close') and contains(., 'conversation')]]").count()

    def sendMessage(self):
        
        #Sending Message to Each applicant
        messaging = self.page.locator("//div[@aria-label='Messaging' and @role='dialog']").first

        msgBox = messaging.get_by_role("textbox")
        msgBox.click(timeout=200000)
      
        messageSentence = f"Hi {self.ApplicantName},\nthank you for your interest in the {self.ApplicationTitle}, the opening is with one of our partner companies.\n\nPlease submit your resume through this link: {self.JobLink} To increase your chances of being matched with job opportunities with our partner companies, Please complete your profile on Qureos.\nOnce you have submitted your application, please let me know so that I can confirm its receipt. \n𝗔 𝗤𝗨𝗜𝗖𝗞 𝗧𝗜𝗣: Boost your odds of success, {self.ApplicantName}: Must Complete your profile to 100% and stand out from the competition!"
        msgBox.fill(messageSentence)

        #Checking Valid link to send msg
        if self.JobLink == '[LINK]':
            print("No link in msgBox")
        else:
            messaging.get_by_role("button", name = 'Send', exact=True).click(timeout=200000)
            print("msg sent")



    def getRequiredJobLink(self):
        
        #Reading my Assigned Jobs for the week
        df = pd.read_csv("D:\WORK\All_Python_Work\Python Work\PANDAS folder\Qureos\Playwright\FILES\My_Jobs_Details.csv")
        job_titles = list(df['Job Title'])
        print(job_titles)
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
