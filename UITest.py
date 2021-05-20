import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import time
import numpy as np
import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
from itertools import count
import pandas as pd
import queue
import datetime


plt.style.use('fivethirtyeight')

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)

genDataY = []
conDataY = []
batDataY = []
timeX1=[]
#timeX1 =[datetime.datetime.now() + datetime.timedelta(minutes=i) for i in range(12)]
timeX2 =[0]
timeX3 =[0]
timeX4 =[0]
timeX5 =[0]
timeX6 =[0]
timeX7 =[0]
timeX8 =[0]
load1Data=[0]



load2Data=[0]
load3Data=[0]
load4Data=[0]
load5Data=[0]
load6Data=[0]
load7Data=[0]
load8Data=[0]

#def animate(i):
    

#message Handler
def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    top = str(message.topic)
    loadNum = msg[0:1]
    float(loadNum)
    data = msg[1:len(msg)]
    float(data)
    print("Load: " + loadNum + "\n")
    print("Value: " + data + "\n")
    #load decisions
    if loadNum == 0:
        if len(load1Data) >= 288:
            load1Data.remove(1)
        load1Data.append(data)
    elif loadNum == 1:
        if len(load2Data) >= 288:
            load2Data.remove(1)
        load2Data.append(data)
    elif loadNum == 2:
        if len(load3Data) >= 288:
            load3Data.remove(1)
        load3Data.append(data)
    elif loadNum == 3:
        if len(load4Data) >= 288:
            load4Data.remove(1)
        load4Data.append(data)
    elif loadNum == 4:
        if len(load5Data) >= 288:
            load5Data.remove(1)
        load5Data.append(data)
    elif loadNum == 5:
        if len(load6Data) >= 288:
            load6Data.remove(1)
        load6Data.append(data)
    elif loadNum == 6:
        if len(load7Data) >= 288:
            load7Data.remove(1)
        load7Data.append(data)
    elif loadNum == 7:
        if len(load8Data) >= 288:
            load8Data.remove(1)
        load8Data.append(data)

            
def subscribe():
    broker = "broker.mqttdashboard.com"
    dataTopic = "seniordesign/microgrid/data"
    client.on_message=on_message
    client.connect(broker)
    client.subscribe(dataTopic)
    client.loop_start()


#to publish messages to server( commands - Load# on/off
def publish(load):
    print ("starting")
    if loadValue[load]==0:
        loadValue[load]=1
    else:
        loadValue[load]=0
    print("finish if")
    commandTopic = "seniordesign/microgrid/command"
    print ("Printing")
    client.publish(commandTopic, str(load) + " " + str(loadValue[load]))



#s=Style()
#s.configure('Off.Button', background = 'red')
#s.configure('On.Button', background = 'green')

LARGE_FONT = ("VERDANA", 12)


loadValue = [1,1,1,1,1,1,1,1]


class MainPage(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Power Generation")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PerfPage, LoadPage, InfoPage, LoadGraphPage1, LoadGraphPage2, LoadGraphPage3, LoadGraphPage4, LoadGraphPage5, LoadGraphPage6, LoadGraphPage7, LoadGraphPage8):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()
#-------------------------------------------------------------------------------------------------------

#Main Page
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="", font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        homeButton = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        #homeButton.pack()
        homeButton.place(relx=0, rely=0, relwidth=0.1, relheight=0.08)

        perfButton = ttk.Button(self, text="Performance",
                            command=lambda: controller.show_frame(PerfPage))
        #perfButton.pack()
        perfButton.place(relx=.3, rely=0, relwidth=0.15, relheight=0.08)

        infoButton = ttk.Button(self, text="Info",
                            command=lambda: controller.show_frame(InfoPage))
        #infoButton.pack()
        infoButton.place(relx=.9, rely=0, relwidth=0.1, relheight=0.08)

        toggleButton = ttk.Button(self, text="Toggle",
                            command=lambda: controller.show_frame(LoadPage))
        #toggleButton.pack()
        toggleButton.place(relx=.6, rely=0, relwidth=0.15, relheight=0.08)

        
        
        #GENERATED GRAPH
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        ax = [25,27,29,20,15,16,32,35,37,39,28,25,22,18,16,12,6,0,16,20,20,20,30,31]
        ay = [-24,-23,-22,-21,-20,-19,-18,-17,-16,-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1]
        a.plot(ay, ax)
        a.set_xlabel('Time')
        a.set_ylabel('Power')
        a.set_title('Power Generated')
                    
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.NONE, expand = False)


        #CONSUMED GRAPH
        f = Figure(figsize=(5,5), dpi=100)
        b = f.add_subplot(111)
        bx = [20,20,20,22,24,20.22,30,32,34,32,30,20,18,16,20,24,26,28,30,28,28,28,20,18]
        by = [-24,-23,-22,-21,-20,-19,-18,-17,-16,-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1]
        b.plot(by, bx)
        b.set_xlabel('Time')
        b.set_ylabel('Power')
        b.set_title('Power Consumed')
                    
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.NONE, expand = True)


        #Battery GRAPH
        f = Figure(figsize=(5,5), dpi=100)
        c = f.add_subplot(111)
        cx = [100,90,80,70,60,50,40,30,20,10]
        cy = [1,2,3,4,5,6,7,8,9,10]
        c.plot(cy, cx)
        c.set_xlabel('Time')
        c.set_ylabel('Battery ')
        c.set_title('Battery %')
                    
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.NONE, expand = False)
        
#---------------------------------------------------------------------------------------------
        
##Performance Page
class PerfPage(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Performance", font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        homeButton = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        #homeButton.pack()
        homeButton.place(relx=0, rely=0, relwidth=0.1, relheight=0.08)

        infoButton = ttk.Button(self, text="Info",
                            command=lambda: controller.show_frame(InfoPage))
        #infoButton.pack()
        infoButton.place(relx=.9, rely=0, relwidth=0.1, relheight=0.08)


        #BUTTONS FOR EACH LOAD:
        l1Button = ttk.Button(self, text="Load 1",
                            command=lambda: controller.show_frame(LoadGraphPage1))
        l1Button.place(relx=.35, rely=.3, relwidth=0.1, relheight=0.08)

        l2Button = ttk.Button(self, text="Load 2",
                            command=lambda: controller.show_frame(LoadGraphPage2))
        l2Button.place(relx=.55, rely=.3, relwidth=0.1, relheight=0.08)

        l3Button = ttk.Button(self, text="Load 3",
                            command=lambda: controller.show_frame(LoadGraphPage3))
        l3Button.place(relx=.35, rely=.4, relwidth=0.1, relheight=0.08)

        l4Button = ttk.Button(self, text="Load 4",
                            command=lambda: controller.show_frame(LoadGraphPage4))
        l4Button.place(relx=.55, rely=.4, relwidth=0.1, relheight=0.08)

        l5Button = ttk.Button(self, text="Load 5",
                            command=lambda: controller.show_frame(LoadGraphPage5))
        l5Button.place(relx=.35, rely=.5, relwidth=0.1, relheight=0.08)

        l6Button = ttk.Button(self, text="Load 6",
                            command=lambda: controller.show_frame(LoadGraphPage6))
        l6Button.place(relx=.55, rely=.5, relwidth=0.1, relheight=0.08)

        l7Button = ttk.Button(self, text="Load 7",
                            command=lambda: controller.show_frame(LoadGraphPage7))
        l7Button.place(relx=.35, rely=.6, relwidth=0.1, relheight=0.08)

        l8Button = ttk.Button(self, text="Load 8",
                            command=lambda: controller.show_frame(LoadGraphPage8))
        l8Button.place(relx=.55, rely=.6, relwidth=0.1, relheight=0.08)


#--------------------------------------------------------------------------------------------------------
class LoadGraphPage1(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Load 1 Graph", font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        homeButton = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        #homeButton.pack()
        homeButton.place(relx=0, rely=0, relwidth=0.1, relheight=0.08)

        infoButton = ttk.Button(self, text="Info",
                            command=lambda: controller.show_frame(InfoPage))
        #infoButton.pack()
        infoButton.place(relx=.9, rely=0, relwidth=0.1, relheight=0.08)


        #LOAD GRAPH
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        ax = [1,2,3,4,5,6,7,8,9,10]
        ay = [1,2,3,4,5,6,7,8,9,10]
        a.plot(ax,ay)
        #a.plot(timeX1, load1Data)
        a.set_xlabel('Time (past 24hrs)')
        a.set_ylabel('Power')
        a.set_title('Load: ')
        #a.gcf().autofmt_xdate()
        #myFmt = mdates.DateFormatter('%H:%M')
        #a.gca().xaxis.set_major_formatter(myFmt)
        #a.show()
                    
        #def animate():
         #   x_vals.append()
          #  y_vals.append(
          #  plt.cla()
          #  plt.plot(x_vals, y_vals)

        #ani = FuncAnimation(plt.gcf(), animate, interval=300000)
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)


#--------------------------------------------------------------------------------------------------------
class LoadGraphPage2(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Load 2 Graph", font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        homeButton = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        #homeButton.pack()
        homeButton.place(relx=0, rely=0, relwidth=0.1, relheight=0.08)

        infoButton = ttk.Button(self, text="Info",
                            command=lambda: controller.show_frame(InfoPage))
        #infoButton.pack()
        infoButton.place(relx=.9, rely=0, relwidth=0.1, relheight=0.08)


        #LOAD GRAPH
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        #a.plot(timeX, load2Data)
        a.set_xlabel('Time (past 24hrs)')
        a.set_ylabel('Power')
        a.set_title('Load: ')
                    
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)

#--------------------------------------------------------------------------------------------------------
class LoadGraphPage3(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Load 3 Graph", font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        homeButton = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        #homeButton.pack()
        homeButton.place(relx=0, rely=0, relwidth=0.1, relheight=0.08)

        infoButton = ttk.Button(self, text="Info",
                            command=lambda: controller.show_frame(InfoPage))
        #infoButton.pack()
        infoButton.place(relx=.9, rely=0, relwidth=0.1, relheight=0.08)


        #LOAD GRAPH
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        #a.plot(timeX, load3Data)
        a.set_xlabel('Time (past 24hrs)')
        a.set_ylabel('Power')
        a.set_title('Load: ')
                    
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)

#--------------------------------------------------------------------------------------------------------
class LoadGraphPage4(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Load 4 Graph", font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        homeButton = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        #homeButton.pack()
        homeButton.place(relx=0, rely=0, relwidth=0.1, relheight=0.08)

        infoButton = ttk.Button(self, text="Info",
                            command=lambda: controller.show_frame(InfoPage))
        #infoButton.pack()
        infoButton.place(relx=.9, rely=0, relwidth=0.1, relheight=0.08)


        #LOAD GRAPH
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        #a.plot(timeX, load4Data)
        a.set_xlabel('Time (past 24hrs)')
        a.set_ylabel('Power')
        a.set_title('Load: ')
                    
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)

#--------------------------------------------------------------------------------------------------------
class LoadGraphPage5(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Load 5 Graph", font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        homeButton = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        #homeButton.pack()
        homeButton.place(relx=0, rely=0, relwidth=0.1, relheight=0.08)

        infoButton = ttk.Button(self, text="Info",
                            command=lambda: controller.show_frame(InfoPage))
        #infoButton.pack()
        infoButton.place(relx=.9, rely=0, relwidth=0.1, relheight=0.08)


        #LOAD GRAPH
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        #a.plot(timeX, load5Data)
        a.set_xlabel('Time (past 24hrs)')
        a.set_ylabel('Power')
        a.set_title('Load: ')
                    
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)

#--------------------------------------------------------------------------------------------------------
class LoadGraphPage6(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Load 6 Graph", font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        homeButton = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        #homeButton.pack()
        homeButton.place(relx=0, rely=0, relwidth=0.1, relheight=0.08)

        infoButton = ttk.Button(self, text="Info",
                            command=lambda: controller.show_frame(InfoPage))
        #infoButton.pack()
        infoButton.place(relx=.9, rely=0, relwidth=0.1, relheight=0.08)


        #LOAD GRAPH
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        #a.plot(timeX, load6Data)
        a.set_xlabel('Time (past 24hrs)')
        a.set_ylabel('Power')
        a.set_title('Load: ')
                    
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)

#--------------------------------------------------------------------------------------------------------
class LoadGraphPage7(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Load 7 Graph", font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        homeButton = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        #homeButton.pack()
        homeButton.place(relx=0, rely=0, relwidth=0.1, relheight=0.08)

        infoButton = ttk.Button(self, text="Info",
                            command=lambda: controller.show_frame(InfoPage))
        #infoButton.pack()
        infoButton.place(relx=.9, rely=0, relwidth=0.1, relheight=0.08)


        #LOAD GRAPH
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        #a.plot(timeX, load7Data)
        a.set_xlabel('Time ([ast 24hrs)')
        a.set_ylabel('Power')
        a.set_title('Load: ')
                    
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)

#--------------------------------------------------------------------------------------------------------
class LoadGraphPage8(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Load 8 Graph", font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        homeButton = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        #homeButton.pack()
        homeButton.place(relx=0, rely=0, relwidth=0.1, relheight=0.08)

        infoButton = ttk.Button(self, text="Info",
                            command=lambda: controller.show_frame(InfoPage))
        #infoButton.pack()
        infoButton.place(relx=.9, rely=0, relwidth=0.1, relheight=0.08)


        #LOAD GRAPH
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        #a.plot(timeX, load8Data)
        a.set_xlabel('Time (past 24hrs)')
        a.set_ylabel('Power')
        a.set_title('Load: ')
                    
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
#--------------------------------------------------------------------------------------------------------
class LoadPage(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Toggle Loads", font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        homeButton = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        #homeButton.pack()
        homeButton.place(relx=0, rely=0, relwidth=0.1, relheight=0.08)

        infoButton = ttk.Button(self, text="Info",
                            command=lambda: controller.show_frame(InfoPage))
        #infoButton.pack()
        infoButton.place(relx=.9, rely=0, relwidth=0.1, relheight=0.08)


        #BUTTONS FOR EACH LOAD:
        bColor1=""
        if loadValue[0] == 1:
            bColor1='green'
        else:
            bColor1='red'
        l1Button = ttk.Button(self, text="Load 1", command=lambda: publish(0))
        l1Button.place(relx=.35, rely=.3, relwidth=0.1, relheight=0.08)


        bColor2=""
        if loadValue[1] == 1:
            bColor2='green'
        else:
            bColor2='red'
        l2Button = ttk.Button(self, text="Load 2", command=lambda: publish(1))
        l2Button.place(relx=.55, rely=.3, relwidth=0.1, relheight=0.08)


        bColor3=""
        if loadValue[2] == 1:
            bColor3='green'
        else:
            bColor3='red'
        l3Button = ttk.Button(self, text="Load 3", command=lambda: publish(2))
        l3Button.place(relx=.35, rely=.4, relwidth=0.1, relheight=0.08)


        bColor4=""
        if loadValue[3] == 1:
            bColor4='green'
        else:
            bColor4='red'
        l4Button = ttk.Button(self, text="Load 4", command=lambda: publish(3))
        l4Button.place(relx=.55, rely=.4, relwidth=0.1, relheight=0.08)


        bColor5=""
        if loadValue[4] == 1:
            bColor5='green'
        else:
            bColor5='red'
        l5Button = ttk.Button(self, text="Load 5", command=lambda: publish(4))
        l5Button.place(relx=.35, rely=.5, relwidth=0.1, relheight=0.08)


        bColor6=""
        if loadValue[5] == 1:
            bColor6='green'
        else:
            bColor6='red'
        l6Button = ttk.Button(self, text="Load 6", command=lambda: publish(5))
        l6Button.place(relx=.55, rely=.5, relwidth=0.1, relheight=0.08)


        bColor7=""
        if loadValue[6] == 1:
            bColor7='green'
        else:
            bColor7='red'
        l7Button = ttk.Button(self, text="Load 7", command=lambda: publish(6))
        l7Button.place(relx=.35, rely=.6, relwidth=0.1, relheight=0.08)


        bColor8=""
        if loadValue[7] == 1:
            bColor8='green'
        else:
            bColor8='red'
        l8Button = ttk.Button(self, text="Load 8", command=lambda: publish(7))
        l8Button.place(relx=.55, rely=.6, relwidth=0.1, relheight=0.08)


#-------------------------------------------------------------------------------------------------------
class InfoPage(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Info", font = LARGE_FONT)
        label.pack(pady=10,padx=10)
        #Text on Page
        label = tk.Label(self, text="Fall 2020 - Sustainable Modular Microgrid - Spring 2021 \n \n Designed By: \n Alex Zaino \n James Woods \n Matthew Schmidt \n Ethan Gershgorin", font = LARGE_FONT)
        label.pack(side = tk.TOP, fill=tk.X, expand = True)

        #canvas = Canvas(self, width=300, height = 300)
        #canvas.pack()
        #img = ImageTk.PhotoImage(Image.open("EmbeddedImage.png"))
        #canvas.create_image(20,20, anchor=NW, image=img)
        


        homeButton = ttk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        #homeButton.pack()
        homeButton.place(relx=0, rely=0, relwidth=0.1, relheight=0.08)

        




client=mqtt.Client()
subscribe()

        
app = MainPage()
app.mainloop()
