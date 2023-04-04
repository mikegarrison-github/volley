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

Uses another JSON file for data. Two dictionaries.

One is all the schools, each of which is a dictionary with keys of "my name", "rk name", and "seed". Seed should be set to 9999 unless the team is one of the tournament seeds.

The other dictionary is the brackets, consisting of keys like "UL1" that refer to "upper left" of the NCAA bracket. Each quadrant has a 1, 2, 3, and 4 that are associated with the top four seeds in that quadrant, but the code does not actually care which is 1, which is 2, etc. That information comes from the seed in the schools data section.

### Running The Simulation

Select the number of runs (default 10000) and hit the button to run the tournament. This will take quite some time, because it will run the tournament up to 65 different ways. One run for the teams with their actual pablo ratings, and one run for each surviving team as if it had a tournament median pablo rating. (Currently hardwired to 500 runs per team, regardless of the value set for number of runs.)

Results will appear in the upper text window.

### Editing Bracket As Matches Are Played

An editor is available. Click on the box and get a dropdown list of the 16 subregionals (UL1, UL2, etc.). Select one. Four lines will appear.

To indicate that a team has won, click its name. To indicate that a team has lost, click "Newly Defeated". Previously defeated teams will just show up in the list as "Defeated", and this will already be pre-selected. (There is no way to "undefeat" a team other than opening up the JSON file and editing it that way.) When the winning and/or losing teams have been selected, click the write button.

Note that after the first two rounds have been played, each subregional list will contain at most one team, so you will have to find the losing team by going back to the dropdown and pulling up a different subregional quad. (It is not actually necessary to indicate a team as the winner if it is the only one still remaining in the subregion. It is only necessary to remove losers by clicking them as "Newly Defeated" and then writing the data to the JSON file.)