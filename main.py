# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 09:24:14 2022

@author: seg faults
"""

import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
    )


#main window
w = tk.Tk()

#change frames based on if the building type changes
def change_frames(*args):
    
    if len(w.winfo_children()) > 1:
        building_frame(w.winfo_children()[1])
        energy_frame(w.winfo_children()[2])
        time_frame(w.winfo_children()[3])

    
    return

class Display:
    
    def __init__(self):
        
        self.btype = tk.StringVar()
        #change the variables if the building type changes
        self.btype.trace('w', change_frames)
        self.building = tk.StringVar()
        self.energy = tk.StringVar()
        self.time = tk.StringVar()
        self.dorm = None
        self.non_dorm = None
        self.weather = None
        self.data_used = None
        
        self.btype.set('Dorm')
        self.building.set('Busch')
        self.energy.set('Steam')
        self.time.set('Yearly')
        
        return
    
#class of common values
d = Display()

#load data
d.dorm = pd.read_csv('C:\\Users\\Owner\\Documents\\HackOHIO\\HackOhio22-main\\HackOhio22-main\\Dorm Buildings.csv')
d.non_dorm = pd.read_csv('C:\\Users\\Owner\\Documents\\HackOHIO\\HackOhio22-main\\HackOhio22-main\\Non-Dorm Buildings.csv')
d.weather = pd.read_csv('C:\\Users\\Owner\\Documents\\HackOHIO\\HackOhio22-main\\HackOhio22-main\\Weather Data.csv')

#remove null columns
#dorm = df_dorm.dropna(axis=1)
#non_dorm = df_non_dorm.dropna(axis=1)
#weather = df_weather.dropna(axis=1)

#make scatter plots
x = d.dorm.loc[:,'Series Name']
y = d.dorm.loc[:,'Busch House - Electricity Consumption (kBTU)']



#holds all the rows of Series Name. 
seriesName = list(d.dorm['Series Name'])
month = [] #string of all the months
day = [] #
year = [] #list
#year = {} #dictionary (map)
time = []
yearMonths = []


def yearsInData(v):
    #    2017-01-01T05:00:00

    for i in range(len(v)):
        y = v[i][0:4] #"2017"
        if y not in year: year.append(y)
        # print (type (year))
        # print("year modified: ", year)
yearsInData(seriesName)

#gives all the dates in the each year
def allDatesInAYear(v, y):
    yearTwo = []
    for i in range(len(v)):
        if (seriesName[i][0:4] == y):
            yearTwo.append(seriesName[i][0:18])
    return yearTwo



# print(year[0])

for i in range(len(year)):
    x = []
    x = allDatesInAYear(seriesName, year[i])
    # print ("Dates in a year: ", x)
    yearMonths.append(x)



monthsInYear = [] #holds the months in a year. 

for i in range(0, len(yearMonths)):
    months = [] #holds all the month in 2017
    for j in range(0, len(yearMonths[i])):
        # print (yearMonths[i][j]) #2017 ---- till end of 2017 
        x = yearMonths[i][j][5:7] #"01" 5:7
        if x not in months: months.append(x)
    monthsInYear.append(months)

print(monthsInYear[5]) #all the months in 2017 monthsInYear


def type_frame(frame):
    
    options = [
        'Dorm',
        'Non-Dorm'
        ]
    d.btype.set(options[0])
    lbl = tk.Label(frame, text='Building Type:')
    ent = tk.OptionMenu(frame, d.btype, *options)
    lbl.grid(row=0, column=0)
    ent.grid(row=0, column=1)
    
    return

def building_frame(frame):
    
    options = None
    
    if d.btype.get() == 'Dorm':
        #get all dorm names
        options = [
            'Baker Hall',
            'Busch House',
            'Morrill, Justin S, Tower',
            'Smith-Steeb Hall',
            'Taylor Tower'
            ]
    elif d.btype.get() == 'Non-Dorm':
        #get all non-dorm names
        options = [
            'Denney, Joseph Villiers, Hall',
            'Enarson, Harold L, Classroom Building',
            'Knowlton, Austin E, Hall',
            'North Recreation Center',
            'Thompson, William Oxley, Memorial Library',
            ]
    d.building.set(options[0])
    lbl = tk.Label(frame, text='Building:')
    ent = tk.OptionMenu(frame, d.building, *options)
    lbl.grid(row=0, column=0)
    ent.grid(row=0, column=1)
    
    return

def energy_frame(frame):
    
    options = [
        'Steam Consumption (kBTU)',
        'Electricity Consumption (kBTU)',
        'Chilled Water Consumption (kBTU)',
        'Hot Water Consumption (kBTU)',
        'Natural Gas Consumption (kBTU)',
        'Total Energy Consumption (Cleaned) (kBTU)'
        ]
    d.energy.set(options[0])
    lbl = tk.Label(frame, text='Energy:')
    ent = tk.OptionMenu(frame, d.energy, *options)
    lbl.grid(row=0, column=0)
    ent.grid(row=0, column=1)
    
    return

def time_frame(frame):
    
    options = [
        'Yearly',
        'Monthly',
        'Daily'
        ]
    d.time.set(options[0])
    lbl = tk.Label(frame, text='Time:')
    ent = tk.OptionMenu(frame, d.time, *options)
    lbl.grid(row=0, column=0)
    ent.grid(row=0, column=1)
    
    return

def get_building_name():
    
    data = None
    if d.btype.get() == 'Dorm':
        data = d.dorm
    else:
        data = d.non_dorm
    
    n = data.filter(like=d.building.get())
    x = data.loc[:, 'Series Name']
    d.data_used = n.merge(x, left_index=True, right_index=True)
    
    return

def get_energy():
    
    n = d.data_used.filter(like=d.energy.get())
    x = d.data_used.loc[:, 'Series Name']
    d.data_used = n.merge(x, left_index=True, right_index=True)
    
    return
        
def yearly_data():
    
    years = {}
    
    #iterate over data
    for i in d.data_used.index:
        
        #get the year
        y = d.data_used['Series Name'][i][:4]
        if y in years:
            data = d.data_used[d.building.get() + ' - ' + d.energy.get()][i]
            d_original = years[y]['data']
            num = years[y]['number'] + 1
            years[y] = {'data':(d_original + data), 'number':num}
        else:
            years[y] = {'data':d.data_used[d.building.get() + ' - ' + d.energy.get()][i], 'number': 1}
                    
    #take averages
    for year in years:
        avg = years[year]['data'] / years[year]['number']
        years[year]['data'] = avg
    
    return years

def monthly_graph():
    
    months = {}
    
    #iterate over data
    for i in d.data_used.index:
        
        #get the year
        m = d.data_used['Series Name'][i][5:7]
        if m in months:
            data = d.data_used[d.building.get() + ' - ' + d.energy.get()][i]
            d_original = months[m]['data']
            num = months[m]['number'] + 1
            months[m] = {'data':(d_original + data), 'number':num}
        else:
            months[m] = {'data':d.data_used[d.building.get() + ' - ' + d.energy.get()][i], 'number': 1}
                    
    #take averages
    for month in months:
        avg = months[month]['data'] / months[month]['number']
        months[month]['data'] = avg
    
    return months
    
def daily_graph():
    
    days = {}
    
    #iterate over data
    for i in d.data_used.index:
        
        #get the year
        y = d.data_used['Series Name'][i][11:]
        if y in days:
            data = d.data_used[d.building.get() + ' - ' + d.energy.get()][i]
            d_original = days[y]['data']
            num = days[y]['number'] + 1
            days[y] = {'data':(d_original + data), 'number':num}
        else:
            days[y] = {'data':d.data_used[d.building.get() + ' - ' + d.energy.get()][i], 'number': 1}
                    
    #take averages
    for day in days:
        avg = days[day]['data'] / days[day]['number']
        days[day]['data'] = avg
    
    return days

def x_and_y(dic):
    
    x = []
    y = []
    for k in dic:
        x.append(k)
        y.append(dic[k]['data'])
    
    return x, y

def plot(x, y, w, title, x_label):
    
    fig = plt.figure(figsize=(20, 10))
    fig.add_subplot(111).plot(x, y, 'r')
    
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel('kBTU')
    
    can = FigureCanvasTkAgg(fig, master=w)
    can.draw()
    can.get_tk_widget().grid(row=0, column=0, sticky='nesw')
    
    t = NavigationToolbar2Tk(can, w, pack_toolbar=False)
    t.update()
    t.grid(row=1, column=0, sticky='ew')
    
    
    return

#make graphs of the data
def graphs():
    
    #isolate the building and energy
    get_building_name()
    get_energy()
    
    win = tk.Toplevel()
    
    #make different graphs for different topics
    if d.time.get() == 'Yearly':
        
        year_dic = yearly_data()
        #get x and y
        x_axis, y_axis = x_and_y(year_dic)
        #plot
        plot(x_axis, y_axis, win, (d.building.get() + ' - ' + d.energy.get()), 'Year')
                
    elif d.time.get() == 'Monthly':
        
        month_dic = monthly_graph()
        #get x and y
        x_axis, y_axis = x_and_y(month_dic)
        #plot
        plot(x_axis, y_axis, win,(d.building.get() + ' - ' + d.energy.get()), 'Month')
        
    elif d.time.get() == 'Daily':
        
        day_dic = daily_graph()
        #get x and y
        x_axis, y_axis = x_and_y(day_dic)
        #plot
        plot(x_axis, y_axis, win,(d.building.get() + ' - ' + d.energy.get()), 'Hour')
    
    return

#add frames
def init_frames(window):
    
    #dropdown menu frames
    for i in range(4):
        frm = tk.Frame(window)
        frm.grid(row=i, column=0, sticky='nws')
        #fill based on i
        if i == 0:
            type_frame(frm)
        elif i == 1:
            building_frame(frm)
        elif i == 2:
            energy_frame(frm)
        elif i == 3:
            time_frame(frm)
        
    #button
    btn = tk.Button(window, text='Get graphs', command=graphs)
    btn.grid(row=4, column=1)
    
    return

init_frames(w)

w.mainloop()