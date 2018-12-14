import pandas
import more_itertools as mit
from tkinter import *
from tkinter.filedialog import askopenfilename
import os
import sqlite3
import pickle

class back:

    def __init__(self,db):
        print('initialized...')
        #Creating a data base from the available files
        self.conn=sqlite3.connect(db)
        self.cur=self.conn.cursor()
        try:
            self.cur.execute("DROP TABLE stimulation_data")
        except sqlite3.OperationalError:
            pass

        self.cur.execute("CREATE TABLE IF NOT EXISTS stimulation_data (id INTEGER PRIMARY KEY, dir_list_info, dir_list_data,stim_date_time,log_id, stim_id, stim_state, serial_APCS, serial_EDSM, stim_dur, current, impedance, voltage)")
        self.conn.commit()

    def open1(self):
        filename = [askopenfilename()]
        return filename

    def get_dir(self):
        dir_info='/Users/eli/Documents/Data_science/python3/DCSM_visualizer/data'
        dir_list_data = []
        dir_list_info = []
        for root, dirs, files in os.walk(dir_info):
            if any(file.endswith('info.txt') for file in files):
                if os.path.abspath(root).find('/st/')>0:
                    dir_list_data.append(os.path.abspath(root)+'/'+files[0])
                    dir_list_info.append(os.path.abspath(root)+'/'+files[1])
        return dir_list_info, dir_list_data

    def fill_matrix(self,dir_list_info, dir_list_data):
        for i,d in zip(dir_list_info,dir_list_data):
            info=pandas.read_csv(i,delimiter="\t",header=None)
            data=pandas.read_csv(d,delimiter="\t",header=None)

            stim_date_time=info.ix[1,0][info.ix[1,0].find('=')+1:]
            log_id=info.ix[2,0][info.ix[2,0].find('=')+1:]
            stim_id=info.ix[3,0][info.ix[3,0].find('=')+1:]
            stim_state=info.ix[4,0][info.ix[4,0].find('=')+1:]
            serial_apcs=info.ix[5,0][info.ix[5,0].find('=')+1:]
            serial_edsm=info.ix[6,0][info.ix[6,0].find('=')+1:]
            stim_dur=info.ix[7,0][info.ix[7,0].find('=')+1:]
            current=data.ix[0:,0]
            #we code the current to make it string and safe it in the database
            current_coded=pickle.dumps(current)
            #with this code we retrieve the information coded
            #print(pickle.loads(current_coded))
            impedance=data.ix[0:,1]
            impedance_coded=pickle.dumps(impedance)
            voltage=data.ix[0:,2]
            voltage_coded=pickle.dumps(voltage)

            self.cur.execute("INSERT INTO stimulation_data VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?)", (i,d,stim_date_time,log_id, stim_id, stim_state, serial_apcs, serial_edsm, stim_dur,current_coded,impedance_coded,voltage_coded))
            self.conn.commit()
            print("done filling data base")

    def view(self):
        self.cur.execute('SELECT id, stim_state, stim_date_time FROM stimulation_data')
        rows=self.cur.fetchall()
        return rows

    def view1(self,variable):
        self.cur.execute("SELECT id, stim_state, stim_date_time FROM stimulation_data WHERE stim_state=?",[variable])
        rows=self.cur.fetchall()
        return rows

    def selection2(self, index):
        self.cur.execute("SELECT stim_date_time,stim_state FROM stimulation_data WHERE id=?",str(index+1))
        rows=self.cur.fetchall()
        return rows

    def selection3(self, index):
        self.cur.execute("SELECT current, impedance, voltage FROM stimulation_data WHERE id=?",str(index+1))
        rows=self.cur.fetchall()
        return rows

    def selection4(self, index):
        index2=list(index)
        index2 = [x+1 for x in index2]
        print(str(index2))
        #self.cur.execute("SELECT current, impedance, voltage FROM stimulation_data WHERE id=?",str(index2))
        self.cur.execute('SELECT current, impedance, voltage FROM stimulation_data WHERE id in ({0})'.format(', '.join('?' for _ in index2)), index2)
        rows=self.cur.fetchall()
        return rows

    def __del__(self):
        self.conn.close()
