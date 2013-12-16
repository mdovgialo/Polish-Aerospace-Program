# -*- coding: utf8 -*-
import json
import sys
import Tkinter as Tk
from Tkinter import Frame
import time
import requests as rr

def get_indicators():

##    print 'getting inds'
    try:
        r=session.get("HTTP://"+ADDRESS+":8111/indicators", timeout=timeout)
    ##    print r.text
    ##    r = conn.getresponse()
    ##    print 
    ##    r = urllib2.urlopen('http://'+ADDRESS+':8111/indicators')
        
        d = json.loads(r.text)
        

    except:
        d = {}
##    d = json.loads('''{"valid": true,
##"speed": 0.000512,
##"pedals1": -1.000000,
##"pedals2": -1.000000,
##"stick_elevator": 0.000000,
##"stick_ailerons": 0.001099,
##"vario": 0.000000,
##"altitude_hour": 62.090237,
##"altitude_min": 62.090237,
##"aviahorizon_roll": 0.004631,
##"aviahorizon_pitch": -11.503861,
##"bank": -0.004631,
##"bank1": -0.004631,
##"turn": -0.000000,
##"turn1": -0.000000,
##"compass": 41.759010,
##"compass1": 41.759010,
##"compass2": 41.759010,
##"clock_hour": 6.716667,
##"clock_min": 43.000000,
##"clock_sec": 16.000000,
##"manifold_pressure": 0.704258,
##"oil_pressure": 23.989164,
##"oil_pressure1": 23.989162,
##"oil_temperature": 23.989164,
##"oil_temperature1": 23.989162,
##"water_temperature": 19.427303,
##"water_temperature1": 19.427307,
##"mixture": 1.000000,
##"fuel1": 554.640625,
##"fuel2": 0.000000,
##"fuel_pressure": 0.000000,
##"fuel_pressure1": 0.000000,
##"oxygen": 0.000000,
##"trimmer": -0.000000,
##"throttle": 0.000000,
##"weapon1": 0.000000,
##"weapon2": 0.000000,
##"ammo_counter1": 350.000000,
##"ammo_counter2": 120.000000,
##"ammo_counter3": 120.000000,
##"ammo_counter4": 350.000000}''')

    return d



l = 0
white = (255,255,255,255)
red = (255,0, 0 ,255)
TEMPERATURE_COLUMN = 0
AMMO_COLUMN = 2
ELEVATION_COLUMN = 1
OTHER_COLUMN = 3
NEEDED_INSTRUMENTS = ['vario', 'temperature', 'altitude_hour', 'ammo', 'flaps']
ADDRESS = "localhost"
timeout=0.001
session = rr.session()#ADDRESS+':8111')
##conn.connect()
dt = 1
IPSET=True
TS = 25
FONT = r'C:\Windows\Fonts\comicbd.ttf'
labelfont = (FONT, TS,)
labelfonts = (FONT, TS/2,)
class GenericInd():
    def __init__(self, master, name):
        self.label = Tk.StringVar()
        self.name = str(name)
        if self.name+'_size' in settings:
            self.widget = Tk.Label(master, textvariable=self.label,fg='white', bg='black', font=(FONT, int(settings[self.name+'_size'])))
        else:
            self.widget = Tk.Label(master, textvariable=self.label,fg='white', bg='black', font=labelfont)
        if (self.name+'_gridx' in settings) and (self.name+'_gridy' in settings):
            self.widget.grid(column= int(settings[self.name+'_gridx']),row= int(settings[self.name+'_gridy']))
        else:
            self.widget.grid(column=OTHER_COLUMN,)
        if (self.name+'_prefix' in settings):
            self.prefix = settings[self.name+'_prefix']
        else:
            self.prefix = self.name
        
        self.update(0)
        
    def update(self, temp):                 
        self.label.set(self.prefix+' '+str(temp))

class VarioInd():
    def __init__(self, master, name):
        self.label = Tk.StringVar()
        self.name = str(name)
        if self.name+'_size' in settings:
            self.widget = Tk.Label(master, textvariable=self.label,fg='white', bg='black', font=(FONT, int(settings[self.name+'_size'])))
        else:
            self.widget = Tk.Label(master, textvariable=self.label,fg='white', bg='black', font=labelfont)
        if (self.name+'_gridx' in settings) and (self.name+'_gridy' in settings):
            self.widget.grid(column= int(settings[self.name+'_gridx']),row= int(settings[self.name+'_gridy']))
        else:
            self.widget.grid(column=OTHER_COLUMN,)

        if (self.name+'_prefix' in settings):
            self.prefix = settings[self.name+'_prefix']
        else:
            self.prefix = self.name
        
        self.update(0)
        
    def update(self, temp):                 
        self.label.set(self.prefix+' '+str(int(temp))+' m/s')

class WaterTempInd():
    def __init__(self, master, name):
        self.label = Tk.StringVar()
        self.name = str(name)
        if self.name+'_size' in settings:
            self.widget = Tk.Label(master, textvariable=self.label,fg='white', bg='black', font=(FONT, int(settings[self.name+'_size'])))
        else:
            self.widget = Tk.Label(master, textvariable=self.label,fg='white', bg='black', font=labelfont)
        if (self.name+'_gridx' in settings) and (self.name+'_gridy' in settings):
            self.widget.grid(column= int(settings[self.name+'_gridx']),row= int(settings[self.name+'_gridy']))
        else:
            self.widget.grid(column=TEMPERATURE_COLUMN,)
        if (self.name+'_prefix' in settings):
            self.prefix = settings[self.name+'_prefix']
        else:
            self.prefix = u"H₂O "
        self.update(0)
        
    def update(self, temp):
        if temp > 95:
            self.widget.config(fg='red')
        else:
            self.widget.config(fg='white')                   
        self.label.set(self.prefix+self.name[17:]+' '+str(int(temp))+u' °C')

class HeadTempInd():
    def __init__(self, master, name):
        self.label = Tk.StringVar()
        self.name = str(name)
        if self.name+'_size' in settings:
            self.widget = Tk.Label(master, textvariable=self.label,fg='white', bg='black', font=(FONT, int(settings[self.name+'_size'])))
        else:
            self.widget = Tk.Label(master, textvariable=self.label,fg='white', bg='black', font=labelfont)
        if (self.name+'_gridx' in settings) and (self.name+'_gridy' in settings):
            self.widget.grid(column= int(settings[self.name+'_gridx']),row= int(settings[self.name+'_gridy']))
        else:
            self.widget.grid(column=TEMPERATURE_COLUMN,)
        if (self.name+'_prefix' in settings):
            self.prefix = settings[self.name+'_prefix']
        else:
            self.prefix = u"Head "
        self.update(0)
        
    def update(self, temp):            
        self.label.set(self.prefix+self.name[17:]+' '+str(int(temp))+u' °C')

class AmmoInd():
    def __init__(self, master, name):
        self.label = Tk.StringVar()
        self.name = str(name)
        if self.name+'_size' in settings:
            self.widget = Tk.Label(master, textvariable=self.label,fg='white', bg='black', font=(FONT, int(settings[self.name+'_size'])))
        else:
            self.widget = Tk.Label(master, textvariable=self.label,fg='white', bg='black', font=labelfont)
        if (self.name+'_gridx' in settings) and (self.name+'_gridy' in settings):
            self.widget.grid(column= int(settings[self.name+'_gridx']),row= int(settings[self.name+'_gridy']))
        else:
            self.widget.grid(column=AMMO_COLUMN,)
        if (self.name+'_prefix' in settings):
            self.prefix = settings[self.name+'_prefix']
        else:
            self.prefix = "Ammo "
        self.update(1)
        
    def update(self, temp):
        if temp < 50:
            self.widget.config(fg='red')
        else:
            self.widget.config(fg='white') 
        self.label.set(self.prefix+self.name[12:]+' '+str(int(temp)))

class OilTempInd():
    def __init__(self, master, name):
        self.label = Tk.StringVar()
        self.name = str(name)
        if self.name+'_size' in settings:
            self.widget = Tk.Label(master, textvariable=self.label,fg='white', bg='black', font=(FONT, int(settings[self.name+'_size'])))
        else:
            self.widget = Tk.Label(master, textvariable=self.label,fg='white', bg='black', font=labelfont)
        if (self.name+'_gridx' in settings) and (self.name+'_gridy' in settings):
            self.widget.grid(column= int(settings[self.name+'_gridx']),row= int(settings[self.name+'_gridy']))
        else:
            self.widget.grid(column=TEMPERATURE_COLUMN,)
        if (self.name+'_prefix' in settings):
            self.prefix = settings[self.name+'_prefix']
        else:
            self.prefix = "Oil "
        self.update(0)
        
    def update(self, temp):
        if temp > 110:
            self.widget.config(fg='red')
        else:
            self.widget.config(fg='white')   
        self.label.set(self.prefix+self.name[15:]+' '+str(int(temp))+u' °C')
class App:                         ### (1)
    def __init__(self, myParent):      ### (1a)
        
        self.status = Tk.StringVar()
        self.status.set('Avaiting indicators from game session')
        self.statuswidg = Tk.Label(myParent, textvariable=self.status, fg='white', bg='black', font=labelfonts).pack()

        self.frame = Frame(myParent)
        self.frame.pack()
        self.frame.config(bg='black')
        self.ind = get_indicators()
       

        self.inds = {}
        self.t_m=time.time()
        self.frame.after(int(dt*1000), self.upd)
        
        
    def inds_to_disp(self, master):
        ind_d = {}
        for instr in NEEDED_INSTRUMENTS:
            for available in self.ind.keys():
                if instr in available:
                    
                    ind_d[available] = self.get_instr(available, master)
        return ind_d
                    
    def upd(self):
        d = get_indicators()
        try:
            if 'vario' not in d:
                d['vario'] = (d['altitude_hour']-self.ind['altitude_hour'])/(time.time()/self.t_m)
                self.t_m=time.time()
        except Exception:
            pass
        self.ind = d
        if len(d) == 0:
            for child in self.frame.winfo_children():
                child.destroy()
            self.status.set('No response from game at: '+"HTTP://"+ADDRESS+":8111/indicators")
        elif d['valid'] and len(self.inds)>0:
            self.status.set('In game at: '+"HTTP://"+ADDRESS+":8111/indicators")
            for ind in self.inds.values():
                try:
                    ind.update(d[ind.name])
                except:
                    pass
        elif d['valid']==False and len(self.inds)>0:
            for child in self.frame.winfo_children():
                child.destroy()
            self.inds={}

        elif d['valid']==True and len(self.inds)<1:
            ds = self.inds_to_disp(self.frame)
            self.inds = ds
        if  len(d) != 0 and d['valid']==False:
            if len(self.frame.winfo_children())<1:
               self.status.set('Avaiting indicators from game session')

            
        self.frame.after(int(dt*1000), self.upd)

    def get_instr(self, instr, master):
        if 'water_temperature' in instr:
            return WaterTempInd(master, instr)
        elif 'oil_temperature' in instr:
            return OilTempInd(master, instr)
        elif 'ammo' in instr:
            return AmmoInd(master, instr)
        elif 'vario' in instr:
            return VarioInd(master, instr)
        elif 'head_temperature' in instr:
            return HeadTempInd(master, instr)
        
        else:
            return GenericInd(master, instr)

if __name__ == '__main__':
    try:
        ADDRESS = open('adress.txt').read().strip()
        print 'new adress', ADDRESS
    except Exception:
        print 'adress reading failed'
       

    
    NEEDED_INSTRUMENTS = []
    ins = open('instruments.txt')
    for i in ins:
        NEEDED_INSTRUMENTS.append(i.strip())
        print i
    try:
        settings = json.loads(open('settings.txt').read().decode('utf-8-sig'))
    except:
        pass
    try:
        TS = settings['s']
    except:
        pass
    try:
        FONT = settings['font']
    except:
        pass
    try:
        dt = settings['dt']
    except:
        pass
    try:
        timeout = settings['timeout']
    except:
        pass
    labelfont = (FONT, TS,)
    labelfonts = (FONT, TS/2,)
    print settings
    print NEEDED_INSTRUMENTS
    print ADDRESS

    

    root = Tk.Tk()
    root.config(bg='black')
    cockpit = App(root)
    root.mainloop()
