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
import PIL.Image
import PIL.ImageTk
from backend import back

matplotlib.use('TkAgg')
back_end=back()
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

        b0=Button(frame1,text="Load data",width=12,command=self.open_command)
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
        self.list1=Listbox(frame2,height=6, width=35)
        self.list1.pack(side=LEFT,fill=BOTH, expand=False)



        self.list1.configure(yscrollcommand=sb1.set, xscrollcommand=sb2.set)
        sb1.configure(command=self.list1.yview)
        sb2.configure(command=self.list1.xview)


        #here we get the selection by clicking on top of the item
        self.list1.bind('<<ListboxSelect>>',self.get_selected_row)


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
        self.ax2.set_ylabel('Impedance (KOhm)',{'fontname':'Helvetica', 'size':'12'})
        self.ax2.tick_params('y', colors='tab:orange', labelsize=12)

        self.ax3 = self.ax.twinx()
        self.ax3.spines['right'].set_position(('axes', 1.25))
        self.ax3.set_ylabel('Voltage (V)',{'fontname':'Helvetica', 'size':'12'})
        self.ax3.tick_params('y', colors='tab:olive', labelsize=12)

        f.tight_layout()

#..............................................



        b3=Button(frame1,text="Plot",width=12,command=self.plot_command)
        b3.grid(row=2,column=6)

## MY FUNCTIONS
    def open_command(self):
        self.list1.delete(0,END)
        self.list1.insert(END,back_end.open1())

    def get_selected_row(self,event):
        try:
            #global selected_tuple
            index=self.list1.curselection()[0]
            self.selected_tuple=self.list1.get(index)
            data=back_end.selection(self.selected_tuple,1)
            #print(data.ix[1,0][0:data.ix[1,0].find('=')])
            print(data.ix[1,0][data.ix[1,0].find('=')+1:])
            #print(data.ix[1,0](data.ix[1,0].find('=')+1,))
            self.e1.delete(0,END)
            self.e1.insert(END,data.ix[1,0][data.ix[1,0].find('=')+1:])
            self.e2.delete(0,END)
            self.e2.insert(END,data.ix[4,0][data.ix[4,0].find('=')+1:])

        except IndexError:
            pass
    def plot_command(self):
        try:
            #index=list1.curselection()[0]
            #print(self.index)
            #selected_tuple=list1.get(index)
            data=back_end.selection(self.selected_tuple,2)
            #plotting the data
            #a.plot(data.index,data.ix[0:,0],'-b',label='current')
            #a.plot(data.index,data.ix[0:,1],'--g',label='impedance')
            a.clear()
            self.ax.clear()
            self.ax2.clear()
            self.ax3.clear()
            self.ax.plot(data.index,data.ix[0:,0],'tab:blue',label='current')
            self.ax.set_xlabel('Time (s)',{'fontname':'Helvetica', 'size':'12'})
            self.ax.set_ylabel('Intensity (mA)',{'fontname':'Helvetica', 'size':'12'})
            self.ax.set_xlim(min(data.index)-10, max(data.index)+10)
            self.ax.set_title('Stimulation Parameters',{'fontname':'Helvetica', 'size':'12'})

            #ax2 = self.ax.twinx()
            self.ax2.plot(data.index,data.ix[0:,1],'tab:orange',label='impedance')
            self.ax2.set_ylabel('Impedance (KOhm)',{'fontname':'Helvetica', 'size':'12'})
            self.ax2.grid(False)

            #ax3 = self.ax.twinx()
            self.ax3.spines['right'].set_position(('axes', 1.25))
            self.ax3.plot(data.index,data.ix[0:,2],'tab:olive',label='voltage')
            self.ax3.set_ylabel('Voltage (V)',{'fontname':'Helvetica', 'size':'12'})
            self.ax3.grid(False)

            f.tight_layout()

            self.canvas.draw()

        except IndexError:
            pass



window=Tk()
Window(window)
window.mainloop()
