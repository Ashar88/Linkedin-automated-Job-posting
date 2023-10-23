from playwright.sync_api import sync_playwright
import time
from constant import WEBSITE
import pandas as pd
from fuzzywuzzy import process
from nameparser import HumanName
import numpy as np


class linkedinJob_Repeated():

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
                # self.page.locator(f"(//ul[contains(@class, 'artdeco-pagination__pages--number')]//button)[{i}]").scroll_into_view_if_needed(timeout=30000)
                self.page.locator(f"(//ul[contains(@class, 'artdeco-pagination__pages--number')]//button)[{i}]").click()
            except: pass

            print(f"\nallpagesButton number: {i}")
            time.sleep(1)
            self.ApplicantsPerPages()

            # break
            i+=1;  
            self.page.wait_for_selector("//ul[contains(@class, 'artdeco-pagination__pages--number')]//button", timeout=500000)
            allPagesButton = self.page.locator("//ul[contains(@class, 'artdeco-pagination__pages--number')]//button").count()


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
        # alreadyMessageSent = appHeader.get_by_text("Message sent").is_visible(timeout=2000)
        # if alreadyMessageSent: return 

        
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




    def sendMessage(self):
        
        #Sending Message to Each applicant
        messaging = self.page.locator("//div[@aria-label='Messaging' and @role='dialog']").first
        self.profileUrl = self.getProfileUrl(messaging)
        messaging = self.getMessagingBoxWithURL()
        messaging.get_by_role("button", name = "Expand your conversation with").click(timeout=200000)
        self.messaging = messaging

        self.closeMessageBoxExceptProfileURL()
        self.closeMessageBoxExceptProfileURL()
        self.closeMessageBoxExceptProfileURL()
        self.FullApplicantName = self.getFullApplicantNameFunction(messaging)
        self.closeMessageBoxExceptProfileURL()
        self.closeMessageBoxExceptProfileURL()
        self.closeMessageBoxExceptProfileURL()
        self.ApplicantName = self.getApplicantFirstName(self.FullApplicantName)
        self.closeMessageBoxExceptProfileURL()
        self.closeMessageBoxExceptProfileURL()
        self.closeMessageBoxExceptProfileURL()


        ### ******************************* 2.1 ********************************
        NotAllowedName = []
        if self.FullApplicantName in NotAllowedName:
            print(f"{self.FAIL}'{self.FullApplicantName}' NAME is not allowed!")
            print(self.WHITE,end='')
            return
        


        print(f"{self.BOLD}The Applicant Name is : {self.ApplicantName}  ( {self.FullApplicantName} )")
        print(self.WHITE,end=' ')

        self.closeMessageBoxExceptProfileURL()
        self.closeMessageBoxExceptProfileURL()
        self.closeMessageBoxExceptProfileURL()
        
        alreadyReplied = False

        self.closeMessageBoxExceptProfileURL()
        self.closeMessageBoxExceptProfileURL()
        self.closeMessageBoxExceptProfileURL()


        ### ******************************* 3(Check Below as well)  ********************************
        # if self.isApplicantAlreadyReplied(messaging):
        #     alreadyReplied = True
        #     print(f"{self.OKCYAN}Already Replied!!")
            
        #     try:
        #         file_path = r"D:\WORK\All_Python_Work\Python Work\PANDAS folder\Qureos\Applied_Applicant_List.txt"
        #         with open(file_path, "a") as file:
        #             file.write(f"{self.FullApplicantName} -->  {self.ApplicationTitle}  --> https://www.linkedin.com/in/{self.profileUrl}")
        #             file.write("\n")    

        #         time.sleep(1)
        #     except Exception as e:
        #         print(e)
        
        # else:
        #     alreadyReplied = False
        #     print(f"{self.WARNING}No Response yet")

        #     try:
        #         file_path = r"D:\WORK\All_Python_Work\Python Work\PANDAS folder\Qureos\Not_Applied_Applicant_List.txt"
        #         with open(file_path, "a") as file:
        #             file.write(f"{self.FullApplicantName} -->  {self.ApplicationTitle}  --> https://www.linkedin.com/in/{self.profileUrl}")
        #             file.write("\n")    
        #     except Exception as e:
        #         print(e)

        self.closeMessageBoxExceptProfileURL()
        self.closeMessageBoxExceptProfileURL()
        self.closeMessageBoxExceptProfileURL()

        print(self.WHITE,end=' ')
        msgBox = messaging.get_by_role("textbox")
        msgBox.click(timeout=200000)
      
        self.closeMessageBoxExceptProfileURL()
        self.closeMessageBoxExceptProfileURL()
        self.closeMessageBoxExceptProfileURL()
        

        
        ### ******************************* 3(Check Above as well) ********************************
        ### ******************************* 3(Don't Share link) ********************************
        messageSentence = f"Dear {self.ApplicantName},\n\nWe hope this message finds you well. We would like to remind you about the importance of completing your profile as well as applying on our platform to maximize your chances of being selected for the {self.ApplicationTitle} at one of our partner companies.\n\nAs mentioned earlier, we have provided a link for you to complete your profile in our platform. It is crucial that you take the time to fill out the remaining details, as it significantly increases your likelihood of being considered for this position. A complete profile not only showcases your skills and qualifications but also helps us match you with the best possible opportunity.\n\nIf you have already completed your profile and applied to the job, please ignore this message, as it indicates that you have successfully taken the necessary action.\n\nRegards,\nQureos Talent Outreach Associate Team\n"
        # messageSentence = f"Dear {self.ApplicantName}, I haven't received a message from your side. If you still want to continue, Kindly fill your Application using provided link.\nThank you!"
        # messageSentence = f"Dear {self.ApplicantName},\nHope you're doing well. I haven't received a message from your side. If you still want to continue, Kindly fill your Application using already provided link.\nThank you!"


        #Checking Valid link to send msg
        self.closeMessageBoxExceptProfileURL()
        self.closeMessageBoxExceptProfileURL()
        self.closeMessageBoxExceptProfileURL()

        # if self.JobLink == '[LINK]':
        #     print("No link in msgBox")
        # eif alreadyReplied:
        if alreadyReplied:
            print("Applicant Already Replied!")
        else:
            msgBox.fill(messageSentence)
            messaging.get_by_role("button", name = 'Send', exact=True).click(timeout=200000)
            print("msg sent")
        






    def isApplicantAlreadyReplied(self, messaging):

        self.closeMessageBoxExceptProfileURL()
        self.closeMessageBoxExceptProfileURL()
        self.closeMessageBoxExceptProfileURL()

        try:      
            for _ in range(5):
                self.closeMessageBoxExceptProfileURL()
                time.sleep(0.2)
                self.closeMessageBoxExceptProfileURL()

            for _ in range(10):
                self.closeMessageBoxExceptProfileURL()
                self.closeMessageBoxExceptProfileURL()
                self.closeMessageBoxExceptProfileURL()

                messageDate = messaging.locator("//time[contains(@class, 'msg-s-message-list__time-heading')]")
                self.closeMessageBoxExceptProfileURL()
                self.closeMessageBoxExceptProfileURL()
                messageDate.first.wait_for(timeout=500000)
                self.closeMessageBoxExceptProfileURL()
                self.closeMessageBoxExceptProfileURL()
                messageDate.first.scroll_into_view_if_needed(timeout=30000)

                self.closeMessageBoxExceptProfileURL()
                self.closeMessageBoxExceptProfileURL()
                self.closeMessageBoxExceptProfileURL()
                
                for _ in range(5):
                    self.closeMessageBoxExceptProfileURL()
                    time.sleep(0.002)
                    self.closeMessageBoxExceptProfileURL()

            self.closeMessageBoxExceptProfileURL()
            self.closeMessageBoxExceptProfileURL()
            profileUrl = self.getProfileUrl(messaging)
            self.closeMessageBoxExceptProfileURL()
            print(f"{self.OKGREEN}Profile Url: {profileUrl}")
            
            self.closeMessageBoxExceptProfileURL()
            self.closeMessageBoxExceptProfileURL()
            self.closeMessageBoxExceptProfileURL()
           
            profileUrlCount = 0
            for _ in range(20):
                self.closeMessageBoxExceptProfileURL()
                time.sleep(0.01)
                self.closeMessageBoxExceptProfileURL()


            self.closeMessageBoxExceptProfileURL()
            self.closeMessageBoxExceptProfileURL()
            self.closeMessageBoxExceptProfileURL()
            messaging.locator(f"//a[contains(@href, '{profileUrl}')]").first.wait_for(timeout=500000) 
            # messaging.locator(f"//a[contains(@href, '{profileUrl}')]").highlight()

            self.closeMessageBoxExceptProfileURL()
            self.closeMessageBoxExceptProfileURL()
            self.closeMessageBoxExceptProfileURL()

            for _ in range(10):
                self.closeMessageBoxExceptProfileURL()
                self.closeMessageBoxExceptProfileURL()
                self.closeMessageBoxExceptProfileURL()

                messaging.locator(f"//a[contains(@href, '{profileUrl}')]").first.wait_for(timeout=500000)
                self.closeMessageBoxExceptProfileURL() 
                self.closeMessageBoxExceptProfileURL() 
                self.closeMessageBoxExceptProfileURL() 
                messaging.locator(f"//a[contains(@href, '{profileUrl}')]").first.scroll_into_view_if_needed(timeout=30000)
                
                self.closeMessageBoxExceptProfileURL()
                self.closeMessageBoxExceptProfileURL()
                self.closeMessageBoxExceptProfileURL()

                profileUrlCount1 = messaging.locator(f"//a[contains(@href, '{profileUrl}')]").count()
                self.closeMessageBoxExceptProfileURL()
                profileUrlCount = max(profileUrlCount, profileUrlCount1)
                
                self.closeMessageBoxExceptProfileURL()
                self.closeMessageBoxExceptProfileURL()
                self.closeMessageBoxExceptProfileURL()
                messaging.locator(f"//a[contains(@href, '{profileUrl}')]").last.wait_for(timeout=500000) 
                self.closeMessageBoxExceptProfileURL()
                self.closeMessageBoxExceptProfileURL()
                self.closeMessageBoxExceptProfileURL()
                messaging.locator(f"//a[contains(@href, '{profileUrl}')]").last.scroll_into_view_if_needed(timeout=30000)
                self.closeMessageBoxExceptProfileURL()
                self.closeMessageBoxExceptProfileURL()
                self.closeMessageBoxExceptProfileURL()

                for _ in range(5):
                    self.closeMessageBoxExceptProfileURL()
                    time.sleep(0.01)
                    self.closeMessageBoxExceptProfileURL()



            self.closeMessageBoxExceptProfileURL()    
            self.closeMessageBoxExceptProfileURL()    
            self.closeMessageBoxExceptProfileURL()    
            print(f"Profile Url count: {profileUrlCount}")
            
            self.closeMessageBoxExceptProfileURL()
            self.closeMessageBoxExceptProfileURL()
            if profileUrlCount <= 3:
                return False
            else:
                return True
        except:
            self.closeMessageBoxExceptProfileURL()
            print("Exception Occured Here!")
            return True






    def getProfileUrl(self, messaging):
        profileUrlLocator = messaging.locator("//header//a")
        profileUrlLocator.wait_for(timeout=500000)
        profileUrl = profileUrlLocator.get_attribute('href')
        profileUrl = max(profileUrl.split('/'), key=len)
        return profileUrl

    def getFullApplicantNameFunction(self, messaging):
        profileUrlLocator = messaging.locator("//header//a")
        profileUrlLocator.wait_for(timeout=500000)
        return profileUrlLocator.inner_text(timeout=5000)

    def getMessagingBoxWithURL(self):
        messagingBox = self.page.locator(f"//a[contains(@href, '{self.profileUrl}')]/ancestor::div[@aria-label='Messaging' and @role='dialog']")
        messagingBox.wait_for(timeout=500000) 
        return messagingBox

    def getApplicantFirstName(self, ApplicantName):
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
        
        return applicant






    def Removing_Message_Box_DiscardBtn(self):
        try:
            boxes = self.page.locator("//button[span[contains(., 'Close') and contains(., 'conversation')]]").count()
        
            while boxes >= 1:
                self.page.locator(f"(//button[span[contains(., 'Close') and contains(., 'conversation')]])[{boxes}]").click()
                discardPopup = self.page.get_by_role("button", name = "Discard").count()
                if discardPopup >= 1:
                    print("discard Popup")
                    self.page.get_by_role("button", name = "Discard").click()
                boxes = self.page.locator("//button[span[contains(., 'Close') and contains(., 'conversation')]]").count()
        except:
            print("Exception in Removing_Message_Box_DiscardBtn!!")


    def closeMessageBoxExceptProfileURL(self):
        self.openingMessageBoxIfClosed()
        self.openingMessageBoxIfClosed()
        boxes = self.page.locator("//button[span[contains(., 'Close') and contains(., 'conversation')]]").count()
        self.openingMessageBoxIfClosed()
        self.openingMessageBoxIfClosed()

        while boxes >= 1:
            self.openingMessageBoxIfClosed()
            self.openingMessageBoxIfClosed()
            MessageBoxCloseBtn = self.page.locator(f"(//button[span[contains(., 'Close') and contains(., 'conversation')]])[{boxes}]")
            self.openingMessageBoxIfClosed()
            self.openingMessageBoxIfClosed()
            MessageBox = self.page.locator(f"(//button[span[contains(., 'Close') and contains(., 'conversation')]])[{boxes}]/ancestor::div[@aria-label='Messaging' and @role='dialog']")
            self.openingMessageBoxIfClosed()
            self.openingMessageBoxIfClosed()
            profileUrl = self.getProfileUrl(MessageBox)
            self.openingMessageBoxIfClosed()
            self.openingMessageBoxIfClosed()

            if profileUrl != self.profileUrl:
                self.openingMessageBoxIfClosed()
                self.openingMessageBoxIfClosed()
                MessageBoxCloseBtn.click()
                self.openingMessageBoxIfClosed()
                self.openingMessageBoxIfClosed()
                discardPopup = self.page.get_by_role("button", name = "Discard").count()
                self.openingMessageBoxIfClosed()
                self.openingMessageBoxIfClosed()
                if discardPopup >= 1:
                    print("discard Popup")
                    self.page.get_by_role("button", name = "Discard").click()
                self.openingMessageBoxIfClosed()
                self.openingMessageBoxIfClosed()
                boxes = self.page.locator("//button[span[contains(., 'Close') and contains(., 'conversation')]]").count()
            else:
                boxes -= 1

    def openingMessageBoxIfClosed(self):
        return
        # try:
        #     print("Inside")
        #     self.messaging.highlight()
        #     expandbtn = self.messaging.get_by_role("button", name = "Expand your conversation with")
        #     print("Inside2")
        #     expandbtn.is_visible()
        #     print("Inside3")
        #     expandbtn.highlight()
        #     time.sleep(1)
        #     print("self.messaging.get_by_role")
        # except Exception as e:
        #     print("----------------------Exception Inside")
        #     header = self.messaging.locator("//header")
        #     header.highlight()
        #     header.click(timeout=10000)
        #     print("hello world")





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

