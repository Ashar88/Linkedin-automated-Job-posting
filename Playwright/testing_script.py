from linkedin_job import linkedinJob
from closeEdge import close_msedge
import time


def main1():
    while True:
        close_msedge()
        try:
            app = linkedinJob()
            print("here")
            app.opening_jobs('C:/Users/Syscom/AppData/Local/Microsoft/Edge/User Data1')

        except Exception as e:
            print(e)
            pass

main1()