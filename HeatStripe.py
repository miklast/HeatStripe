#Zebra Data parser



#Special thanks to kf#8888, hiyacynth#2841, and icecube45#8735 for their help in creating this program. 
#This would of been a pile of junk without them.



import pip._vendor.requests
import csv
from tkinter import *
from tkinter import ttk
from configparser import ConfigParser
from ctypes import windll

import settingMaker

#should fix blurry text issue?
windll.shcore.SetProcessDpiAwareness(1)

settingMaker.configSetup()

#creates the reader and locates settings.ini to read 
config = ConfigParser()
config.read('settings.ini')


baseURL = 'https://www.thebluealliance.com/api/v3/'
#Is set in the 'settings.ini' fileS
header = {'X-TBA-Auth-Key':config.get('main','TBA-KEY')}

#This prevents us from repeatedly opening and closing a socket + speeds it up.
s = pip._vendor.requests.Session()

baseGlobal = int(config.get('main', 'rounding'))
counterMaxGlobal = int(config.get('main', 'stop-time'))

def getTBA(url):
    #allows us to quickly call TBA api endpoints.
    return s.get(baseURL + url, headers=header).json()


class dataInput:

    #is constantly updated with data from the main functions so it can be written to the CSV.
    xsData = ''
    ysData = ''
    matchTime = 0
    alliance = "red"
    matchNumber = 1
    aliPos = 0


def matchWriter(dataInput, matchData, writer):

    #"cleaner" way to write to the CSV file, instead of having this everywhere.
    #Calls the dataInput class to get the specific data to write, along with matchData to get other key info along with writer to write.
    dataInput.matchTime = round(dataInput.matchTime, 1) 
    writer.writerow([int(matchData['alliances'][dataInput.alliance][dataInput.aliPos]['team_key'].strip("frc")), dataInput.matchNumber, dataInput.alliance, dataInput.matchTime, dataInput.xsData, dataInput.ysData]) #writes to the CSV
    dataInput.matchTime = dataInput.matchTime + .1
    timeReturn = dataInput.matchTime
    return timeReturn
    

def matchList(event):

    #Collects and finds the last qual match to be played.
    matches = []
    
    #cycles through every mactch in the list. If its a quals match, it gets tested to see if it was played. If it was, it gets added to the list.
    for match in getTBA("event/" + event + "/matches/simple"):
        if match['comp_level'] == "qm":
            if match['alliances']['red']['score'] == -1 or match['alliances']['red']['score'] == None:
                print("match " + str(match['match_number']) + " has not started")
            else:
                matches.append(int(match['match_number']))
    return max(matches)



def JSONToCSV(event):

    #JSONToCSV does as it says, takes the JSON output to a CSV file. To use with Tableau, you need an XLSX file though.

    #These set the class we call from, along with setting some base values for everything.

    
    print(event)
    d = dataInput()
    qualVal = matchList(event)
    d.aliPos = 0 
    d.alliance = "red" 
    d.matchTime = 0
    d.matchNumber = 1
    print("collecting match data")

    #Create a CSV file with the name based on the event given, and acts as if as its a new file, overwriting anything that may of been there before.
    with open(event + 'ZebraData.csv', 'w', newline='') as csvFile:
        #we create an easy way to write to the CSV, then define what our column names are, along with creating the column names. 
        writer = csv.writer(csvFile)
        writer.writerow(['Team', 'Match', 'Alliance', 'Time', 'X', 'Y']) 

        #while we are under the total number of quals, the script will run.
        while d.matchNumber < qualVal + 1:
            #Tells the user the match number, then grabs that specific match.
            print(d.matchNumber)
            matchData = getTBA("match/" + event + "_qm" + str(d.matchNumber) + "/zebra_motionworks") #calls a match.

            #Failsafe condition, basically if there's no Zebradata for a match we skip it.
            if matchData == None:
                print("match " + str(d.matchNumber) + " has no Zebra data, skipping.")
                d.matchNumber+=1
                continue
            
            #if aliPos hits 3, no team will exist (count from 0), so we leave the loop
            while d.aliPos < 3:
                
                #parses the JSON to find designated team, then the specific X/Y data. I could probably combine these...
                allianceXsData = matchData['alliances'][d.alliance][d.aliPos]
                allianceYsData = matchData['alliances'][d.alliance][d.aliPos]
                teamXsData = allianceXsData['xs']
                teamYsData = allianceYsData['ys'] 

                #TeamXsData and teamYsData are two long lists of data, this calls each row both the both of them.
                for xsData, ysData in zip(teamXsData, teamYsData):
                    
                    #The data (should) only be two things: a float or a null. So we check to see if its either, then write the respective code.
                    if type(xsData) == float: 
                        d.xsData = xsData
                        d.ysData = ysData
                        d.matchTime = matchWriter(d, matchData, writer)
                    elif xsData == None: 
                        d.xsData = "null"
                        d.ysData = "null"
                        d.matchTime = matchWriter(d, matchData, writer)
                    #Mainly for debug. If youre hitting this, something obviously went wrong.
                    else:
                        d.matchTime = round(d.matchTime, 1)
                        d.matchTime = d.matchTime + .1
                        print("Something was wrong with the data given.")
                        
                #We incriment the alliance posiiton then set matchTime to 0 to start next match.     
                d.aliPos = d.aliPos + 1
                d.matchTime = 0

                #logic to switch between red and blue alliances.
                if d.aliPos == 3 and d.alliance == "red":
                    d.alliance = "blue"
                    d.aliPos = 0
                elif d.aliPos == 3 and d.alliance == "blue":
                    d.alliance = "red"

            #Once all teams in a match are run through, we reset Alliance Position and time, while incrimenting the match number.                
            d.aliPos = 0
            d.matchTime = 0
            d.matchNumber= d.matchNumber + 1

        #when we're done, we tell the user its finished. Can be misleading though if some matches are skipped.    
        print(str(d.matchNumber - 1) + " matches have been saved")


def JSONToCSVAutos(event):

    #Takes the first 16 seconds of data (accounts for variance in start times) to look at auto paths without having to worry about the rest of the data.
    
    #These set the class we call from, along with setting some base values for everything.
    d = dataInput()
    qualVal = matchList(event)
    d.aliPos = 0 
    d.alliance = "red" 
    d.matchTime = 0
    d.matchNumber = 1
    print("collecting match data")

    #Create a CSV file with the name based on the event given, and acts as if as its a new file, overwriting anything that may of been there before.
    with open(event + 'ZebraDataAutos.csv', 'w', newline='') as csvFile:
        
        #we create an easy way to write to the CSV, then define what our column names are, along with creating the column names.  
        writer = csv.writer(csvFile)
        writer.writerow(['Team', 'Match', 'Alliance', 'Time', 'X', 'Y'])

        #while we are under the total number of quals, the script will run.
        while d.matchNumber < qualVal + 1:
            
            #Tells the user the match number, then grabs that specific match.
            print(d.matchNumber)
            matchData = getTBA("match/" + event + "_qm" + str(d.matchNumber) + "/zebra_motionworks") #calls a match.

            #Failsafe condition, basically if there's no Zebradata for a match we skip it.
            if matchData == None:
                print("match " + str(d.matchNumber) + " has no Zebra data, skipping.")
                d.matchNumber+=1
                continue
            
            #if aliPos hits 3, no team will exist (count from 0), so we leave the loop
            while d.aliPos < 3:
                
                #parses the JSON to find designated team, then the specific X/Y data. I could probably combine these...
                allianceXsData = matchData['alliances'][d.alliance][d.aliPos]
                allianceYsData = matchData['alliances'][d.alliance][d.aliPos]
                teamXsData = allianceXsData['xs']
                teamYsData = allianceYsData['ys']

                #TeamXsData and teamYsData are two long lists of data, this calls each row both the both of them.
                for xsData, ysData in zip(teamXsData, teamYsData):
                    if d.matchTime < 16.1:
                        #The data (should) only be two things: a float or a null. So we check to see if its either, then write the respective code.
                        if type(xsData) == float: 
                            d.xsData = xsData
                            d.ysData = ysData
                            d.matchTime = matchWriter(d, matchData, writer)
                        elif xsData == None:
                            d.xsData = "null"
                            d.ysData = "null"
                            d.matchTime = matchWriter(d, matchData, writer)
                        #Mainly for debug. If youre hitting this, something obviously went wrong.
                        else: 
                             d.matchTime = round(d.matchTime, 1)
                             d.matchTime = d.matchTime + .1
                             print("Something was wrong with the data given.")
                        
                #We incriment the alliance posiiton then set matchTime to 0 to start next match.     
                d.aliPos = d.aliPos + 1
                d.matchTime = 0

                #logic to switch between red and blue alliances.
                if d.aliPos == 3 and d.alliance == "red":
                    d.alliance = "blue"
                    d.aliPos = 0
                elif d.aliPos == 3 and d.alliance == "blue":
                    d.alliance = "red"

            #Once all teams in a match are run through, we reset Alliance Position and time, while incrimenting the match number.                
            d.aliPos = 0
            d.matchTime = 0
            d.matchNumber= d.matchNumber + 1

        #when we're done, we tell the user its finished. Can be misleading though if some matches are skipped.    
        print(str(d.matchNumber - 1) + " matches have been saved")

def findShooterSpots(event):

    global baseGlobal, counterMaxGlobal

    #These set the class we call from, along with setting some base values for everything.
    d = dataInput()
    qualVal = matchList(event)
    d.aliPos = 0 
    d.alliance = "red" 
    d.matchTime = 0
    d.matchNumber = 1
    b, c = baseGlobal, counterMaxGlobal
    base = b
    print("collecting match data")
    #counter is used to count how long we wait until we save the data. Currently, 10 equals one second.
    counter = 0
    counterMax = c

    #Create a CSV file with the name based on the event given, and acts as if as its a new file, overwriting anything that may of been there before.
    with open(event + 'ZebraShooterLocation.csv', 'w', newline='') as csvFile:

        #we create an easy way to write to the CSV, then define what our column names are, along with creating the column names.
        writer = csv.writer(csvFile)
        writer.writerow(['Team', 'Match', 'Alliance', 'Time', 'X', 'Y'])

        #while we are under the total number of quals, the script will run.
        while d.matchNumber < qualVal + 1:

            #we create an easy way to write to the CSV, then define what our column names are, along with creating the column names. 
            print(d.matchNumber)
            matchData = getTBA("match/" + event + "_qm" + str(d.matchNumber) + "/zebra_motionworks")

            #Failsafe condition, basically if there's no Zebradata for a match we skip it.
            if matchData == None:
                print("match " + str(d.matchNumber) + " has no Zebra data, skipping.")
                d.matchNumber+=1
                continue

            #super high values are put as placeholders so we dont risk them accidentally false flagging data when first called every match.
            #These variables will just play telephone with each other, checking to see if movement has happened.
            #I bet theres a better way to do this, but this was my solution.
            xsTestA = 1257
            xsTestB = 4131
            xsTestC = 15286

            ysTestA = 800
            ysTestB = 800
            ysTestC = 800

            xsRepeatTest = 300
            ysRepeatTest = 300

            #if aliPos hits 3, no team will exist (count from 0), so we leave the loop
            while d.aliPos < 3:
                
                #parses the JSON to find designated team, then the specific X/Y data. I could probably combine these...
                allianceXsData = matchData['alliances'][d.alliance][d.aliPos]
                allianceYsData = matchData['alliances'][d.alliance][d.aliPos]
                teamXsData = allianceXsData['xs']
                teamYsData = allianceYsData['ys']

                #TeamXsData and teamYsData are two long lists of data, this calls each row both the both of them.
                for xsData, ysData in zip(teamXsData, teamYsData): 

                    #Our whacky game of telephone begins, sending data up the chain to start comparing.
                    xsTestC = xsTestB
                    xsTestB = xsTestA
                    xsTestA = xsData

                    ysTestC = ysTestB
                    ysTestB = ysTestA
                    ysTestA = ysData

                    #We check if any value is null, since obviously tracking a null value shot gets us nowehere. If null, we move on.
                    if xsData == None or ysData == None or xsTestC == None or ysTestC == None:
                        counter = 0
                        d.matchTime = d.matchTime + .1

                    #We check if the data is within range, currently .15 on both X and Y axis. If it is, we start counting.
                    elif xsData - xsTestC < .15 and ysData - ysTestC < .15:
                        counter = counter + 1
                        d.matchTime = d.matchTime + .1

                        #When the counter hits one, we save the location and time,rounding it for easy tracking later. Currently, this value (bsae) is 3ft. 
                        if counter == 1:
                            xsDataWrite = base * round(xsData/base)
                            ysDataWrite = base * round(ysData/base)
                            timeAtStart = d.matchTime

                    #If the values at any point leave the .15 threshold, we reset the counter and start again.
                    else:
                        counter = 0
                        d.matchTime = d.matchTime + .1

                    #Once the counter hits the threshold, defaulting to 3.5s, we start writing.
                    if counter > counterMax:

                        #we check to make sure theyre not still in the same spot.
                        #While they may just take that long to shoot, chances are theyre instead dead on the field.
                        if xsRepeatTest == xsDataWrite and ysRepeatTest == ysDataWrite:
                            counter = 0
                        #If it doesnt match, we set the data up to be written, and reset the counter.
                        else:
                            xsRepeatTest = xsDataWrite
                            ysRepeatTest = ysDataWrite
                            d.xsData = xsDataWrite
                            d.ysData = ysDataWrite
                            d.matchTime = matchWriter(d, matchData, writer)
                            counter = 0
                    
                #We incriment the alliance posiiton then set matchTime to 0 to start next match.     
                d.aliPos = d.aliPos + 1
                d.matchTime = 0

                #logic to switch between red and blue alliances.
                if d.aliPos == 3 and d.alliance == "red":
                    d.alliance = "blue"
                    d.aliPos = 0
                elif d.aliPos == 3 and d.alliance == "blue":
                    d.alliance = "red"

            #Once all teams in a match are run through, we reset Alliance Position and time, while incrimenting the match number.                
            d.aliPos = 0
            d.matchTime = 0
            d.matchNumber= d.matchNumber + 1
        print(str(d.matchNumber - 1) + " matches have been saved")
                        

    

def guiMenu():


    mainframe = ttk.Frame(root, padding='3 3 12 12')
    #label = ttk.Label(mainframe, text='heatStripe test').grid(column=0, row = 0, padx=2, pady=2)
    eventLabel = ttk.Label(mainframe, text="Event code:").grid(column=0, row=1, padx=2,pady=2)
    fullEventButton = ttk.Button(mainframe, text='Collect Match Data', default="active", command =lambda: guiDelegator(str(guiEventName.get()), 0)).grid(column=0, row=2, padx=2, pady=2)
    autoButton = ttk.Button(mainframe, text='Collect Auto Data', default="active", command =lambda: guiDelegator(str(guiEventName.get()), 1)).grid(column=1, row=2, padx=2, pady=2)
    stopPointButton = ttk.Button(mainframe, text='Collect Stop Data', default="active", command =lambda: guiDelegator(str(guiEventName.get()), 2)).grid(column=2, row=2, padx=2, pady=2)
    eventLabel = ttk.Entry(mainframe, textvariable=str(guiEventName)).grid(column=1, row=1, padx=2, pady=3)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    

    
    root.mainloop()


def guiDelegator(eventName, commandType):
    #guiDelegator currenty does the errorhandling for the user input then delegates the tasks to the respective functions, and then sends a success or failure message based on what happens
    #Future goals include adding a progress bar, as currently there is no way for the user to tell if the program is working or completely frozen, which is not ideal.
    eventExceptionTest = "match/" + eventName + "_qm1"


    try:
        if getTBA(eventExceptionTest)['alliances']['red']['score'] == -1 or getTBA(eventExceptionTest)['alliances']['red']['score'] == None:
            g=g
    
    except:
        #Theres bound to be a way i can include this at the beginning of the function and have it work for all instances. Need to mess with that
        pop = Toplevel(root)
        photo = PhotoImage(file = "g19.png")
        pop.iconphoto(False, photo)
        errorText = ttk.Label(pop, text="No match data has been found for this event. Please double check that the event code is correct.").grid(column=0, row = 1, padx=12, pady=6)
        saveButton = ttk.Button(pop, text='Okay', default="active", command =lambda: pop.destroy()).grid(column=0, row=2, padx=2, pady=2)
        #pop.grid(column=0, row=1, padx=1, pady=1)

    else:
        matchNum = matchList(eventName)

        #match is just Python's switch function. 
        #We take the input from the gui menu and whatever # value its associated gets sent in for that command to run. Nifty and it emulates my original pipeline really well
        match commandType: 
            case 0:
                 progResp = JSONToCSV(eventName)
            case 1:
                 progResp = JSONToCSVAutos(eventName)
            case 2:
                 progResp = findShooterSpots(eventName)

        pop = Toplevel(root)
        photo = PhotoImage(file = "g19.png")
        pop.iconphoto(False, photo)
        successPopup = ttk.Label(pop, text= str(matchNum) + " matches have been saved").grid(column=0, row = 1, padx=12, pady=6)
        saveButton = ttk.Button(pop, text='Okay', default="active", command =lambda: pop.destroy()).grid(column=0, row=2, padx=2, pady=2)

        




def apiErrorGui():
    apiUserValue = StringVar()

    #Im fairly sure this is still not the "most correct" way to do this, so i should come back and clean up the popup
    mainframe = ttk.Frame(root, padding='3 3 12 12', borderwidth=5)
    apiEntryLabel = ttk.Label(mainframe, text="No TBA API Key found, please enter one below:").grid(column=0, row=0)
    saveButton = ttk.Button(mainframe, text='save', default="active", command =lambda: [settingMaker.tbaAppend(apiUserValue.get()), root.destroy()]).grid(column=2, row=2, padx=2, pady=2)
    apiUserEntry = ttk.Entry(mainframe, width=64, textvariable=str(apiUserValue)).grid(column=0, row=1)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.mainloop()




root = Tk()
root.title("HeatStripe")
guiEventName = StringVar()

photo = PhotoImage(file = "g19.png")
root.iconphoto(False, photo)


try:
    if 'Error' in getTBA('status') or header == {'X-TBA-Auth-Key':''} or header == {'X-TBA-Auth-Key':'EDIT ME!'}:
        g = g
        
except:
    
    apiErrorGui()
    
    s.close()
else:
    guiMenu()
    s.close()
