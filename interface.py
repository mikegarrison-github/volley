import conference as conf
import tournament as tourn
import random
from tkinter import *
import statistics
from classes import Team,PabloWeeklyRating
import json




def open_conf_sched(root,conf_file) -> None:
    # create new window object subordinate to the main window (root)
    window = Toplevel(root)
    answer_frame = Frame(window, width =10, height =10)
    answer_frame.grid(row=21)

    def match_boxes(*args) -> None:
        week = str(clicked.get())
        matches = conf_data["CONF_SCHED"].get(week,[])
        count = 0
        for widget in answer_frame.winfo_children():
            widget.destroy()
        for match in matches:
            count +=1
            brow = 20+count
            match.append(StringVar())
            home_team = match[1]
            if home_team == "Defeated":
                ht_name = "Defeated"
            else:
                ht_name = conf_data["CONFERENCE"][home_team]["my name"]
            Radiobutton(answer_frame,text=ht_name,value=home_team,variable=match[2]).grid(row=brow,column=1)
            visiting_team = match[0]
            if visiting_team == "Defeated":
                vt_name = "Defeated"
            else:
                vt_name = conf_data["CONFERENCE"][visiting_team]["my name"]
            Radiobutton(answer_frame,text=vt_name,value=visiting_team,variable=match[2]).grid(row=brow,column=0)
        def write_data(*args) -> None:
            out_list = []
            for match in matches:
                if match[0] == match[2].get():
                    out_list.append([match[0],"Defeated"])
                elif match[1] == match[2].get():
                    out_list.append(["Defeated",match[1]])
                else:
                    out_list.append([match[0],match[1]])
            conf_data["CONF_SCHED"][week]=out_list
            json_out = json.dumps(conf_data,indent=4)
            with open(conf_file, "w") as outfile:
                outfile.write(json_out)

        
        # create a write data button
        Button(answer_frame,text="Write Data",command=write_data).grid(row=90)


    # open json file and read in conference data
    F = open(conf_file)
    conf_data = conf.read_conference_data(F)
    F.close

    # week_select dropdown
    options = list(conf_data["CONF_SCHED"].keys())
    clicked = StringVar()
    clicked.set("1")
    OptionMenu(window,clicked,*options).grid(row=20)
    clicked.trace_add("write",match_boxes)

    # create a window close button
    Button(window,text="Close",command=window.destroy).grid(row=100)

    #activate window (until it is closed)
    window.grab_set()

    # END OPEN CONF SCHEDULE FUNCTION (return None) (ends when window is closed)






def run_conference(runs_value,text,text2,conf_file="conf.json",pablo_file=None) -> None:
    
    # check/set number of runs for monte carlo simulation (defaut 10000)
    try:
        number_of_runs = int(runs_value.get())
    except:
        number_of_runs = 10000
        runs_value.set("10000")
    
    # get conference data from json file
    F = open(conf_file)
    conf_data = conf.read_conference_data(F)
    F.close
    number_of_matches = conf_data["NUMBER_OF_MATCHES"]

    # seed random number generator
    random.seed()

    # get data from pablo file and create pablo data object
    if pablo_file:
        pablo_data = PabloWeeklyRating(pablo_file)
    else:
        pablo_data = PabloWeeklyRating()
    
    # get current records
    results_table = []
    current_results=conf.find_current_records(number_of_matches,conf_data)
    for school in current_results:
        team = Team(school)
        team.load_from_dict(conf_data["CONFERENCE"])
        team.find_pablo(pablo_data)
        current_results[school]["rank"] = team.rank
        current_results[school]["rating"]= team.rating
        wins = current_results[school]["wins"]
        losses = current_results[school]["losses"]
        percentage = float(wins)/float(wins + losses)
        results_table.append([team.rank,team.my_name,wins,losses,percentage])

    # sort results table by percentage, rank, name
    results_table.sort(key=lambda entry: entry[1])
    results_table.sort(key=lambda entry: entry[0])
    results_table.sort(reverse=True,key=lambda entry: entry[4])

    #start building out_string with header and current standings table
    out_string = '''All discussion about the PAC-12 is welcome (except for trolling and flamebaiting)

==================

[font color="red"]NOTE: All references to rankings in this post are based on pablo, not AVCA![/font]

Standings:\n\n'''
    for school in results_table:
        out_string += "("+str(school[0])+") "+str(school[1])+" "+str(school[2])+"-"+str(school[3])+"\n"
    out_string += "\n("+str(pablo_data.pablo_date)+" pablo rankings)\n\n==================\n\n"

    # build expected wins table
    out_string += "Expected wins as of "+str(pablo_data.pablo_date)+"\n\n"
    # actually generate expected wins as final_results dict
    for school in conf_data["CONFERENCE"]:
        team = Team(school)
        team.load_from_dict(conf_data["CONFERENCE"])
        current_results[school]["expected wins"]=[]
        current_results[school]["expected placements"]=[]
    current_results["Defeated"]={"rating":-9999}
    final_results = conf.run_conference(number_of_runs,number_of_matches,current_results,pablo_data,conf_data)
    del final_results["Defeated"]
    # now sort final results by mean expected wins, pablo rating, name
    sorted_list_of_schools = sorted(conf_data["CONFERENCE"].keys())
    _pablo = {}
    for school in sorted_list_of_schools:
        _pablo[school] = final_results[school]["rating"]
    pablo_sorted_list = [x for (x,y) in sorted(_pablo.items(), key=lambda item: item[1], reverse=True)]
    _wins = {}
    for school in pablo_sorted_list:
        _wins[school] = statistics.mean(final_results[school]["expected wins"])
    wins_sorted_list = [x for (x,y) in sorted(_wins.items(), key=lambda item: item[1], reverse=True)]
    # build string
    for school in wins_sorted_list:
        wins = final_results[school]["expected wins"]
        mean_wins = statistics.mean(wins)
        median_wins = statistics.median(wins)
        std_wins = statistics.stdev(wins)
        maximum_possible_wins = final_results[school]["wins"] + final_results[school]["unplayed"]
        minimum_possible_wins = final_results[school]["wins"]
        high_wins = sorted([mean_wins+std_wins,minimum_possible_wins,maximum_possible_wins])[1]
        low_wins = sorted([mean_wins-std_wins,minimum_possible_wins,maximum_possible_wins])[1]
        display_name = conf_data["CONFERENCE"][school]["my name"]
        out_string += str(display_name)+" "+str(round(high_wins,1))+" to "+str(round(low_wins,1))+" -- median wins: "+str(round(median_wins))+"\n"
    
    # build expected placements table
    out_string += "\n==================\n\nExpected placement as of "+str(pablo_data.pablo_date)+"\n\n"
    for school in wins_sorted_list:
        number_of_teams = len(conf_data["CONFERENCE"])
        placements = final_results[school]["expected placements"]
        mean_placements = statistics.mean(placements)
        median_placements = statistics.median(placements)
        std_placements = statistics.stdev(placements)
        high_placements = sorted([mean_placements+std_placements,1,number_of_teams])[1]
        low_placements = sorted([mean_placements-std_placements,1,number_of_teams])[1]
        display_name = conf_data["CONFERENCE"][school]["my name"]
        out_string += str(display_name)+" "+str(round(low_placements,1))+" to "+str(round(high_placements,1))+" -- median placement: "+str(round(median_placements))+"\n"
    
    # build remaining text (will be edited by hand cut/paste from second text box)
    out_string += "\n==================\n\nThis week's matches (Pacific times)\n\n"
    out_string += '''Thur:
[font color="19d2e6"]7:00pm[/font] 

Fri:
[font color="19d2e6"]7:00pm[/font] 

Sat:
[font color="19d2e6"]noon[/font] 

Sun:
[font color="19d2e6"]11:00am[/font] 

==================

[font color="gold"]Pablo highlight matches of the week (top-25 pablo matchups):[/font]

None

==================

[font color="red"]Pablo close matches of the week (55 percent or closer):[/font]

None

==================

Next week:

Mountains @ BayArea, Washington @ Oregon, Arizona @ LA

===================

Conference schedule link:

https://pac-12.com/womens-volleyball/schedule/

Pablo is the creation of @pablo and is available by subscription on richkern.com'''
    
    # insert into first text box
    text.delete("1.0","end")
    text.insert("1.0",out_string)
    
    # make match lines and insert into second text box (for copy/paste into first text box)
    match_string = conf.make_schedules_and_odds(current_results,pablo_data,conf_data)
    text2.delete("1.0","end")
    text2.insert("1.0",match_string)

    # END RUN CONFERENCE FUNCTION (return None)





def main():
    root = Tk()

    # set some things that will be used elsewhere
    pablo_date=StringVar(root,"no pablo data")
    hca=IntVar(root,0)
    runs_value = StringVar(root,"10000")
    conf_file = 'conf.json'
    pablo_file = None

    # test pablo inner function
    def test_pablo(*args):
        if pablo_file:
            pablo_data = PabloWeeklyRating(pablo_file)
        else:
            pablo_data = PabloWeeklyRating()
        hca.set(pablo_data.hca)
        pablo_date.set(pablo_data.pablo_date)

    # Construct root window
    #labels
    Label(root, text="Mike's Volleytalk pablo control panel").grid(row=0,columnspan=99)
    Label(root,text="Output:").grid(row=15,column=0)
    Label(root,text="Pablo Date:").grid(row=1,column=0)
    Label(root,textvariable=pablo_date).grid(row=1,column=1)
    Label(root,text="HCA:").grid(row=2,column=0)
    Label(root,textvariable=hca).grid(row=2,column=1)
    Label(root,text="If the date and HCA apprear to be valid:").grid(row=4,columnspan=2)
    Label(root,text="Number of runs:").grid(row=5,column=0)
    # text and entry boxes
    text = Text(root,width=100,height=25)
    text.grid(row=16,columnspan=99)
    text2 = Text(root,width=100,height=25)
    text2.grid(row=18,columnspan=99)
    runs = Entry(root,textvariable=runs_value)
    runs.grid(row=5, column=1)
    # buttons
    Button(root,text="Check Pablo",command=test_pablo).grid(row=3,columnspan=2)
    Button(root,text="Run Conference",command=lambda: run_conference(runs_value,text,text2,conf_file)).grid(row=6,columnspan=2)
    Button(root,text="Edit Schedule",command=lambda: open_conf_sched(root,conf_file)).grid(row=6,column=2)

    root.mainloop()

    # END MAIN FUNCTION (return None, program will end when mainloop ends)






if __name__ == "__main__":
    main()
