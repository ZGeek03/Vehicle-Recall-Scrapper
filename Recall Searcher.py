# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 14:33:30 2022

@author: Soccerguy03
"""
from requests import get
import PySimpleGUI as sg

cancelled = False




#if make is unconventional
def convertMake(make):
    if "mercedes" in make.lower():
        return "mercedes-benz"
    elif "chevy" in make.lower() or "chevrolet" in make.lower():
        return "chevrolet"
    else:
        return make
    


while cancelled == False:
    layoutMain = [
        [sg.Text("Enter Vehicle Details Below.")],
        [sg.Text("Make:"), sg.InputText(size=(30, 3), border_width=0)],
        [sg.Text("Model:"), sg.InputText(size=(30, 3), border_width=0)],
        [sg.Text("Year:"), sg.InputText(size=(30, 3), border_width=0)],
        [sg.Submit(), sg.Button("Cancel")]
        ]
    window = sg.Window("Recall Searcher", layoutMain)
    while True:
        event, userVals = window.read(timeout=10)
        if event in ("Cancel", sg.WIN_CLOSED):
            print("Cancelled by user")
            cancelled = True
            break
        if event == "Submit":
            break
        
    window.close() #die
    if userVals[0] == "" or userVals[1] == "" or userVals[0] == "":
        if cancelled == False:
            oopsLayout = [
                [sg.Text("It looks like you forgot some information!")],
                [sg.Button("ok")]
                ]
            window = sg.Window("Oops!", oopsLayout)
            while True:
                event, userVals = window.read(timeout=10)
                if event in ("ok", sg.WIN_CLOSED):
                    print("Search started over.")
                    break
            window.close()
    else:
        vehicleMake = userVals[0]
        vehicleModel = userVals[1]
        vehicleYear = userVals[2]
        url = "https://api.nhtsa.gov/recalls/recallsByVehicle?make=" + convertMake(vehicleMake) + "&model=" + vehicleModel + "&modelYear=" + vehicleYear
            
        
        #https://api.nhtsa.gov/products/vehicle/models?modelYear=2019&make=mercedes-benz&issueType=r
        response = get(url)
        
        jsonData = response.json()
        
        recallTree = []
        recallDateSelected = ""
        
        for i in jsonData["results"]:
            recallTree.append(i["ReportReceivedDate"])
        
        text = "Current and Past Recalls on your " + vehicleYear + " " + vehicleMake + " " + vehicleModel
        resultsLayout = [
            [sg.Text(text)],
            [sg.Listbox(recallTree, size=(75, 35))],
            [sg.Submit("Open Recall", key="open_details"), sg.Button("Close")]
            ]
        window = sg.Window("Recall Searcher", resultsLayout)
        while True:
            event, userVals = window.read()
            if event in ("Close", sg.WIN_CLOSED):
                print("Search Restarted.")
                break
            if event == "open_details":
                for i in jsonData["results"]:
                    if i["ReportReceivedDate"] == userVals[0][0]:
                        recallDateSelected = i
                recallLayout = [
                    [sg.Text("Component: "+ recallDateSelected["Component"])],
                    [sg.Text("Summary: " + recallDateSelected["Summary"], size=(50, 7))],
                    [sg.Text("Notes: " + recallDateSelected["Notes"], size=(50, 7))],
                    [sg.Text("Remedy: " + recallDateSelected["Remedy"], size=(50, 7))],
                    [sg.Button("Close")]
                    ]
                recallWindow = sg.Window(recallDateSelected["ReportReceivedDate"], recallLayout)
                while True:
                    event, recallVals = recallWindow.read()
                    if event in ("Close", sg.WIN_CLOSED):
                        print("Recall Detail Window Closed.")
                        break
                recallWindow.close()
        window.close()