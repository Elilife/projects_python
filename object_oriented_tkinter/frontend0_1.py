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

        # Select language 1= English, 2= Deutsch, 3=Español
        self.LANG=1

        l21 = Label(frame1, text="   ",fg='black',bg='white')
        l21.grid(row=1,column=4)

        self.l1=Label(frame1,text="SEARCHING TOOLS",fg='black',bg='white',font=('Helvetica', 14, 'bold'))
        self.l1.grid(row=0,column=5,sticky=W)

        self.l2=Label(frame1,text="Stimulation Date",fg='black',bg='white',font=('Helvetica', 14))
        self.l2.grid(row=1,column=5,sticky=W)

        self.l3=Label(frame1,text="Stimulation State",fg='black',bg='white',font=('Helvetica', 14))
        self.l3.grid(row=2,column=5,sticky=W)

        self.l4=Label(frame1,text="Stimulations",fg='black',bg='white',font=('Helvetica', 14))
        self.l4.grid(row=4,column=1,sticky=E)

        im = PIL.Image.open("neuroconn.png")
        im= im.resize((230,90), PIL.Image.ANTIALIAS)
        photo = PIL.ImageTk.PhotoImage(im)

        l5 = Label(frame1, image=photo)
        l5.image = photo  # keep a reference!
        l5.grid(row=1,column=10,columnspan=4, rowspan=4,sticky=W+E+N+S,)

        l6 = Label(frame1, text="                         ",fg='black',bg='white')
        l6.grid(row=4,column=9)

        self.stim_date_time_text=StringVar()
        self.e1=Entry(frame1,textvariable=self.stim_date_time_text)
        self.e1.grid(row=1,column=6)

        self.stim_state_text=StringVar()
        self.e2=Entry(frame1,textvariable=self.stim_state_text)
        self.e2.grid(row=2,column=6)


        l20 = Label(frame1, text="      ",fg='black',bg='white')
        l20.grid(row=1,column=0)

        self.l8=Label(frame1,text="Data",fg='black',bg='white',font=('Helvetica', 14, 'bold'))
        self.l8.grid(row=1,column=1,sticky=W)

        self.b0=Button(frame1,text="Load",width=14,command=self.view_command)
        self.b0.grid(row=1,column=2,columnspan=2, rowspan=1,sticky=W+E)

        # Dictionary with options
        choices = { 'English','Deutsch','Español'}
        self.tkvar = StringVar()
        self.tkvar.set('English') # set the default option

        popupMenu = OptionMenu(frame1, self.tkvar, *choices,command=self.func)
        self.l7=Label(frame1,text="Language",fg='black',bg='white',font=('Helvetica', 14, 'bold'))
        self.l7.grid(row=2,column=1,sticky=W)

        popupMenu.grid(row=2,column=2,columnspan=2, rowspan=1,sticky=W+E)

        self.b2=Button(frame1,text="Search entry",width=12,command=self.search_command)
        self.b2.grid(row=1,column=8)

        self.b6=Button(frame1,text="Close",width=12,command=window.destroy)
        self.b6.grid(row=2,column=8)

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


## MY FUNCTIONS
    def func(self,value):

        if value=='English':
            self.LANG=0
        elif value=='Deutsch':
            self.LANG=1
        elif value=='Español':
            self.LANG=2
        self.l1.config(text=["SEARCHING TOOLS", "WERKZEUGE SUCHEN", "BÚSQUEDA DE HERRAMIENTAS"][self.LANG])
        self.l2.config(text=["Stimulation Date", "Stimulationsdatum", "Fecha de estimulación"][self.LANG])
        self.l3.config(text=["Stimulation State", "Stimulationszustand", "Estado de estimulación"][self.LANG])
        self.l4.config(text=["Stimulations", "Stimulations", "Estimulaciones"][self.LANG])
        self.l8.config(text=["Data", "Daten", "Datos"][self.LANG])
        self.b0.config(text=["Load", "Laden", "Abrir"][self.LANG])
        self.l7.config(text=["Language", "Sprache", "Idioma"][self.LANG])
        self.b2.config(text=["Search entry","Eintrag suchen","Búsqueda"][self.LANG])
        self.b6.config(text=["Close","Schließen","Cerrar"][self.LANG])
        # for the ploting
        self.ax.set_xlabel(["Time (s)","Zeit (s)","Tiempo (s)"][self.LANG],{'fontname':'Helvetica', 'size':'12'})
        self.ax.set_ylabel(["Intensity (mA)","Intensität (mA)","Intensidad (mA)"][self.LANG],{'fontname':'Helvetica', 'size':'12'})
        self.ax.set_title(["Stimulation Parameters","Stimulationsparameter","Parámetros de estimulación"][self.LANG],{'fontname':'Helvetica', 'size':'12'})
        self.ax2.set_ylabel(["Voltage (V)","Spannung (V)","Voltaje (V)"][self.LANG],{'fontname':'Helvetica', 'size':'12'})
        self.ax3.set_ylabel(["Impedance (KOhm)","Impedanz (KOhm)","Impedancia (KOhm)"][self.LANG],{'fontname':'Helvetica', 'size':'12'})

        self.canvas.draw()

        print(value)
        print(str(self.LANG))

    def open_command(self):
        self.list1.delete(0,END)
        self.list1.insert(END,back_end.open1())

    def search_command(self):
        self.list1.delete(0,END)
        print(self.e2.get())
        for row in back_end.view1(self.e2.get()):
            self.list1.insert(END,row)

    def view_command(self):
        self.list1.delete(0,END)
        dir_list_info, dir_list_data=back_end.get_dir()
        back_end.fill_matrix(dir_list_info, dir_list_data)
        self.list1.delete(0,END)
        for row in back_end.view():
            self.list1.insert(END,row)

    def get_selected_row2(self,event):
        try:

            if len(self.list1.curselection())>1:
                self.e1.delete(0,END)
                self.e1.insert(END,'---')
                self.e2.delete(0,END)
                self.e2.insert(END,'---')
                #ploting part starts here
                print('more than one')
                index=self.list1.curselection()[0:]
                data=back_end.selection4(index)
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
                time=range(int(np.amax(d)))
                a.clear()
                self.ax.clear()
                self.ax2.clear()
                self.ax3.clear()
                self.ax.plot(time,data_avg[:,0],'tab:blue',label='current')
                self.ax.fill_between(time, data_avg[:,0]-data_error[:,0], data_avg[:,0]+data_error[:,0], alpha=0.2, edgecolor='#1B2ACC', facecolor='#089FFF')
                self.ax.set_xlabel(["Time (s)","Zeit (s)","Tiempo (s)"][self.LANG],{'fontname':'Helvetica', 'size':'12'})
                self.ax.set_ylabel(["Intensity (mA)","Intensität (mA)","Intensidad (mA)"][self.LANG],{'fontname':'Helvetica', 'size':'12'})
                self.ax.set_xlim(min(time)-1, max(time)+1)
                self.ax.set_title(["Stimulation Parameters","Stimulationsparameter","Parámetros de estimulación"][self.LANG],{'fontname':'Helvetica', 'size':'12'})

                self.ax2.plot(time,data_avg[:,1],'tab:orange',label='voltage')
                self.ax2.fill_between(time, data_avg[:,1]-data_error[:,1], data_avg[:,1]+data_error[:,1], alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')
                self.ax2.set_ylabel(["Voltage (V)","Spannung (V)","Voltaje (V)"][self.LANG],{'fontname':'Helvetica', 'size':'12'})
                self.ax2.grid(False)

                self.ax3.spines['right'].set_position(('axes', 1.25))
                self.ax3.plot(time,data_avg[:,2],'tab:olive',label='impedance')
                self.ax3.fill_between(time, data_avg[:,2]-data_error[:,2], data_avg[:,2]+data_error[:,2], alpha=0.5, edgecolor='tab:olive', facecolor='tab:olive')
                self.ax3.set_ylabel(["Impedance (KOhm)","Impedanz (KOhm)","Impedancia (KOhm)"][self.LANG],{'fontname':'Helvetica', 'size':'12'})
                self.ax3.grid(False)

                f.tight_layout()

                self.canvas.draw()


            else:
                index=self.list1.curselection()[0]
                rows=back_end.selection2(index)
                self.e1.delete(0,END)
                self.e1.insert(END,rows[0][0])
                self.e2.delete(0,END)
                self.e2.insert(END,rows[0][1])
                #PLOTTING
                index=self.list1.curselection()[0]
                data=back_end.selection3(index)
                #with this code we retrieve the information coded
                current=pickle.loads(data[0][0])

                a.clear()
                self.ax.clear()
                self.ax2.clear()
                self.ax3.clear()
                self.ax.plot(current.index.values,pickle.loads(data[0][0]),'tab:blue',label='current')
                self.ax.set_xlabel(["Time (s)","Zeit (s)","Tiempo (s)"][self.LANG],{'fontname':'Helvetica', 'size':'12'})
                self.ax.set_ylabel(["Intensity (mA)","Intensität (mA)","Intensidad (mA)"][self.LANG],{'fontname':'Helvetica', 'size':'12'})
                self.ax.set_xlim(min(current.index.values)-1, max(current.index.values)+1)
                self.ax.set_title(["Stimulation Parameters","Stimulationsparameter","Parámetros de estimulación"][self.LANG],{'fontname':'Helvetica', 'size':'12'})

                self.ax2.plot(current.index.values,pickle.loads(data[0][1]),'tab:orange',label='voltage')
                self.ax2.set_ylabel(["Voltage (V)","Spannung (V)","Voltaje (V)"][self.LANG],{'fontname':'Helvetica', 'size':'12'})
                self.ax2.grid(False)

                self.ax3.spines['right'].set_position(('axes', 1.25))
                self.ax3.plot(current.index.values,pickle.loads(data[0][2]),'tab:olive',label='impedance')
                self.ax3.set_ylabel(["Impedance (KOhm)","Impedanz (KOhm)","Impedancia (KOhm)"][self.LANG],{'fontname':'Helvetica', 'size':'12'})
                self.ax3.grid(False)

                f.tight_layout()

                self.canvas.draw()


        except IndexError:
            pass



window=Tk()
Window(window)
window.mainloop()
