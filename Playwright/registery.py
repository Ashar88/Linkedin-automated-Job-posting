# Python code to add current script to the registry

# module to edit the windows registry
import winreg as reg
import os			

def AddToRegistry():


	pth = os.path.dirname(os.path.realpath(__file__))
	
	# name of the python file with extension
	s_name="run.py"	
	
	# joins the file name to end of path address
	address=os.path.join(pth,s_name)
	address = r'C:\Users\Syscom\anaconda3\python.exe "D:\WORK\All_Python_Work\Python Work\PANDAS folder\Qureos\Playwright\run.py"'
	print(address)

	# key we want to change is HKEY_CURRENT_USER
	# # key value is Software\Microsoft\Windows\CurrentVersion\Run
	key = reg.HKEY_CURRENT_USER
	key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
	
	# # open the key to make changes to
	open = reg.OpenKey(key,key_value,0,reg.KEY_ALL_ACCESS)
	
	# # modify the opened key
	reg.SetValueEx(open,"any_name",0,reg.REG_SZ,address)
	
	# # now close the opened key
	reg.CloseKey(open)

# Driver Code
if __name__=="__main__":
	AddToRegistry()
