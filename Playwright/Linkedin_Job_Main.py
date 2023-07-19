from playwright.sync_api import sync_playwright
import time
from constant import WEBSITE
import pandas as pd
from fuzzywuzzy import process
from nameparser import HumanName
import numpy as np


class linkedinJob():

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

            page.wait_for_selector("//a[contains(@href,'www.linkedin.com/hiring/jobs')][@class = 'app-aware-link ']", timeout=20000)
            jobsCount = page.locator("//a[contains(@href,'www.linkedin.com/hiring/jobs')][@class = 'app-aware-link ']").count()
            print(f"the job count length is len: {jobsCount}")
        
           # Looping through All Jobs
            i = 1
            while i <= jobsCount:
                print(f"\n\n RIGHT NOW on the job({i}) - {jobsCount}")
                page.locator(f"(//a[contains(@href,'www.linkedin.com/hiring/jobs')][@class = 'app-aware-link '])[{i}]").click()
                self.viewApplicants()

                #Coming back to this page Again to check another job
                page.goto(WEBSITE)
                i+=1; jobsCount = page.locator("//a[contains(@href,'www.linkedin.com/hiring/jobs')][@class = 'app-aware-link ']").count()
                print("\nOpening_Jobs page, go back")
                break



    def viewApplicants(self):
        
        # checking whether application is active/paused or not
        countVar = 0
        while True:
            active = self.page.get_by_text("Active", exact=True).is_visible(timeout=5000)
            if not active:
                active = self.page.get_by_text("Paused", exact=True).is_visible(timeout=5000)
            print(f"active/paused-{countVar}:{active}")
            if active: break
            if countVar >= 10: return
            countVar+=1
            time.sleep(1)
        

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

        
        # Closing the Appeared popups
        self.Removing_Message_Box_DiscardBtn()

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
                time.sleep(0.5)
                # self.page.wait_for_selector("//ul[contains(@class, 'artdeco-pagination__pages--number')]//button", state='visible') 
                self.page.locator(f"(//ul[contains(@class, 'artdeco-pagination__pages--number')]//button)[{i}]").click()
            except: pass

            print(f"allpagesButton number: {i}")
            time.sleep(1)
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
            
            self.Removing_Message_Box_DiscardBtn()
            self.page.locator(f"(//div[@class='hiring-applicants__list-container']/ul/li/a)[{i}]").click(timeout=10000)
            
            self.eachApplicantProfile()

            time.sleep(0.7)         
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
        
        
        #Selecting Appropriate Name for the Applicant
        applicant = ""
        try:
            fullName = " ".join([name.capitalize() for name in ApplicantName.split()])
            name = HumanName(fullName)
            first , middle, last = name['first'], name['middle'], name['last']
            if "muhammad" in first.lower() or "mohammad" in first.lower(): first = ""  
            listed = [first , middle, last]
            applicant = listed[ np.argmax([len(first), len(middle), len(last)-2]) ]
        except:
            applicant = ApplicantName
        
        
        self.ApplicantName = applicant
        print(f"The Applicant Name is : {self.ApplicantName}  ( {ApplicantName} )")
  

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

        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()
        self.Removing_Message_Box_DiscardBtn()
        
        #Sending Message to Applicant
        Message.click()
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
        messaging = self.page.locator("//div[@aria-label='Messaging' and @role='dialog']").first

        # messageDate = messaging.locator("//time[contains(@class, 'msg-s-message-list__time-heading')]").last
        # messageDate.scroll_into_view_if_needed(timeout=5000)
        # dateDay = messageDate.inner_text()
        # print(dateDay)
        # self.getDayDifference(dateDay)
        # time.sleep(7)

        msgBox = messaging.get_by_role("textbox")
        msgBox.click()
      
        messageSentence = f"Hi {self.ApplicantName},\nthank you for your interest in the {self.ApplicationTitle}, the opening is with one of our partner companies.\n\nPlease submit your resume through this link: {self.JobLink} To increase your chances of being matched with job opportunities with our partner companies, Please complete your profile on Qureos.\nOnce you have submitted your application, please let me know so that I can confirm its receipt. \n𝗔 𝗤𝗨𝗜𝗖𝗞 𝗧𝗜𝗣: Boost your odds of success, {self.ApplicantName}: Must Complete your profile to 100% and stand out from the competition!"
        # messageSentence = messageSentence.encode('utf-8').decode('unicode-escape')
        # messageSentence = f"Dear {self.ApplicantName},\n\nWe hope this message finds you well. We would like to remind you about the importance of completing your profile on our platform to maximize your chances of being selected for the {self.ApplicationTitle} at one of our partner companies.\n\nAs mentioned earlier, we have provided a link for you to complete your profile in our platform. It is crucial that you take the time to fill out the remaining details, as it significantly increases your likelihood of being considered for this position. A complete profile not only showcases your skills and qualifications but also helps us match you with the best possible opportunity.\n\nIf you have already completed your profile and applied to the job, please disregard this message, as it indicates that you have successfully taken the necessary action.\n\nRegards,\nQureos Talent Outreach Associate Team\n"
        msgBox.fill(messageSentence)

        #Checking Valid link to send msg
        if self.JobLink == '[LINK]':
            print("No link in msgBox")
        else:

            messaging.get_by_role("button", name = 'Send', exact=True).click()
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

