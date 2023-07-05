from Linkedin_Job_Main import linkedinJob
from close_Edge_exe import close_msedge
from Getting_Excel_Data import Excel_Data
import time


def testing_script():
    Excel_Data()
    
    # while True:
    close_msedge()
    try:
        app = linkedinJob()
        print("here")
        app.opening_jobs('C:/Users/Syscom/AppData/Local/Microsoft/Edge/User Data1')

    except Exception as e:
        # time.sleep(1500)
        print(e)

testing_script()