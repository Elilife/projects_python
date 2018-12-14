"""
neuroConn visualizer
DC-STIMULATOR MOBILE
author:Eliana Garcia Cossio
"""

from tkinter import *
import matplotlib
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
import numpy as np
import PIL.Image
import PIL.ImageTk
import pickle
import pandas
from backend0 import back

matplotlib.use('TkAgg')
back_end=back("stimulation_data.db")
style.use("ggplot")

f=Figure(figsize=(8,5),dpi=100)
a=f.add_subplot(111)

class Window(object):

    def __init__(self,window):
        self.window=window
        self.window.wm_title("neuroConn Visualizer")

        frame1=Frame(window)
        frame1.pack(side=TOP, fill=X)

        l0=Label(frame1,text="                         ",fg='black',bg='white')
        l0.grid(row=0,column=1)

        l1=Label(frame1,text="SEARCHING TOOLS",fg='black',bg='white',font=('Helvetica', 14, 'bold'))
        l1.grid(row=0,column=2,sticky=W)

        l2=Label(frame1,text="Stimulation Date",fg='black',bg='white',font=('Helvetica', 14))
        l2.grid(row=1,column=2,sticky=W)

        l3=Label(frame1,text="Stimulation State",fg='black',bg='white',font=('Helvetica', 14))
        l3.grid(row=2,column=2,sticky=W)

        l4=Label(frame1,text="Stimulations",fg='black',bg='white',font=('Helvetica', 14))
        l4.grid(row=4,column=0,sticky=E)

        #l5=Label(frame1,text="                         ",fg='black',bg='white')


        im = PIL.Image.open("neuroconn.png")
        im= im.resize((230,90), PIL.Image.ANTIALIAS)
        photo = PIL.ImageTk.PhotoImage(im)

        l5 = Label(frame1, image=photo)
        l5.image = photo  # keep a reference!
        l5.grid(row=1,column=8,columnspan=4, rowspan=4,sticky=W+E+N+S,)

        l6 = Label(frame1, text="                         ",fg='black',bg='white')
        l6.grid(row=4,column=7)



        self.stim_date_time_text=StringVar()
        self.e1=Entry(frame1,textvariable=self.stim_date_time_text)
        self.e1.grid(row=1,column=3)

        self.stim_state_text=StringVar()
        self.e2=Entry(frame1,textvariable=self.stim_state_text)
        self.e2.grid(row=2,column=3)

        b0=Button(frame1,text="Load data",width=12,command=self.view_command)
        b0.grid(row=1,column=0)

        #b1=Button(frame1,text="View all",width=12,command=view_command)
        #b1.grid(row=0,column=6)

        b2=Button(frame1,text="Search entry",width=12)
        b2.grid(row=1,column=6)

        b6=Button(frame1,text="Close",width=12,command=window.destroy)
        b6.grid(row=3,column=6)

        ## Frame 2 for list and graph

        frame2=Frame(window)
        frame2.pack(side=TOP,fill=X)



        sb1=Scrollbar(frame2,orient="vertical")
        sb1.pack(side=LEFT,fill=BOTH, expand=False)
        sb2=Scrollbar(frame2,orient="horizontal")
        sb2.pack(side=LEFT,fill=BOTH, expand=False)
        self.list1=Listbox(frame2, selectmode=EXTENDED,height=6, width=35)
        self.list1.pack(side=LEFT,fill=BOTH, expand=False)



        self.list1.configure(yscrollcommand=sb1.set, xscrollcommand=sb2.set)
        sb1.configure(command=self.list1.yview)
        sb2.configure(command=self.list1.xview)


        #here we get the selection by clicking on top of the item
        self.list1.bind('<<ListboxSelect>>',self.get_selected_row2)


        #a.plot([0],[0])
        self.canvas=FigureCanvasTkAgg(f,frame2)
        self.ax = self.canvas.figure.axes[0]
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=RIGHT,fill=BOTH, expand=True)

        toolbar=NavigationToolbar2TkAgg(self.canvas,frame2)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP,fill=BOTH, expand=True)

#..............................................
        self.ax.set_xlabel('Time',{'fontname':'Helvetica', 'size':'12'})
        self.ax.set_ylabel('Intensity (mA)',{'fontname':'Helvetica', 'size':'12'})
        self.ax.tick_params('y', colors='tab:blue', labelsize=12)
        #self.ax.set_xlim(min(data.index)-10, max(data.index)+10)
        self.ax.set_title('Stimulation Parameters',{'fontname':'Helvetica', 'size':'12'})


        self.ax2 = self.ax.twinx()
        self.ax2.set_ylabel('Voltage (V)',{'fontname':'Helvetica', 'size':'12'})
        self.ax2.tick_params('y', colors='tab:orange', labelsize=12)

        self.ax3 = self.ax.twinx()
        self.ax3.spines['right'].set_position(('axes', 1.25))
        self.ax3.set_ylabel('Impedance (KOhm)',{'fontname':'Helvetica', 'size':'12'})
        self.ax3.tick_params('y', colors='tab:olive', labelsize=12)

        f.tight_layout()

#..............................................



        b3=Button(frame1,text="Plot",width=12,command=self.plot_command2)
        b3.grid(row=2,column=6)

## MY FUNCTIONS
    def open_command(self):
        self.list1.delete(0,END)
        self.list1.insert(END,back_end.open1())

    def view_command(self):
        dir_list_info, dir_list_data=back_end.get_dir()
        back_end.fill_matrix(dir_list_info, dir_list_data)
        self.list1.delete(0,END)
        for row in back_end.view():
            self.list1.insert(END,row)

    def get_selected_row2(self,event):
        if len(self.list1.curselection())>1:
            self.e1.delete(0,END)
            self.e1.insert(END,'---')
            self.e2.delete(0,END)
            self.e2.insert(END,'---')

        else:
            index=self.list1.curselection()[0]
            rows=back_end.selection2(index)
            self.e1.delete(0,END)
            self.e1.insert(END,rows[0][0])
            self.e2.delete(0,END)
            self.e2.insert(END,rows[0][1])

    def plot_command2(self):
        try:
            if len(self.list1.curselection())>1:
                print('more than one')
                index=self.list1.curselection()[0:]
                data=back_end.selection4(index)
                #CREATE A MATRIX WITH ALL INFO FOR CURRENT AND FILL UNEQUAL VALUES WITH NANS
                #finding longest vector
                max_val_0=0
                d=np.zeros((1, len(data)))
                for i in range(len(data)):
                    temp=pickle.loads(data[i][0])
                    temp2=temp.shape
                    d[0,i]=temp2[0]
                print(str(np.amax(d)))
                data_full=np.empty((int(np.amax(d)), len(data),3))
                data_full[:] = np.nan

                for i in range(len(data)):
                    for j in [0, 1, 2]:
                        data_full[0:int(d[0,i]),i,j]=pickle.loads(data[i][j])
                #mean across measurements
                data_avg=np.nanmean(data_full, axis=1)
                data_error=np.nanstd(data_full, axis=1)

                #x = np.arange(9, dtype=float).reshape(3, 3)
                #x[:,1] = np.nan
                #print(str(d.shape))
                    #if max_val>max_val_0:
                        #max_val_0=max_val
                #print(str(max_val_0))
                time=range(int(np.amax(d)))
                a.clear()
                self.ax.clear()
                self.ax2.clear()
                self.ax3.clear()
                self.ax.plot(time,data_avg[:,0],'tab:blue',label='current')
                self.ax.fill_between(time, data_avg[:,0]-data_error[:,0], data_avg[:,0]+data_error[:,0], alpha=0.2, edgecolor='#1B2ACC', facecolor='#089FFF')
                self.ax.set_xlabel('Time (s)',{'fontname':'Helvetica', 'size':'12'})
                self.ax.set_ylabel('Intensity (mA)',{'fontname':'Helvetica', 'size':'12'})
                self.ax.set_xlim(min(time)-1, max(time)+1)
                self.ax.set_title('Stimulation Parameters',{'fontname':'Helvetica', 'size':'12'})

                #ax2 = self.ax.twinx()
                self.ax2.plot(time,data_avg[:,1],'tab:orange',label='voltage')
                self.ax2.fill_between(time, data_avg[:,1]-data_error[:,1], data_avg[:,1]+data_error[:,1], alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')
                self.ax2.set_ylabel('Voltage (V)',{'fontname':'Helvetica', 'size':'12'})
                self.ax2.grid(False)

                #ax3 = self.ax.twinx()
                self.ax3.spines['right'].set_position(('axes', 1.25))
                self.ax3.plot(time,data_avg[:,2],'tab:olive',label='impedance')
                self.ax2.fill_between(time, data_avg[:,2]-data_error[:,2], data_avg[:,2]+data_error[:,2], alpha=0.5, edgecolor='tab:olive', facecolor='tab:olive')
                self.ax3.set_ylabel('Impedance (KOhm)',{'fontname':'Helvetica', 'size':'12'})
                self.ax3.grid(False)

                f.tight_layout()

                self.canvas.draw()

            else:
                index=self.list1.curselection()[0]
                data=back_end.selection3(index)
                #with this code we retrieve the information coded
                current=pickle.loads(data[0][0])

                a.clear()
                self.ax.clear()
                self.ax2.clear()
                self.ax3.clear()
                self.ax.plot(current.index.values,pickle.loads(data[0][0]),'tab:blue',label='current')
                self.ax.set_xlabel('Time (s)',{'fontname':'Helvetica', 'size':'12'})
                self.ax.set_ylabel('Intensity (mA)',{'fontname':'Helvetica', 'size':'12'})
                self.ax.set_xlim(min(current.index.values)-1, max(current.index.values)+1)
                self.ax.set_title('Stimulation Parameters',{'fontname':'Helvetica', 'size':'12'})

                #ax2 = self.ax.twinx()
                self.ax2.plot(current.index.values,pickle.loads(data[0][1]),'tab:orange',label='voltage')
                self.ax2.set_ylabel('Voltage (V)',{'fontname':'Helvetica', 'size':'12'})
                self.ax2.grid(False)

                #ax3 = self.ax.twinx()
                self.ax3.spines['right'].set_position(('axes', 1.25))
                self.ax3.plot(current.index.values,pickle.loads(data[0][2]),'tab:olive',label='impedance')
                self.ax3.set_ylabel('Impedance (KOhm)',{'fontname':'Helvetica', 'size':'12'})
                self.ax3.grid(False)

                f.tight_layout()

                self.canvas.draw()

        except IndexError:
            pass



window=Tk()
Window(window)
window.mainloop()
