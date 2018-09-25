#Website blocker
#indicate the path for windows or mac
#in mac run : sudo python3 script.py
#in windowns: open a cmd and run as administrator, change the directory and run: python3
import time
from datetime import datetime as dt
#windows path
#host_path1=r"C:\Windows\System32\drivers\etc\hosts"#keep it raw \n in case we have that
#mac path
#host_path2="/etc/hosts"
host_temp='/Users/eli/Documents/Data_science/python3/3_webbrowser_blocker/hosts'
redirect='127.0.0.1'
website_list=['www.facebook.com','facebook.com']

while True:
    if dt(dt.now().year,dt.now().month,dt.now().day,8)<dt.now()<dt(dt.now().year,dt.now().month,dt.now().day,16):
        print('Working hours')
        with open(host_temp,'r+') as file:
            content=file.read()
            for website in website_list:
                if website in content:
                    pass
                else:
                    file.write(redirect+ ' ' + website +'\n')
    else:
        with open(host_temp,'r+') as file:
            content=file.readlines()
            file.seek(0)#to start from te beggining of the file
            for line in content:
                if not any(website in line for website in website_list):
                    file.write(line)
                file.truncate()#delete everything down
        print('Fun hours!!')
    time.sleep(5)#checking every 5 seconds
