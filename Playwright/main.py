from linkedin_job import linkedinJob
import pandas as pd
import datetime
import time
from closeEdge import close_msedge

def main():

    while True:
        print("time.sleep(60*5)\n")
        time.sleep(60*5)
        print("time.sleep(60*5)\n")
        close_msedge()

        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = "D:\WORK\All_Python_Work\Python Work\PANDAS folder\Qureos\Playwright\start_time.txt"
        with open(file_path, "a") as file:
            file.write("Before----------"+ current_time + "\n")


        app = linkedinJob()
        app.opening_jobs()
    

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = "D:\WORK\All_Python_Work\Python Work\PANDAS folder\Qureos\Playwright\start_time.txt"
        with open(file_path, "a") as file:
            file.write("After----------"+ current_time + "   " + app.ApplicationTitle )
            file.write("\n\n")
            
        time.sleep(60*10)

main()