
<p align="center">
  <img src="https://i.imgur.com/nlQeJZD.png" />
</p>

# Heatstripe
Quickly download and play with ZEBRA Motionworks data in a simple and usable format.

## Use
This program allows you to save the JSON data ZEBRA MotionWorks outputs given by [The Blue Alliance](https://www.thebluealliance.com/) into an easily readable excel based format (CSV) for use in both in Excel and Tableau. ZEBRA MotionWorks tracking will be at over 10 events this year, so being able to make use of this data will be huge, especially if you are at an event with this technology available. With Tableau, you can easily use this data to track any movement on the field and take your scouting to the next level with little required work.

![](https://i.imgur.com/HNSmIwj.png)

![](https://i.imgur.com/vxVB3Zm.png)

![](https://i.imgur.com/vdvpzks.png)

![](https://i.imgur.com/vCC05gy.png)

## Install
1. Download the latest version of Python. This program only works on Python 3.10 and above.

2. Download and extract the program.

3. Generate a TBA API key. This is used to access data from The Blue Alliance. You can generate a TBA API key [here.](https://www.thebluealliance.com/account)

3. Run the program. The first time setup will have you enter your API key. You will need to run the program a 2nd time to have the changes save fully.

4. If the data is for use within Tableau, you must resave the data from a CSV file to an XLSX file to be able to connect it to Tableau. Tableau does not like large CSV files and will refuse to run properly with them.

## FAQ

**Q. How do I add the field image in Tableau?**

 To add a background map in Tableau, go to Map > Background Images, and upload a field image using the X and Y columns as the X and Y fields.

![Example of adding an image to a sheet](https://i.imgur.com/f8T7gXN.gif)

You can find high quality field photos for the 2022 season in this [Chief Delphi thread](https://www.chiefdelphi.com/t/2022-top-down-field-renders/399031?u=miklast). Use the photo with the prefix "cropped" for the best results.

## Thanks

These people helped make this project possible:



| <a href="https://github.com/icecube45" target="_blank">**Icecube45**</a> | <a href="https://github.com/MC42" target="_blank">**MC42**</a> | <a href="https://github.com/octocynth" target="_blank">**octocynth**</a> |
| :---: |:---:| :---:|
| [![Icecube45](https://avatars3.githubusercontent.com/u/1614007?&s=200)](https://github.com/icecube45)    | [![MC42](https://avatars3.githubusercontent.com/u/6531081?&s=200)](https://github.com/MC42) | [![octocynth](https://avatars1.githubusercontent.com/u/8210419?s=200)](https://github.com/octocynth)  |
| <a href="http://github.com/icecube45" target="_blank">`github.com/icecube45`</a> | <a href="https://github.com/MC42" target="_blank">`github.com/MC42`</a> | <a href="https://github.com/octocynth" target="_blank">`github.com/octocynth`</a> |
