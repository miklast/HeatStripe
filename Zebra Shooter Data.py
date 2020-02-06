import requests
import csv


baseURL = 'http://www.thebluealliance.com/api/v3/' #Makes it easier to call upon the link
header = {'X-TBA-Auth-Key':''}

s = requests.Session() #This prevents us from repeatedly opening and closing a socket + speeds it up.

def getTBA(url):
    return s.get(baseURL + url, headers=header).json()

event = input("Enter event code: ")
eventCodeLen = int(len(event)) + 1 #finds the length of the user input, and adds one to account for the underscore so any equations with it can focus solely on the changable TBA output.
matchNumbers = getTBA("event/"+ event + "/matches/keys") #grabs all matches from an event


def matchWriter(xsData, ysData, matchTime, x, matchData, alliance, matchNumber, writer):
    matchTime = round(matchTime, 1) #makes the time more readable for us/tableau
    writer.writerow([int(matchData['alliances'][alliance][x]['team_key'].strip("frc")), matchNumber, alliance, matchTime, xsData, ysData]) #writes to the CSV
    matchTime = matchTime + .1
    timeReturn = matchTime
    return timeReturn
    

def matchList():

    #matchList queries TBA for a full list of matches from an event, and finds how many total qual matches were played.

    matchMax = []
    
    for m in matchNumbers: #TBA outptuts json, this puts it into a slightly more managable list.
        print(m)
        if m[eventCodeLen:eventCodeLen + 2] == "qm":
            matchMax.append(int(m[eventCodeLen + 2:eventCodeLen + 4])) #if it has "qm", put its number into the list
        else:
            print("did nothing") #if it doesnt have QM, then it ignores it. Should be changed to nothing instead of just saying it did nothing.

    print(matchMax) #prints the list of matches, debug
    largestQualValue = int(max(matchMax)) #Grabs the largest value from the list, turns it into an integer.
    print(largestQualValue)
    return largestQualValue #total number of qual matches an event has.



def JSONToCSV():

    #JSONToCSV does as it says, takes the JSON output to a CSV file. To use with Tableau, you need an XLSX file though.
    
    qualVal = matchList() #Runs the matchList function, what it returns (largestQualValue) becomes qualVal.
    x = 0 #refers to the position of a team on an alliance. Used to cycle through each team in a match.
    alliance = "red" #Defaults to red outputs first.
     
    matchTime = 0 #defauts to 0, didnt want to try and use the JSON data times, this was easier.

    with open('ZebraData.csv', 'w', newline='') as csvFile: #creates a file named "ZebraData.cev" and starts writing to it, overwriting anything that may of been here before.
        writer = csv.writer(csvFile)
        writer.writerow(['Team', 'Match', 'Alliance', 'Time', 'X', 'Y']) #Creates the columns
        alliance = "red"

        matchNumber = 1 #We can assume all events have their first qual match as "1", so the starting value is 1. If an event differs for some reason (data didnt track that match) we can set the value using min(matchMax) over in the matchList function later.

        while matchNumber < qualVal + 1:
            print(matchNumber)#mainly to show that the code is working.
            matchData = getTBA("match/" + event + "_qm" + str(matchNumber) + "/zebra_motionworks") #calls a match.
            
            while x < 3: #if X hits 3, no team will exist, so we leave the loop

                allianceXsData = matchData['alliances'][alliance][x]
                allianceYsData = matchData['alliances'][alliance][x] #parses the JSON to find designated team

                teamXsData = allianceXsData['xs']
                teamYsData = allianceYsData['ys'] #finds the X/Y data for each team

                
                for xsData, ysData in zip(teamXsData, teamYsData): #turns nasty JSON output into something more usable
                    if type(xsData) == float: #former versions of this had a typeerror issue, this seems to fix it. Maybe because of the nulls?
                        matchTime = matchWriter(xsData, ysData, matchTime, x, matchData, alliance, matchNumber, writer)
                    elif xsData == None: #If the data is none, then its a null. Currently, its kept to preserve the data, but the main version will probably remove it.
                        xsData = "null"
                        ysData = "null"
                        matchTime = matchWriter(xsData, ysData, matchTime, x, matchData, alliance, matchNumber, writer)
                    else: #Mainly for debug. If youre hitting this, something obviously went wrong.
                        matchTime = matchTime + .1
                        print("Something was wrong with the data given.")
                        
                x = x + 1
                matchTime = 0 #these two reset for the next team to be run through.

                if x == 3 and alliance == "red":
                    alliance = "blue"
                    x = 0
                elif x == 3 and alliance == "blue":
                    alliance = "red"

                            
            x = 0
            matchTime = 0 #These two reset for the next alliance to be run though.

            matchNumber= matchNumber + 1 #These three reset for the next alliance to be run though.
        print(str(matchNumber - 1) + " matches have been saved")


def JSONToCSVAutos():

    #Takes the first 16 seconds of data (accounts for variance in start times) to look at auto paths without having to worry about the rest of the data.
    
    qualVal = matchList() #Runs the matchList function, what it returns (largestQualValue) becomes qualVal.
    x = 0 #refers to the position of a team on an alliance. Used to cycle through each team in a match.
    alliance = "red" #Defaults to red outputs first.
     
    matchTime = 0 #defauts to 0, didnt want to try and use the JSON data times, this was easier.

    with open('ZebraDataAutos.csv', 'w', newline='') as csvFile: #creates a file named "ZebraData.cev" and starts writing to it, overwriting anything that may of been here before.
        writer = csv.writer(csvFile)
        writer.writerow(['Team', 'Match', 'Alliance', 'Time', 'X', 'Y']) #Creates the columns
        alliance = "red"


        matchNumber = 1 #We can assume all events have their first qual match as "1", so the starting value is 1. If an event differs for some reason (data didnt track that match) we can set the value using min(matchMax) over in the matchList function later.

        while matchNumber < qualVal + 1:
            print(matchNumber)#mainly to show that the code is working.
            matchData = getTBA("match/" + event + "_qm" + str(matchNumber) + "/zebra_motionworks") #calls a match.
            
            while x < 3: #if X hits 3, no team will exist, so we leave the loop

                allianceXsData = matchData['alliances'][alliance][x]
                allianceYsData = matchData['alliances'][alliance][x] #parses the JSON to find designated team

                teamXsData = allianceXsData['xs']
                teamYsData = allianceYsData['ys'] #finds the X/Y data for each team

                
                for xsData, ysData in zip(teamXsData, teamYsData): #turns nasty JSON output into something more usable
                    if matchTime < 16.1:
                        if type(xsData) == float: #former versions of this had a typeerror issue, this seems to fix it. Maybe because of the nulls?
                                matchTime = round(matchTime, 1) #makes the time more readable for us/tableau
                                writer.writerow([int(matchData['alliances'][alliance][x]['team_key'].strip("frc")), matchNumber, alliance, matchTime, xsData, ysData]) #writes to the CSV
                                matchTime = matchTime + .1
                        elif xsData == None: #If the data is none, then its a null. Currently, its kept to preserve the data, but the main version will probably remove it.
                                matchTime = round(matchTime, 1)
                                writer.writerow([int(matchData['alliances'][alliance][x]['team_key'].strip("frc")), matchNumber, alliance, matchTime, "Null", "Null"])
                                matchTime = matchTime + .1
                        else: #Mainly for debug. If youre hitting this, something obviously went wrong.
                                matchTime = round(matchTime, 1)
                                matchTime = matchTime + .1
                                print("Something was wrong with the data given.")
                        
                x = x + 1
                matchTime = 0 #these two reset for the next team to be run through.

                if x == 3 and alliance == "red":
                    alliance = "blue"
                    x = 0
                elif x == 3 and alliance == "blue":
                    alliance = "red"

                            
            x = 0
            matchTime = 0 #These two reset for the next alliance to be run though.

            matchNumber= matchNumber + 1 #These three reset for the next alliance to be run though.
        print(str(matchNumber - 1) + " matches have been saved")


def findShooterSpots():
    qualVal = matchList()
    x = 0
    alliance = "red"
    matchTime = 0

    with open('ZebraShooterLocation.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['Team', 'Match', 'Alliance', 'Time', 'X', 'Y']) #Creates the columns
        alliance = "red"
        allianceSwap = 0
        matchNumber = 1
        teamPosSwap = 0

        xsTestA = 800
        xsTestB = 800
        xsTestC = 800

        ysTestA = 800
        ysTestB = 800
        ysTestC = 800

        xsRepeatTest = 300
        ysRepeatTest = 300

        while matchNumber < qualVal + 1:
            print(matchNumber)#mainly to show that the code is working.
            matchData = getTBA("match/" + event + "_qm" + str(matchNumber) + "/zebra_motionworks") #calls a match.

            while x < 3: #if X hits 3, no team will exist, so we leave the loop

                allianceXsData = matchData['alliances'][alliance][x]
                allianceYsData = matchData['alliances'][alliance][x] #parses the JSON to find designated team

                teamXsData = allianceXsData['xs']
                teamYsData = allianceYsData['ys'] #finds the X/Y data for each team
                
                counter = 0
                for xsData, ysData in zip(teamXsData, teamYsData): #turns nasty JSON output into something more usable
                    
                    xsTestC = xsTestB
                    xsTestB = xsTestA
                    xsTestA = xsData

                    ysTestC = ysTestB
                    ysTestB = ysTestA
                    ysTestA = ysData

                    if xsData == None or ysData == None or xsTestC == None or ysTestC == None:
                        counter = 0
                        matchTime = matchTime + .1

                    elif xsData - xsTestC < .15 and ysData - ysTestC < .15:
                        counter = counter + 1
                        matchTime = matchTime + .1

                        if counter == 1:
                            xsDataWrite = 3 * round(xsData/3)
                            ysDataWrite = 3 * round(ysData/3)
                            timeAtStart = matchTime
                    else:
                        counter = 0
                        matchTime = matchTime + .1

                    if counter > 35:

                        if xsRepeatTest == xsDataWrite and ysRepeatTest == ysDataWrite:
                            counter = 0
                        else:
                            writer.writerow([int(matchData['alliances'][alliance][x]['team_key'].strip("frc")), matchNumber, alliance, timeAtStart, xsDataWrite, ysDataWrite])
                            xsRepeatTest = xsDataWrite
                            ysRepeatTest = ysDataWrite

                            counter = 0
                    
                x = x + 1
                matchTime = 0 #these two reset for the next team to be run through.

                if x == 3 and alliance == "red":
                    alliance = "blue"
                    x = 0
                elif x == 3 and alliance == "blue":
                    alliance = "red"

            x = 0
            matchTime = 0 #These two reset for the next alliance to be run though.

            xsRepeatTest = 30000
            ysRepeatTest = 30000

            matchNumber= matchNumber + 1 #These three reset for the next alliance to be run though.
        print(str(matchNumber - 1) + " matches have been saved")
                        

JSONToCSV()


