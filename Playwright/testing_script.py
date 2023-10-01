from Linkedin_Job_Main__FirstTime import linkedinJob
from Linkedin_Job_Main__Repeated import linkedinJob_Repeated
from close_Edge_exe import close_msedge
from Getting_Excel_Data import Excel_Data
import time


def testing_script():

    # Excel_Data()
    
    # while True:
    close_msedge()
    try:
        
        ### ******************************* 1 ********************************
        # app = linkedinJob()
        app = linkedinJob_Repeated()

        print("here")
        app.opening_jobs('C:/Users/Syscom/AppData/Local/Microsoft/Edge/User Data1')
    
    except Exception as e:
        # time.sleep(1500)
        print(e)

testing_script()