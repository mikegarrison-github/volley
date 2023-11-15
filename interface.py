import conference as conf
import tournament as tourn
import random
from tkinter import *
import statistics
from classes import Team,PabloWeeklyRating
import json
from scipy import stats as SPstats




def open_conf_sched(root,conf_file) -> None:
    # create new window object subordinate to the main window (root)
    window = Toplevel(root)
    answer_frame = Frame(window, width =10, height =10)
    answer_frame.grid(row=21)

    def match_boxes(*args) -> None:
        week = str(clicked.get())
        matches = conf_data["CONF_SCHED"].get(week,[])
        count = 0
        homes = []
        aways = []
        selections = []
        for widget in answer_frame.winfo_children():
            widget.destroy()
        for match in matches:
            brow = 21+count
            selections.insert(count,StringVar())
            home_team = Team(match.get("home"))
            home_team.load_from_dict(conf_data["CONFERENCE"])
            ht_name = home_team.my_name
            homes.insert(count,ht_name)
            visiting_team = Team(match.get("away"))
            visiting_team.load_from_dict(conf_data["CONFERENCE"])
            vt_name = visiting_team.my_name
            aways.insert(count,vt_name)
            current_winner = match.get("winner")
            Radiobutton(answer_frame,text=ht_name,value=home_team.name,variable=selections[count]).grid(row=brow,column=1)
            Radiobutton(answer_frame,text=vt_name,value=visiting_team.name,variable=selections[count]).grid(row=brow,column=0)
            if current_winner:
                selections[count].set(current_winner)
            count +=1
        def write_data(*args) -> None:
            out_list = []
            for i in range(count):
                match = matches[i]
                selected_winner = selections[i].get()
                match["winner"] = selected_winner
                out_list.append(match)
            conf_data["CONF_SCHED"][week]=out_list
            json_out = json.dumps(conf_data,indent=4)
            with open(conf_file_name, "w") as outfile:
                outfile.write(json_out)

        
        # create a write data button
        Button(answer_frame,text="Write Data",command=write_data).grid(row=90)

    # open json file and read in conference data
    try:
        conf_file_name = str(conf_file.get())
    except:
        conf_file_name = "conf.json"
    F = open(conf_file_name)
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

def open_tourn_sched(root,JSON_file) -> None:
    # create new window object subordinate to the main window (root)
    window = Toplevel(root)
    answer_frame = Frame(window, width =10, height =10)
    answer_frame.grid(row=21)

    def match_boxes(*args) -> None:
        bracket = str(clicked.get())
        teams = tourn_data["BRACKET"].get(bracket,[])
        count = 0
        selections = []
        for widget in answer_frame.winfo_children():
            widget.destroy()
        for team in teams:
            brow = 21+count
            selections.insert(count,StringVar())
            Radiobutton(answer_frame,text=team,value=team,variable=selections[count]).grid(row=brow,column=0)
            Radiobutton(answer_frame,text="Newly Defeated",value="Newly Defeated",variable=selections[count]).grid(row=brow,column=1)
            if team == "Defeated":
                selections[count].set("Defeated")
            count +=1
        def write_data(*args) -> None:
            out_list = []
            for i in range(count):
                team = teams[i]
                selected_value = selections[i].get()
                if selected_value == "Defeated" or selected_value == "Newly Defeated":
                    team = "Defeated"
                out_list.append(team)
            tourn_data["BRACKET"][bracket]=out_list
            json_out = json.dumps(tourn_data,indent=4)
            with open(tourn_file_name, "w") as outfile:
                outfile.write(json_out)

        
        # create a write data button
        Button(answer_frame,text="Write Data",command=write_data).grid(row=90)

    # open json file and read in tournament data
    try:
        tourn_file_name = str(JSON_file.get())
    except:
        tourn_file_name = "tourn.json"
    F = open(tourn_file_name)
    tourn_data = json.load(F)
    F.close

    # bracket_select dropdown
    options = list(tourn_data["BRACKET"].keys())
    clicked = StringVar()
    clicked.set(options[0])
    OptionMenu(window,clicked,*options).grid(row=20)
    clicked.trace_add("write",match_boxes)

    # create a window close button
    Button(window,text="Close",command=window.destroy).grid(row=100)

    #activate window (until it is closed)
    window.grab_set()

    # END OPEN TOURNAMENT SCHEDULE FUNCTION (return None) (ends when window is closed)

def run_conference(runs_value,text,text2,conf_file,pablo_file=None) -> None:
    
    text.delete("1.0","end")
    text2.delete("1.0","end")


    # check/set number of runs for monte carlo simulation (defaut 10000)
    try:
        number_of_runs = int(runs_value.get())
    except:
        number_of_runs = 10000
        runs_value.set("10000")
    
    # get conference data from json file
    try:
        conf_file_name = str(conf_file.get())
    except:
        conf_file_name = "conf.json"
    F = open(conf_file_name)
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
        if (wins + losses) > 0:
            percentage = float(wins) / float(wins + losses)
            if wins == 0:
                percentage += -0.0001 * losses
            if losses == 0:
                percentage += 0.0001 * wins
        else:
            percentage = 0.0
        results_table.append([team.rank,team.my_name,wins,losses,percentage,school])

    # sort results table by percentage, rank, name
    results_table.sort(key=lambda entry: entry[1])
    results_table.sort(key=lambda entry: entry[0])
    results_table.sort(reverse=True,key=lambda entry: entry[4])

    # find wins above expectation
    for school in conf_data["CONFERENCE"]:
        team = Team(school)
        team.load_from_dict(conf_data["CONFERENCE"])
        current_results[school]["actual wins"]=[]
        current_results[school]["probable wins"]=[]
    prob_results = conf.run_past_conference(number_of_runs,number_of_matches,current_results,pablo_data,conf_data)

    #start building out_string with header and current standings table
    out_string = conf_data["TEXT"]["INTRO"]+conf_data["TEXT"]["DIVIDER"]+conf_data["TEXT"]["STANDINGS TOP"]
    for school in results_table:
        prob_wins = prob_results[school[5]]["probable wins"]
        actual_wins = prob_results[school[5]]["actual wins"]
        mean_prob_wins = statistics.mean(prob_wins)
        mean_actual_wins = statistics.mean(actual_wins)
        wins_above_expectation = mean_actual_wins - mean_prob_wins
        out_string += "[font color=\"19e6c5\"]("+str(school[0])+")[/font] "+str(school[1])+" [font color=\"gold\"][b]"+str(school[2])+"-"+str(school[3])+"[/b][/font] [font color=\"caec42\"]("+f'{wins_above_expectation:+.0f}'+")[/font]"+"\n"
    out_string += "\n[font color=\"19e6c5\"]("+str(pablo_data.pablo_date)+" pablo rankings)[/font] School [font color=\"gold\"][b]W-L[/b][/font] [font color=\"caec42\"](wins above expectation)[/font]"+conf_data["TEXT"]["DIVIDER"]

    # build expected wins table
    out_string += "Predicted final win totals as of "+str(pablo_data.run_date)+"\n\n"
    # actually generate expected wins as final_results dict
    for school in conf_data["CONFERENCE"]:
        team = Team(school)
        team.load_from_dict(conf_data["CONFERENCE"])
        current_results[school]["expected wins"]=[]
        current_results[school]["expected placements"]=[]
    # current_results["Defeated"]={"rating":-9999}
    final_results = conf.run_conference(number_of_runs,number_of_matches,current_results,pablo_data,conf_data)
    # del final_results["Defeated"]
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
        if std_wins != 0:
            a0,b0 = ((minimum_possible_wins - mean_wins)/std_wins,(maximum_possible_wins - mean_wins)/std_wins)
            a1,b1,loc,scale = SPstats.truncnorm.fit(wins,a0,b0,loc=mean_wins,scale=std_wins)
            a,b = ((minimum_possible_wins - loc)/scale,(maximum_possible_wins - loc)/scale)
            interval_75 = SPstats.truncnorm.interval(0.75,a,b,loc=loc,scale=scale)
            high_wins = sorted([interval_75[1],minimum_possible_wins,maximum_possible_wins])[1]
            low_wins = sorted([interval_75[0],minimum_possible_wins,maximum_possible_wins])[1]
        else:
            high_wins = mean_wins
            low_wins = mean_wins
        display_name = conf_data["CONFERENCE"][school]["my name"]
        out_string += str(display_name)+" "+str(round(high_wins))+" to "+str(round(low_wins))+" -- median wins: "+str(round(median_wins))+"\n"
    
    # build expected placements table
    number_of_teams = len(conf_data["CONFERENCE"])
    out_string = out_string[:-1] # remove extra \n
    out_string += conf_data["TEXT"]["DIVIDER"]+"Predicted final placements as of "+str(pablo_data.run_date)+"\n\n"
    # find non-overlaps
    boundaries = {}
    for school in wins_sorted_list:
        maximum_possible_wins = final_results[school]["wins"] + final_results[school]["unplayed"]
        minimum_possible_wins = final_results[school]["wins"]
        boundaries[school] = {
            "max": maximum_possible_wins,
            "min": minimum_possible_wins
        }
    for school in boundaries:
        # look for schools you can't fall behind
        count = 0 
        for sch in boundaries:
            if boundaries[school]["min"] >= boundaries[sch]["max"] and school != sch:
                count += 1
        worst_place = number_of_teams - count
        boundaries[school]["worst place"] = worst_place
        # look for schools you can't pass
        count = 0
        for sch in boundaries:
            if boundaries[school]["max"] < boundaries[sch]["min"] and school != sch:
                count += 1
        best_place = 1 + count
        boundaries[school]["best place"] = best_place
    _placements = {}
    for school in pablo_sorted_list:
        _placements[school] = statistics.mean(final_results[school]["expected placements"])
    placements_sorted_list = [x for (x,y) in sorted(_placements.items(), key=lambda item: item[1], reverse=False)]
    # build string
    for school in placements_sorted_list:
        placements = final_results[school]["expected placements"]
        mean_placements = statistics.mean(placements)
        median_placements = statistics.median(placements)
        std_placements = statistics.stdev(placements)
        worst_place = boundaries[school]["worst place"]
        best_place = boundaries[school]["best place"]
        if std_placements != 0:
            a0,b0 = ((best_place - mean_placements)/std_placements,(worst_place - mean_placements)/std_placements)
            a1,b1,loc,scale = SPstats.truncnorm.fit(placements,a0,b0,loc=mean_placements,scale=std_placements)
            a,b = ((best_place - loc)/scale,(worst_place - loc)/scale)
            interval_75 = SPstats.truncnorm.interval(0.75,a,b,loc=loc,scale=scale)
            high_placements = sorted([interval_75[1],1,number_of_teams])[1]
            low_placements = sorted([interval_75[0],1,number_of_teams])[1]
        else:
            high_placements = mean_placements
            low_placements = mean_placements
        display_name = conf_data["CONFERENCE"][school]["my name"]
        out_string += str(display_name)+" "+str(round(low_placements))+" to "+str(round(high_placements))+" -- median placement: "+str(round(median_placements))+"\n"
    
    # build remaining text (will be edited by hand cut/paste from second text box)
    out_string = out_string[:-1] # remove extra \n
    out_string += conf_data["TEXT"]["DIVIDER"]+conf_data["TEXT"]["MATCHES TOP"]+conf_data["TEXT"]["MATCHES SKELETON"]+conf_data["TEXT"]["DIVIDER"]
    out_string += '''[font color="gold"]Pablo highlight matches of the week (top-25 pablo matchups):[/font]

None'''
    out_string += conf_data["TEXT"]["DIVIDER"]
    out_string += '''[font color="red"]Pablo close matches of the week (55 percent or closer):[/font]

None'''
    out_string += conf_data["TEXT"]["DIVIDER"]+conf_data["TEXT"]["NEXT WEEK"]+conf_data["TEXT"]["DIVIDER"]+conf_data["TEXT"]["OUTRO"]
    
    # insert into first text box
    text.insert("1.0",out_string)
    
    # make match lines and insert into second text box (for copy/paste into first text box)
    match_string = conf.make_schedules_and_odds(current_results,pablo_data,conf_data)
    text2.insert("1.0",match_string)

    # END RUN CONFERENCE FUNCTION (return None)


def run_tournament(runs_value,text,text2,tourn_file,pablo_file=None) -> None:

    # check/set number of runs for monte carlo simulation (defaut 10000)
    try:
        number_of_runs = int(runs_value.get())
    except:
        number_of_runs = 10000
        runs_value.set("10000")
    
    # get tournament data from json file
    try:
        tournament_file_name = str(tourn_file.get())
    except:
        tournament_file_name = "tournament.json"
    F = open(tournament_file_name)
    tournament_data = json.load(F)
    F.close

    # seed random number generator
    random.seed()

    # get data from pablo file and create pablo data object
    if pablo_file:
        pablo_data = PabloWeeklyRating(pablo_file)
    else:
        pablo_data = PabloWeeklyRating()
    
    # check to see if there are schools in the bracket not defined in the JSON file
    halt = tourn.bracket_check(tournament_data,text)
    if halt:
        return
    
    # actually run the simulated tournament
    final_results = tourn.run_tournament(tournament_data, pablo_data, number_of_runs)

    # assemble the results
    outstring = "\nList of all schools\n-------------------\n"
    for school in final_results:
        outstring += str(school)+" Champs: "+str(final_results[school].get("champion",0))+" #2: "+str(final_results[school].get("runner up",0))+" FF: "+str(final_results[school].get("FF",0))+"\n"
        outstring += " -- Elite 8: "+str(final_results[school].get("E8",0))+" Sweet 16: "+str(final_results[school].get("S6",0))+" won a match: "+str(final_results[school].get("R2",0))+"\n"
        outstring += " -- one and done: "+str(final_results[school].get("zilch",0))+"\n"
    outstring += "\nOdds determined by using the "+str(pablo_data.pablo_date)+" pablo ratings and the regional home court determined by best surviving seed. Final Four is assumed to be neutral court. Tournament simulation uses random number generator and the pablo-determined odds. Results are based on "+str(number_of_runs)+" simulations."+"\n"
    outstring += "\nPercentage chances by tiers\n-------------------"+"\n"
    list_of_champs = []
    list_of_semis = []
    list_of_FF = []
    list_of_E8 = []
    list_of_S16 = []
    list_of_R2 = []
    for school in final_results:
        name = str(school)
        if name == "Defeated":
            continue
        championships = float(final_results[school].get("champion",0))
        runner = float(final_results[school].get("runner up",0))
        final4 = float(final_results[school].get("FF",0))
        elite8 = float(final_results[school].get("E8",0))
        sweet16 = float(final_results[school].get("S6",0))
        round2 = float(final_results[school].get("R2",0))
        semis = championships + runner
        f4 = semis + final4
        e8 = f4 + elite8
        s16 = e8 + sweet16
        r2 = s16 + round2
        locked = False
        if championships >= float(number_of_runs)*0.05:
            champ_pct = championships / float(number_of_runs) * 100
            list_of_champs.append([name,champ_pct])
            locked = True
        if semis >= float(number_of_runs)*0.10 or locked:
            semi_pct = semis / float(number_of_runs) * 100
            list_of_semis.append([name,semi_pct])
            locked = True
        if f4 >= float(number_of_runs)*0.16 or locked:
            f4_pct = f4 / float(number_of_runs) * 100
            list_of_FF.append([name,f4_pct])
            locked = True
        if e8 >= float(number_of_runs)*0.25 or locked:
            e8_pct = e8 / float(number_of_runs) * 100
            list_of_E8.append([name,e8_pct])
            locked = True
        if s16 >= float(number_of_runs)*0.33 or locked:
            s16_pct = s16 / float(number_of_runs) * 100
            list_of_S16.append([name,s16_pct])
            locked = True
        if r2 >= float(number_of_runs)*0.50 or locked:
            r2_pct = r2 / float(number_of_runs) * 100
            list_of_R2.append([name,r2_pct])
    # list of champions
    sorted_list_of_champs = sorted(list_of_champs,key=lambda x: x[1],reverse=True)
    outstring += "\nChampion (cutoff at 5%)"+"\n"
    for champs in sorted_list_of_champs:
        outstring += str(champs[0])+": "+str(int(round(champs[1],0)))+"%"+"\n"
    # list of teams reaching semis
    sorted_list_of_semis = sorted(list_of_semis,key=lambda x: x[1],reverse=True)
    outstring += "\nFinalist (cutoff at 10%)"+"\n"
    for semis in sorted_list_of_semis:
        outstring += str(semis[0])+": "+str(int(round(semis[1],0)))+"%"+"\n"
    # list of teams reaching FF
    sorted_list_of_FF = sorted(list_of_FF,key=lambda x: x[1],reverse=True)
    outstring += "\nFinal Four (cutoff at 16%)"+"\n"
    for teams in sorted_list_of_FF:
        outstring += str(teams[0])+": "+str(int(round(teams[1],0)))+"%"+"\n"
    # list of teams reaching E8
    sorted_list_of_E8 = sorted(list_of_E8,key=lambda x: x[1],reverse=True)
    outstring += "\nElite Eight (cutoff at 25%)"+"\n"
    for teams in sorted_list_of_E8:
        outstring += str(teams[0])+": "+str(int(round(teams[1],0)))+"%"+"\n"
    # list of teams reaching S16
    sorted_list_of_S16 = sorted(list_of_S16,key=lambda x: x[1],reverse=True)
    outstring += "\nSweet 16 (cutoff at 33%)"+"\n"
    for teams in sorted_list_of_S16:
        outstring += str(teams[0])+": "+str(int(round(teams[1],0)))+"%"+"\n"
    # list of teams reaching round 2
    sorted_list_of_R2 = sorted(list_of_R2,key=lambda x: x[1],reverse=True)
    outstring += "\nRound 2 (cutoff at 50%)"+"\n"
    for teams in sorted_list_of_R2:
        outstring += str(teams[0])+": "+str(int(round(teams[1],0)))+"%"+"\n"
    # estimated finish graphs
    outstring += "\nSimulated Number Of Wins (blocks of up to 5%):"+"\n"
    outstring += "Each X represents "+str(int(0.05*number_of_runs))+" simulated tournaments. The last X (or the first one, if there is only one) represents from 1 to "+str(int(0.05*number_of_runs))+" simulations."+"\n"
    for school in final_results:
        name = str(school)
        if name == "Defeated":
            continue
        championships = float(final_results[school].get("champion",0))
        runner = float(final_results[school].get("runner up",0))
        final4 = float(final_results[school].get("FF",0))
        elite8 = float(final_results[school].get("E8",0))
        sweet16 = float(final_results[school].get("S6",0))
        round2 = float(final_results[school].get("R2",0))
        zilch = float(final_results[school].get("zilch",0))
        results = {
            "6": championships,
            "5": runner,
            "4": final4,
            "3": elite8,
            "2": sweet16,
            "1": round2,
            "0": zilch
        }
        most_common_finish = max(results, key=results.get)
        outstring += "\n"+name+" most common number of wins is "+most_common_finish+"\n"
        outstring += "6: "+tourn.xxx(results["6"],number_of_runs)+"\n"
        outstring += "5: "+tourn.xxx(results["5"],number_of_runs)+"\n"
        outstring += "4: "+tourn.xxx(results["4"],number_of_runs)+"\n"
        outstring += "3: "+tourn.xxx(results["3"],number_of_runs)+"\n"
        outstring += "2: "+tourn.xxx(results["2"],number_of_runs)+"\n"
        outstring += "1: "+tourn.xxx(results["1"],number_of_runs)+"\n"
        outstring += "0: "+tourn.xxx(results["0"],number_of_runs)+"\n"
    avg_pablo = tourn.median_pablo(tournament_data,pablo_data)
    outstring += "\n\nAverage (median) pablo score of remaining teams: "+str(avg_pablo)+"\n"
    # do bracket strength test
    outstring += "\nResults when schools have average pablo score:"+"\n"
    br_list = tourn.bracket_list(tournament_data)
    diff_list = []
    for school in br_list:
        name = str(school)
        if name == "Defeated":
            continue
        final_results = tourn.run_tournament(tournament_data, pablo_data, 500, school)
        championships = float(final_results[school].get("champion",0))
        runner = float(final_results[school].get("runner up",0))
        final4 = float(final_results[school].get("FF",0))
        elite8 = float(final_results[school].get("E8",0))
        sweet16 = float(final_results[school].get("S6",0))
        round2 = float(final_results[school].get("R2",0))
        semis = championships + runner
        f4 = championships + runner + final4
        e8 = championships + runner + final4 + elite8
        s16 = championships + runner + final4 + elite8 + sweet16
        r2 = championships + runner + final4 + elite8 + sweet16 + round2
        champ_pct = float(championships) / 5.0
        semi_pct = float(semis) / 5.0
        f4_pct = float(f4) / 5.0
        e8_pct = float(e8) / 5.0
        s16_pct = float(s16) / 5.0
        r2_pct = float(r2) / 5.0
        diff_list.append([school,champ_pct,f4_pct,s16_pct])
    sorted_diff_list = sorted(diff_list,key=lambda x: x[1],reverse=True)
    outstring += "\nFour easiest paths to the championship"+"\n"
    for school in sorted_diff_list[0:4]:
        outstring += str(school[0])+": "+str(round(school[1],1))+"%"+"\n"
    sorted_diff_list = sorted(diff_list,key=lambda x: x[2],reverse=True)
    outstring += "\nEight easiest paths to the Final Four"+"\n"
    for school in sorted_diff_list[0:8]:
        outstring += str(school[0])+": "+str(round(school[2],1))+"%"+"\n"
    sorted_diff_list = sorted(diff_list,key=lambda x: x[3],reverse=True)
    outstring += "\nSixteen easiest paths to the Sweet 16"+"\n"
    for school in sorted_diff_list[0:20]:
        outstring += str(school[0])+": "+str(round(school[3],1))+"%"+"\n"

    # insert into first text box
    text.delete("1.0","end")
    text.insert("1.0",outstring)


    # END RUN Tournament FUNCTION (return None)



def main():
    root = Tk()

    # set some things that will be used elsewhere
    pablo_date=StringVar(root,"no pablo data")
    hca=IntVar(root,0)
    runs_value = StringVar(root,"10000")
    conf_file_value = StringVar(root,'conf.json')
    tournament_file_value = StringVar(root,'tournament.json')
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
    Label(root,text="JSON conf file name:").grid(row=6,column=0)
    Label(root,text="JSON tourn file name:").grid(row=6,column=2)
    # text and entry boxes
    text = Text(root,width=100,height=25)
    text.grid(row=16,columnspan=99)
    text2 = Text(root,width=100,height=25)
    text2.grid(row=18,columnspan=99)
    runs = Entry(root,textvariable=runs_value)
    runs.grid(row=5, column=1)
    conf_file = Entry(root,textvariable=conf_file_value)
    conf_file.grid(row=6, column=1)
    tournament_file = Entry(root,textvariable=tournament_file_value)
    tournament_file.grid(row=6, column=3)
    # buttons
    Button(root,text="Check Pablo",command=test_pablo).grid(row=3,columnspan=2)
    Button(root,text="Run Conference",command=lambda: run_conference(runs_value,text,text2,conf_file_value)).grid(row=7,columnspan=2)
    Button(root,text="Run Tournament",command=lambda: run_tournament(runs_value,text,text2,tournament_file_value)).grid(row=7,column=2,columnspan=2)
    Button(root,text="Edit Schedule",command=lambda: open_conf_sched(root,conf_file_value)).grid(row=8,columnspan=2)
    Button(root,text="Edit Schedule",command=lambda: open_tourn_sched(root,tournament_file_value)).grid(row=8,column=2,columnspan=2)

    root.mainloop()

    # END MAIN FUNCTION (return None, program will end when mainloop ends)






if __name__ == "__main__":
    main()
