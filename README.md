# Python-ZebraDataParser
Python script that turns ZEBRA MotionWorks JSON outputs from TBA into an easily usable Excel file for use in Excel and Tableau.

## Use
This python script allows you to save the JSON ZEBRA MotionWorks outputs The Blue Alliance gives into an easily readable excel based format (CSV) for use in both in Excel and Tableau. ZEBRA MotionWorks tracking will be at over 20 events this year, so being able to make use of this data will be huge especially if you are at an event with this technology available. With Tableau, this can easily use this data to track any sort of movement on the field and take your scouting to the next level with little required work.

![](https://i.imgur.com/HNSmIwj.png)

![](https://i.imgur.com/vxVB3Zm.png)


![](https://i.imgur.com/vdvpzks.png)

![](https://i.imgur.com/vCC05gy.png)

## Install
1. Download a Python IDE and this repo. Common ones are [IDLE](https://www.python.org/), [PyCharm](https://www.jetbrains.com/pycharm/), and [Atom](https://atom.io/packages/ide-python), or you can throw it into an online compiler such as [Repl](https://repl.it/languages/python3) if you do not want to install extra programs. To get the data though, you will have to copy the output into an Excel file.

2. Add your TBA read API key. Without an API key, this program is useless. Currently this is done by editing line 15 to include your API key where it says "Edit me!" You can generate a TBA API key [here.](https://www.thebluealliance.com/account)
![Changing API key](https://i.imgur.com/oG4jWKL.gif)

3. Run the program. Make sure you know if the event has ZEBRA data and what the event code is for whatever event you are looking to find ZEBRA data for. You can see what events will have ZEBRA data for the 2020 season [here](https://www.chiefdelphi.com/t/zebra-motionworks-for-frc-2020-location-announcement/370488/38).

4. If the data is for use within Tableau, you must resave the data from a CSV file to an XLSX file to be able to connect it to Tableau. This is a current limitation of the code, and I do not currently have plans to change this for the 2020 season.

5. That's it! 

## FAQ
**Q. Why cant i do anything with it?**
A. You probably dont have an API key entered. Make sure to make a read API key with TBA, and place it in line 15 of the script. 
**Q. Entering an event tells me it hasn't started when the event has. Why is this?**
A. You must include the year within the event code. For example, if you want data from 2019 PNW District Championship, you must type "2019pncmp". You can find the event code for an event by navigating to it on [TBA](https://www.thebluealliance.com/), and looking at the URL of the event you are looking for.

![](https://i.imgur.com/J5MxE27.png)

**Q. Why does every event I enter tell me its skipping all the matches?**
A. ZEBRA MotionWorks is very new to FRC in this large of a capacity, and only 2019 Chezy Champs (2019cc) has data entered with TBA currently. As the season progresses, more events should have data to explore with. 
