import pandas
import more_itertools as mit
from tkinter import *
from tkinter.filedialog import askopenfilename
class back:

    def __init__(self):
        print('initialized...')

    def open1(self):
        filename = [askopenfilename()]
        return filename

    def selection(self,curselection,var):
        posit=list(mit.locate(''.join(curselection), lambda x: x == "/"))
        print(var)
        dir=''.join(curselection)[0:posit[-1]]
        if var==1:
            host_temp=dir+'/info.txt'
        elif var==2:
            host_temp=dir+'/data.txt'
        info=pandas.read_csv(host_temp,delimiter="\t",header=None)
        return info
