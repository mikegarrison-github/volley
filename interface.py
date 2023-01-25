import conference as conf
import pablo
import tournament as tourn
import random
from tkinter import *
import statistics


def test_pablo(pablo_date=None,hca=None) -> tuple[dict,int,str]:
    pablo_dict, hca_called, pablo_date_called = pablo.read_pablo_data()
    pablo_date.set(pablo_date_called)
    hca.set(hca_called)

def run_conference(runs_value,text,text2,conf_file) -> None:
    try:
        number_of_runs = int(runs_value.get())
    except:
        number_of_runs = 10000
        runs_value.set("10000")
    F = open(conf_file)
    conf_data = conf.read_conference_data(F)
    number_of_matches = conf_data["NUMBER_OF_MATCHES"]
    random.seed()
    pablo_dict, hca, pablo_date = pablo.read_pablo_data()
    # get current records
    results_table = []
    current_results=conf.find_current_records(number_of_matches,conf_data)
    for school in current_results:
        rk_name = conf_data["CONFERENCE"][school]["rk name"]
        pablo_rank = pablo_dict[rk_name]["rank"]
        current_results[school]["rank"] = pablo_rank
        my_name = conf_data["CONFERENCE"][school]["my name"]
        wins = current_results[school]["wins"]
        losses = current_results[school]["losses"]
        percentage = float(wins)/float(wins + losses)
        results_table.append([pablo_rank,my_name,wins,losses,percentage])
    # sort by percentage, rank, name
    results_table.sort(key=lambda entry: entry[1])
    results_table.sort(key=lambda entry: entry[0])
    results_table.sort(reverse=True,key=lambda entry: entry[4])
    out_string = '''All discussion about the PAC-12 is welcome (except for trolling and flamebaiting)

==================

[font color="red"]NOTE: All references to rankings in this post are based on pablo, not AVCA![/font]

Standings:\n\n'''
    for school in results_table:
        out_string += "("+str(school[0])+") "+str(school[1])+" "+str(school[2])+"-"+str(school[3])+"\n"
    out_string += "\n("+str(pablo_date)+" pablo rankings)\n\n==================\n\n"
    out_string += "Expected wins as of "+str(pablo_date)+"\n\n"
    # calculate expected wins
    for school in conf_data["CONFERENCE"]:
        rk_name = conf_data["CONFERENCE"][school]["rk name"]
        rating = pablo_dict[rk_name]["rating"]
        current_results[school]["rating"]=rating
        current_results[school]["expected wins"]=[]
        current_results[school]["expected placements"]=[]
    current_results["Defeated"]={"rating":-9999}
    final_results = conf.run_conference(number_of_runs,number_of_matches,current_results,hca,conf_data)
    del final_results["Defeated"]
    # now sort by expected wins, pablo rating, name
    sorted_list_of_schools = sorted(conf_data["CONFERENCE"].keys())
    _pablo = {}
    for school in sorted_list_of_schools:
        _pablo[school] = final_results[school]["rating"]
    pablo_sorted_list = [x for (x,y) in sorted(_pablo.items(), key=lambda item: item[1], reverse=True)]
    _wins = {}
    for school in pablo_sorted_list:
        _wins[school] = statistics.mean(final_results[school]["expected wins"])
    wins_sorted_list = [x for (x,y) in sorted(_wins.items(), key=lambda item: item[1], reverse=True)]
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
    out_string += "\n==================\n\nExpected placement as of "+str(pablo_date)+"\n\n"
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
    text.delete("1.0","end")
    text.insert("1.0",out_string)
    match_string = conf.make_schedules_and_odds(current_results,hca,conf_data)
    text2.delete("1.0","end")
    text2.insert("1.0",match_string)

def main():
    root = Tk()
    pablo_date=StringVar(root,"no pablo data")
    hca=IntVar(root,0)
    conf_file = 'conf.json'

# label
    Label(root, text="Mike's Volleytalk pablo control panel").grid(row=0,columnspan=99)
    Label(root,text="Output:").grid(row=15,column=0)
    text = Text(root,width=100,height=25)
    text.grid(row=16,columnspan=99)
    text2 = Text(root,width=100,height=25)
    text2.grid(row=18,columnspan=99)
    Label(root,text="Pablo Date:").grid(row=1,column=0)
    Label(root,textvariable=pablo_date).grid(row=1,column=1)
    Label(root,text="HCA:").grid(row=2,column=0)
    Label(root,textvariable=hca).grid(row=2,column=1)
    Button(root,text="Check Pablo",command=lambda: test_pablo(pablo_date,hca)).grid(row=3,columnspan=2)
    Label(root,text="If the date and HCA apprear to be valid:").grid(row=4,columnspan=2)
    Label(root,text="Number of runs:").grid(row=5,column=0)
    runs_value = StringVar(root,"10000")
    runs = Entry(root,textvariable=runs_value)
    runs.grid(row=5, column=1)
    Button(root,text="Run Conference",command=lambda: run_conference(runs_value,text,text2,conf_file)).grid(row=6,columnspan=2)

    root.mainloop()


if __name__ == "__main__":
    main()
