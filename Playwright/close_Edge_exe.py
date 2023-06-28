import psutil

def close_msedge():
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == 'msedge.exe':
            try:
                proc = psutil.Process(process.info['pid'])
                proc.terminate()
                # print(f"Closed msedge.exe with PID {process.info['pid']}")
            except psutil.NoSuchProcess:
                pass

# Call the function to close all instances of msedge.exe
close_msedge()
