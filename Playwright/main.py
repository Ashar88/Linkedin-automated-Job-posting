from Linkedin_Job_Main__FirstTime import linkedinJob
import datetime
import time
from close_Edge_exe import close_msedge
from Getting_Excel_Data import Excel_Data

def main():
    switchProfile = True
    PATH_EDGE = 'C:/Users/Syscom/AppData/Local/Microsoft/Edge/User Data'
    Excel_Data()

    while True:
        print("time.sleep(60*5)\n")
        time.sleep(60*5)
        print("time.sleep(60*5)\n")
        close_msedge()
        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = "D:\WORK\All_Python_Work\Python Work\PANDAS folder\Qureos\Playwright\LOGS.txt"
        with open(file_path, "a") as file:
            file.write("Before----------"+ current_time +"    "+PATH_EDGE+"\n")

        try:
            app = linkedinJob()
            app.opening_jobs(PATH_EDGE = PATH_EDGE)
            
        except Exception as e:
            print(e)

        if switchProfile :
            PATH_EDGE = PATH_EDGE + "1"
            print(PATH_EDGE)
            switchProfile = False
        else:
            PATH_EDGE = PATH_EDGE[:-1]
            print(PATH_EDGE)
            switchProfile = True



        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = "D:\WORK\All_Python_Work\Python Work\PANDAS folder\Qureos\Playwright\LOGS.txt"
        with open(file_path, "a") as file:
            file.write("After----------"+ current_time )
            file.write("\n\n")
            
        time.sleep(60*3)

main()