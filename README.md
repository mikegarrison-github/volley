# volley

This is a small project written to (so far) do two things:

1) automatically generate much of the content of the PAC-12 Week X volleyball posts I have been doing for years
2) run a pablo-based monte carlo simulator of the NCAA D1 volleyball tournament in order to generate odds for teams to advance

Both applications use the pablo rating system that is published on RichKern.com

## Running The Code

To run the code:

python interface.py

## Getting The Pablo Data

To get the pablo data:

Go to the pablo rankings page on RichKern.com and save/download the page as an HTML file.

## Conference

### JSON file

To create the conference schools and schedule, edit the conf.json file (and if desired, save a copy under a different name). The list of schools is in CONFERENCE. Each school gets a "my name" that will be the display name in the output text and a "rk name" that should be the same name as is found in the pablo list from Rich Kern. The name of the key in the list should be the name used in the schedules.

The schedules are done by week. Each week is a list of dictionary objects that (so far) consist of "home", "away", and "winner". When initially creating an unplayed schedule, "winner" can be set to "" or to null (no quotes) or can be just not included.

Number of matches should be set to the expected number of matches to be played in one season by each team. (It is assumed this is the same for all teams.)

There are also some text variables that can be edited in order to customize some of the output.

### Making A Run

Check to see if the pablo data is read correctly by pushing the "Check Pablo" button.

Set the number of simulations to be run. Default is 10000. The bigger the number, the longer it will take. So if just testing, pick a small number like 100.

To run the simulations, press the "Run Conference" button.

The main output text will be in the first window. Individual match predictions will show up in the second window, in order to be pasted into the first window (or just directly pasted into the Volleytalk post).

Some of the post is not automated and will need to be edited, like the "next week" section and the link to the conference schedule.

### CONF File Editor

To make it easier to keep the conf file up-to-date with winners and losers, an automated editing program is avalable. Click the "Edit Schedule" button. A new window will open with a dropdown list for each of the weeks. Select the desired (usually most recent) week. The list of matches should show up. Select the radio button for the winner of any completed matches and then hit the "Write Data" button. This will set the "winner" variable in the JSON file with the name of the selected team.

## Tournament Simulator

Info to come later. Uses another JSON file for data.