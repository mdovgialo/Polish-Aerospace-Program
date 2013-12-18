# -*- coding: utf8 -*-
import json
import sys
import Tkinter as Tk
from Tkinter import Frame
import time
import requests as rr
import math as m
import random
import ctypes
SPI_SETSCREENSAVEACTIVE = 17
def get_indicators():

    try:
        r=session.get("HTTP://"+ADDRESS+":8111/indicators", timeout=timeout)
        d = json.loads(r.text)        
    except:
        d = {}


        ## debug flaps:
##    d["valid"]=True
##    d["gear, %"] = random.choice([0, 1])
##    d["airbrake, %"] = int(time.time()*10%100)
##    d["flaps, %"] = int(time.time()*10%100)
        ## debug
    try:
        r=session.get("HTTP://"+ADDRESS+":8111/state", timeout=timeout)
        d.update( json.loads(r.text) )
    except:
        pass
##    d.update( json.loads('''{"valid": true,
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
##"ammo_counter4": 350.000000}'''))
##
##
##    d.update(json.loads('''{"valid": true,
##"aileron, %": 0,
##"elevator, %": -4,
##"rudder, %": 1,
##"TAS, km/h": 327,
##"IAS, km/h": 281,
##"M": 0.27,
##"AoA, deg": -0.7,
##"AoS, deg": 0.1,
##"Ny": 0.99,
##"Vy, m/s": 5.8,
##"Wx, deg/s": 0,
##"throttle 1, %": 110,
##"RPM throttle 1, %": 100,
##"radiator 1, %": 81,
##"power 1, hp": 2593.5,
##"RPM 1": 2699,
##"manifold pressure 1, atm": 1.37,
##"water temp 1, C": 89,
##"oil temp 1, C": 98,
##"pitch 1, deg": 28.4,
##"thrust 1, kgs": 1175,
##"efficiency 1, %": 54,
##"throttle 2, %": 110,
##"RPM throttle 2, %": 100,
##"radiator 2, %": 81,
##"power 2, hp": 2592.7,
##"RPM 2": 2699,
##"manifold pressure 2, atm": 1.37,
##"water temp 2, C": 89,
##"oil temp 2, C": 98,
##"pitch 2, deg": 28.4,
##"thrust 2, kgs": 1175,
##"efficiency 2, %": 54}'''))
    return d



l = 0
BG = 'black'
ALLERT_CL = 'red'
FG = 'white'
white = (255,255,255,255)
red = (255,0, 0 ,255)
TEMPERATURE_COLUMN = 0
AMMO_COLUMN = 2
ELEVATION_COLUMN = 1
OTHER_COLUMN = 3
NEEDED_INSTRUMENTS = ['vario', 'temperature', 'altitude_hour', 'ammo', 'flaps']
ADDRESS = "localhost"
timeout=0.001
session = rr.session()
dt = 1
IPSET=True
TS = 25
FONT = r'C:\Windows\Fonts\comicbd.ttf'
labelfont = (FONT, TS,)
labelfonts = (FONT, TS/2,)
class FlapsInd():
    def __init__(self, master, name):
        self.name = str(name)
        if self.name+'_size' in settings:
            self.size = settings[self.name+'_size']
        else:
            self.size = 50
        self.widget = Tk.Canvas(master, width=self.size, height=self.size, bg=BG, highlightthickness=0)
        if (self.name+'_gridx' in settings) and (self.name+'_gridy' in settings):
            self.widget.grid(column= int(settings[self.name+'_gridx']),row= int(settings[self.name+'_gridy']))
        else:
            self.widget.grid(column=OTHER_COLUMN,)
        wing = [self.size*0.1, self.size*0.5, self.size*0.3, self.size*0.3,
                self.size*0.9, self.size*0.5, self.size*0.85, self.size*0.5,
                self.size*0.5, self.size*0.5, self.size*0.1, self.size*0.5,]
        self.linewith=self.size/25
        self.wing = self.widget.create_line(*wing, fill=FG, smooth=True, width=self.linewith)
        self.flap = self.widget.create_line(self.size*0.5, self.size*0.5, self.size*0.7, self.size*0.7, fill=FG, width=self.linewith)

    def update(self, proc):
        self.widget.delete(self.flap)
        
        if proc == '--':
             self.flap = self.widget.create_line(self.size*0.0, self.size*1, self.size*1, 0,
                                            fill=ALLERT_CL, capstyle = Tk.ROUND, width=self.linewith)
        else:
            phi = proc/100.*m.pi/2.2
    
            r = 0.3
            
            pos =  [int(self.size*0.6 + self.size*r*m.cos(phi)) , int(self.size*0.5+self.size*r*m.sin(phi)),]
            self.flap = self.widget.create_line(self.size*0.6, self.size*0.5 ,pos[0], pos[1],
                                            fill=[FG, ALLERT_CL][proc>0], capstyle = Tk.ROUND, width=self.linewith)

class AirbrakeInd():
    def __init__(self, master, name):
        self.name = str(name)
        if self.name+'_size' in settings:
            self.size = settings[self.name+'_size']
        else:
            self.size = 50
        self.widget = Tk.Canvas(master, width=self.size, height=self.size, bg=BG, highlightthickness=0)
        if (self.name+'_gridx' in settings) and (self.name+'_gridy' in settings):
            self.widget.grid(column= int(settings[self.name+'_gridx']),row= int(settings[self.name+'_gridy']))
        else:
            self.widget.grid(column=OTHER_COLUMN,)
        wing = [self.size*0.1, self.size*0.5, self.size*0.3, self.size*0.3,
                self.size*0.9, self.size*0.5, self.size*0.85, self.size*0.5,
                self.size*0.5, self.size*0.5, self.size*0.1, self.size*0.5,]
        self.linewith=self.size/25
        self.wing = self.widget.create_line(*wing, fill=FG, smooth=True, width=self.linewith)
        self.flap1 = self.widget.create_line(self.size*0.5, self.size*0.5, self.size*0.7, self.size*0.7, fill=FG, width=self.linewith)
        self.flap2 = self.widget.create_line(self.size*0.5, self.size*0.5, self.size*0.7, self.size*0.3, fill=FG, width=self.linewith)
    def update(self, proc):
##        print proc, 'airbrake proc'
        self.widget.delete(self.flap1)
        self.widget.delete(self.flap2)

        if proc == '--':
             self.flap = self.widget.create_line(self.size*0.0, self.size*1, self.size*1, 0,
                                            fill=ALLERT_CL, capstyle = Tk.ROUND, width=self.linewith)
        else:
            phi = proc/100.*m.pi/2
    
            r = 0.4
            
            pos1 =  [int(self.size*0.6 + self.size*r*m.cos(phi)) , int(self.size*0.5+self.size*r*m.sin(phi)),]
            
            self.flap1 = self.widget.create_line(self.size*0.5, self.size*0.5 ,pos1[0], pos1[1],
                                            fill=[FG, ALLERT_CL][proc>0], capstyle = Tk.ROUND, width=self.linewith)
            pos2 =  [int(self.size*0.6 + self.size*r*m.cos(phi)) , int(self.size*0.5-self.size*r*m.sin(phi)),]
            
            self.flap2 = self.widget.create_line(self.size*0.5, self.size*0.5 ,pos2[0], pos2[1],
                                            fill=[FG, ALLERT_CL][proc>0], capstyle = Tk.ROUND, width=self.linewith)


class GearInd():
    def __init__(self, master, name):
        self.name = str(name)
        if self.name+'_size' in settings:
            self.size = settings[self.name+'_size']
        else:
            self.size = 50
        self.widget = Tk.Canvas(master, width=self.size, height=self.size, bg=BG, highlightthickness=0)
        if (self.name+'_gridx' in settings) and (self.name+'_gridy' in settings):
            self.widget.grid(column= int(settings[self.name+'_gridx']),row= int(settings[self.name+'_gridy']))
        else:
            self.widget.grid(column=OTHER_COLUMN,)
        wing = [self.size*0.1, self.size*0.38,
                self.size*0.9, self.size*0.38, ]
        
        plane = [self.size*0.45, self.size*0.2, self.size*0.55, self.size*0.39]
        self.linewith=self.size/25
        
        self.wing = self.widget.create_line(*wing, fill=FG, smooth=True, width=self.linewith, capstyle = Tk.ROUND )
        self.plane = self.widget.create_oval(*plane, outline = FG, fill= FG, width=self.linewith )
        self.planeu = self.widget.create_line(self.size*0.5, self.size*0.2, self.size*0.5, self.size*0.01, fill=FG, smooth=False, width=self.linewith/2)
        self.gearup = False
    def show_gear(self):
        if self.gearup==True:
            tag = 'GEAR'
            self.gear1 =  self.widget.create_line(self.size*0.3, self.size*0.38, self.size*0.3, self.size*0.5,
                                                  fill=ALLERT_CL, width=self.linewith/2, capstyle = Tk.ROUND, tags=tag)
            self.gear2 =  self.widget.create_line(self.size*0.7, self.size*0.38, self.size*0.7, self.size*0.5,
                                                  fill=ALLERT_CL, width=self.linewith/2, capstyle = Tk.ROUND, tags=tag)
            self.gear3 = self.widget.create_oval(self.size*0.28, self.size*0.45,
                                                 self.size*0.32, self.size*0.55,
                                                 outline = ALLERT_CL, fill= ALLERT_CL, width=self.linewith/2, tags=tag )
            self.gear3 = self.widget.create_oval(self.size*0.68, self.size*0.45,
                                                 self.size*0.72, self.size*0.55,
                                                 outline = ALLERT_CL, fill= ALLERT_CL, width=self.linewith/2 , tags=tag)
            self.gearup = False
        else:
            self.widget.delete('GEAR')
            self.gearup = True
    def update(self, proc):
        if proc == '--':
            self.widget.delete('GEAR')
            self.gear1 =  self.widget.create_line(self.size*0.0, self.size*1, self.size*1, 0,
                                            fill=ALLERT_CL, capstyle = Tk.ROUND, width=self.linewith, tags='GEAR')
        else:
            self.gearup=proc>0
            
            self.show_gear()


            
class GenericInd():
    def __init__(self, master, name):
        self.label = Tk.StringVar()
        self.name = str(name)
        if self.name+'_size' in settings:
            self.widget = Tk.Label(master, textvariable=self.label,fg=FG, bg=BG, font=(FONT, int(settings[self.name+'_size'])))
        else:
            self.widget = Tk.Label(master, textvariable=self.label,fg=FG, bg=BG, font=labelfont)
        if (self.name+'_gridx' in settings) and (self.name+'_gridy' in settings):
            self.widget.grid(column= int(settings[self.name+'_gridx']),row= int(settings[self.name+'_gridy']))
        else:
            self.widget.grid(column=OTHER_COLUMN,)
        if (self.name+'_prefix' in settings):
            self.prefix = settings[self.name+'_prefix']
        else:
            self.prefix = self.name
            
        if (self.name+'_limit' in settings):
            self.limit = settings[self.name+'_limit']
        else:
            self.limit = 100000000000
        self.update(0)
        
    def update(self, temp):
        if temp > self.limit:
            self.widget.config(fg=ALLERT_CL)
        else:
            self.widget.config(fg=FG) 
        self.label.set(self.prefix+' {}'.format(temp))

class VarioInd():
    def __init__(self, master, name):
        self.label = Tk.StringVar()
        
        self.name = str(name)
        if self.name+'_size' in settings:
            self.widget = Tk.Label(master, textvariable=self.label,fg=FG, bg=BG, font=(FONT, int(settings[self.name+'_size'])))
        else:
            self.widget = Tk.Label(master, textvariable=self.label,fg=FG, bg=BG, font=labelfont)
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
        try:
            temp=int(temp)
        except:
            temp='--'
        self.label.set(self.prefix+' {}'.format(temp)+' m/s')

class WaterTempInd():
    def __init__(self, master, name):
        self.label = Tk.StringVar()
        self.name = str(name)
        if self.name+'_size' in settings:
            self.widget = Tk.Label(master, textvariable=self.label,fg=FG, bg=BG, font=(FONT, int(settings[self.name+'_size'])))
        else:
            self.widget = Tk.Label(master, textvariable=self.label,fg=FG, bg=BG, font=labelfont)
        if (self.name+'_gridx' in settings) and (self.name+'_gridy' in settings):
            self.widget.grid(column= int(settings[self.name+'_gridx']),row= int(settings[self.name+'_gridy']))
        else:
            self.widget.grid(column=TEMPERATURE_COLUMN,)
        if (self.name+'_prefix' in settings):
            self.prefix = settings[self.name+'_prefix']
        else:
            self.prefix = u"H₂O "
            
        if (self.name+'_limit' in settings):
            self.limit = settings[self.name+'_limit']
        else:
            self.limit = 98
        self.update(0)
        
    def update(self, temp):
        try:
            temp=int(temp)
        except:
            pass
        if temp > self.limit:
            self.widget.config(fg=ALLERT_CL)
        else:
            self.widget.config(fg=FG)               
        self.label.set(self.prefix+self.name[17:]+' '+str(temp)+u' °C')

class HeadTempInd():
    def __init__(self, master, name):
        self.label = Tk.StringVar()
        self.name = str(name)
        if self.name+'_size' in settings:
            self.widget = Tk.Label(master, textvariable=self.label,fg=FG, bg=BG, font=(FONT, int(settings[self.name+'_size'])))
        else:
            self.widget = Tk.Label(master, textvariable=self.label,fg=FG, bg=BG, font=labelfont)
        if (self.name+'_gridx' in settings) and (self.name+'_gridy' in settings):
            self.widget.grid(column= int(settings[self.name+'_gridx']),row= int(settings[self.name+'_gridy']))
        else:
            self.widget.grid(column=TEMPERATURE_COLUMN,)
        if (self.name+'_prefix' in settings):
            self.prefix = settings[self.name+'_prefix']
        else:
            self.prefix = u"Head "
        if (self.name+'_limit' in settings):
            self.limit = settings[self.name+'_limit']
        else:
            self.limit = 100000000000
        self.update(0)
        
    def update(self, temp):
        try:
            temp=int(temp)
        except:
            temp = '--'
        if temp > self.limit:
            self.widget.config(fg=ALLERT_CL)
        else:
            self.widget.config(fg=FG) 
        self.label.set(self.prefix+self.name[17:]+' '+str(temp)+u' °C')

class AmmoInd():
    def __init__(self, master, name):
        self.label = Tk.StringVar()
        self.name = str(name)
        if self.name+'_size' in settings:
            self.widget = Tk.Label(master, textvariable=self.label,fg=FG, bg=BG, font=(FONT, int(settings[self.name+'_size'])))
        else:
            self.widget = Tk.Label(master, textvariable=self.label,fg=FG, bg=BG, font=labelfont)
        if (self.name+'_gridx' in settings) and (self.name+'_gridy' in settings):
            self.widget.grid(column= int(settings[self.name+'_gridx']),row= int(settings[self.name+'_gridy']))
        else:
            self.widget.grid(column=AMMO_COLUMN,)
        if (self.name+'_prefix' in settings):
            self.prefix = settings[self.name+'_prefix']
        else:
            self.prefix = "Ammo "
        if (self.name+'_limit' in settings):
            self.limit = settings[self.name+'_limit']
        else:
            self.limit = 0
        self.update(1)
        
    def update(self, temp):
        try:
            temp=int(temp)
        except:
            pass
        if temp < self.limit:
            self.widget.config(fg=ALLERT_CL)
        else:
            self.widget.config(fg=FG) 
        self.label.set(self.prefix+self.name[12:]+' '+str(temp))

class OilTempInd():
    def __init__(self, master, name):
        self.label = Tk.StringVar()
        self.name = str(name)
        if self.name+'_size' in settings:
            self.widget = Tk.Label(master, textvariable=self.label,fg=FG, bg=BG, font=(FONT, int(settings[self.name+'_size'])))
        else:
            self.widget = Tk.Label(master, textvariable=self.label,fg=FG, bg=BG, font=labelfont)
        if (self.name+'_gridx' in settings) and (self.name+'_gridy' in settings):
            self.widget.grid(column= int(settings[self.name+'_gridx']),row= int(settings[self.name+'_gridy']))
        else:
            self.widget.grid(column=TEMPERATURE_COLUMN,)
        if (self.name+'_prefix' in settings):
            self.prefix = settings[self.name+'_prefix']
        else:
            self.prefix = "Oil "
        if (self.name+'_limit' in settings):
            self.limit = settings[self.name+'_limit']
        else:
            self.limit = 100000000000
        self.update(0)
        
    def update(self, temp):
        try:
            temp=int(temp)
        except:
            pass
        if temp > self.limit:
            self.widget.config(fg=ALLERT_CL)
        else:
            self.widget.config(fg=FG)   
        self.label.set(self.prefix+self.name[15:]+' '+str(temp)+u' °C')






        ####################################################################################################
                                                    
class App:                         ### (1)
    def __init__(self, myParent):      ### (1a)
        
        self.status = Tk.StringVar()
        self.status.set('Avaiting indicators from game session')
        self.statuswidg = Tk.Label(myParent, textvariable=self.status, fg=FG, bg=BG, font=labelfonts).pack()
        
        self.frame = Frame(myParent)
        self.frame.pack()
        self.statusbar = Frame(myParent)
        self.statusbar.pack()
        self.frame.config(bg=BG)
        self.ind = get_indicators()
       

        self.inds = {}
        self.t_m=time.time()
        self.frame.after(int(dt*1000), self.upd)
        
        
    def inds_to_disp(self, master):
        ind_d = {}
        for instr in NEEDED_INSTRUMENTS:
            if DRAW_ALL:
                ind_d[instr] = self.get_instr(instr, master)
            else:
                for available in self.ind.keys():
                    if instr in available:
                        ind_d[available] = self.get_instr(available, master)
##        print ind_d
        return ind_d
                    
    def upd(self):
        d = get_indicators()
        try:
            if 'vario' not in d and len(d)>1:
                d['vario'] = (d['altitude_hour']-self.ind['altitude_hour'])/(time.time()-self.t_m)
                self.t_m=time.time()
        except Exception:
            try:
                if len(d)>1:
                    d['vario'] = '--'
            except:
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
                    ind.update('--')
        elif d['valid']==False and len(self.inds)>0:
            for child in self.frame.winfo_children():
                child.destroy()
            self.inds={}
            self.ind ={}

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
        elif "flaps, %" == instr:
            return FlapsInd(master, instr)
        elif "gear, %" in instr:
            return GearInd(master, instr)
        elif "airbrake, %" in instr:
##            print 'airbrake in instr'
            return AirbrakeInd(master, instr)
        
        else:
            return GenericInd(master, instr)
SPI_SETSCREENSAVEACTIVE = 17
SPI_GETSCREENSAVEACTIVE = 16
def setScreenSaverEnabled(state):
    """Enable or disable the Windows screensaver.
    Note that enabling the screen save isn't the same as running it. It just
    means that the saver *will* run after the screen saver wait time has elapsed
    the PC is unused during that time."""
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETSCREENSAVEACTIVE,
                                               state,
                                               None,
                                               0)
    
def getScreenSaverEnabled():
    state = ctypes.c_int()
    ctypes.windll.user32.SystemParametersInfoA(SPI_GETSCREENSAVEACTIVE,
                                               0,
                                               ctypes.byref(state),
                                               0)
    return bool(state.value)

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
    except Exception as E:
        print 'EXCEPTION Settings Error:', E
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
    try:
        DRAW_ALL = settings['DRAW_ALL']
    except:
        DRAW_ALL = 0
    labelfont = (FONT, TS,)
    labelfonts = (FONT, TS/2,)
    print settings
    print NEEDED_INSTRUMENTS
    print ADDRESS

    

    root = Tk.Tk()
    try:
        if  settings['ON_TOP'] == 1:
            root.wm_attributes("-topmost", 1)
    except:
        pass
    root.config(bg=BG)
    cockpit = App(root)

    try :
        scr_act = getScreenSaverEnabled()
        if scr_act:
             setScreenSaverEnabled(False)
    except:
        pass
    root.mainloop()
    try :
        if scr_act:
             setScreenSaverEnabled(True)
    except:
        pass
