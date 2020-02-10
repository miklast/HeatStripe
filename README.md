# Python-ZebraDataParser
Python script that turns ZEBRA MotionWorks JSON outputs from TBA into an easily usable Excel file for use in Excel and Tableau.

## Use
This python script allows you to save the JSON data ZEBRA MotionWorks outputs given by [The Blue Alliance](https://www.thebluealliance.com/) into an easily readable excel based format (CSV) for use in both in Excel and Tableau. ZEBRA MotionWorks tracking will be at over 20 events this year, so being able to make use of this data will be huge, especially if you are at an event with this technology available. With Tableau, you can easily use this data to track any movement on the field and take your scouting to the next level with little required work.

![](https://i.imgur.com/HNSmIwj.png)

![](https://i.imgur.com/vxVB3Zm.png)

![](https://i.imgur.com/vdvpzks.png)

![](https://i.imgur.com/vCC05gy.png)

## Install
1. Download a Python IDE and this repo. Common ones are [IDLE](https://www.python.org/), [PyCharm](https://www.jetbrains.com/pycharm/), and [Atom](https://atom.io/packages/ide-python), or you can throw it into an online compiler such as [Repl](https://repl.it/languages/python3) if you do not want to install extra programs. To get the data though, you will have to copy the output into an Excel file.

2. Add your TBA read API key. Without an API key, this program is useless. Currently, this is done by editing line 15 to include your API key where it says "Edit me!" You can generate a TBA API key [here.](https://www.thebluealliance.com/account)
![Changing API key](https://i.imgur.com/oG4jWKL.gif)

3. Run the program. Make sure you know if the event has ZEBRA data and what the event code is for whatever event you are looking to find ZEBRA data for. You can see what events will have ZEBRA data for the 2020 season [here](https://www.chiefdelphi.com/t/zebra-motionworks-for-frc-2020-location-announcement/370488/38).

4. If the data is for use within Tableau, you must resave the data from a CSV file to an XLSX file to be able to connect it to Tableau. This is a current limitation of the code, and I do not currently have plans to change this for the 2020 season.

5. That's it!

![](https://i.imgur.com/7f3uyb4.gif)

## FAQ

**Q. How is this different from Caleb's Parser?**

A. Unlike Caleb's parser, which actually parses the data, this script only transcribes the data from the JSON output into a CSV file. This means you only get the raw Zebra data to work with without any calculations run on it, outside of the stopped positions program.

**Q. Does this make use of [Caleb's zones](https://www.chiefdelphi.com/t/2020-zebra-data-parser-zones/375721)?**

While it does not in code, you can upload the zone map as a background Image in Tableau to make use of it. To add a background map in Tableau, go to Map > Background Images, and upload his map using the X and Y columns as the X and Y fields.

![Example of adding an image to a sheet](https://i.imgur.com/f8T7gXN.gif)

**Q. Why can't I do anything with it?**

A. You probably do not have a valid API key entered. Make sure to make a read API key with TBA, and place it in line 15 of the script. 

**Q. Entering an event tells me it hasn't started when the event has. Why is this?**

A. You must include the year within the event code. For example, if you want data from 2019 PNW District Championship, you must type "2019pncmp". You can find the event code for an event by navigating to it on [TBA](https://www.thebluealliance.com/), and looking at the URL of the event you are looking for.

![](https://i.imgur.com/J5MxE27.png)

**Q. Why does every event I enter tell me it's skipping all the matches?**

A. ZEBRA MotionWorks is very new to FRC in this large of a capacity, and only 2019 Chezy Champs (2019cc) has data entered with TBA currently. As the season progresses, more events should have data to explore with. 


## Future Plans
To add by week 1:

 - Delay for data writing (Caleb's currently has a 1.6s delay, im waiting until we see some 2020 data to add it. Chances are ill add it anyways pre W1 and have it editable in the settings.)
 - User settings persist when re-running code. This may limit the user to only IDLE to make full use though.
 
 To explore:
 
 - Gsheets integration. 
 - Explicit deadzones to ignore in tracking shooter locations (red is unable to shoot past its own initiation line, why bother tracking if they stopped there?
