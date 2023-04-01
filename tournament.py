import random
import statistics
import math
import json
from classes import Team



def read_data(tournament_file=None) -> dict:
    try:
        tournament_file_name = str(tournament_file.get())
    except:
        tournament_file_name = "tournament.json"

    F = open(tournament_file_name)
    tournament_data = json.load(F)
    F.close

    return tournament_data

def make_quad_list(tournament_data, quad) -> list:
    bracket = tournament_data["BRACKET"][quad]
    return bracket


def play_match(tournament_data, pablo_data, schools, home_school, avg_school=None) -> float:
    team0 = Team(schools[0])
    team1 = Team(schools[1])
    if team0.name == "Defeated":
        team0.set_names("Defeated","Defeated")
    else:
        team0.load_from_dict(tournament_data["SCHOOLS"])
    if team1.name == "Defeated":
        team1.set_names("Defeated","Defeated")
    else:
        team1.load_from_dict(tournament_data["SCHOOLS"])
    team0.find_pablo(pablo_data)
    team1.find_pablo(pablo_data)
    if schools[0] == avg_school:
        team0.rating = median_pablo(tournament_data,pablo_data)
    if schools[1] == avg_school:
        team1.rating = median_pablo(tournament_data,pablo_data)
    if schools[0] == home_school:
        team_1_prob = team1.chance_to_win(pablo_data,team0,"A")
    elif schools[1] == home_school:
        team_1_prob = team1.chance_to_win(pablo_data,team0,"H")
    else:
        team_1_prob = team1.chance_to_win(pablo_data,team0,"N")
    return team_1_prob


def play_quad(tournament_data, pablo_data, bracket, neutral_flag=False, avg_school=None) -> list:
    
    # who is home?
    home_school = None
    top_seed = None
    for school in bracket:
        this_school = Team(school)
        if school == "Defeated":
            this_school.set_names("Defeated","Defeated")
        else:
            this_school.load_from_dict(tournament_data["SCHOOLS"])
        seed = this_school.seed
        if seed != 9999:
            if top_seed:
                if seed < top_seed:
                    home_school = school
                    top_seed = seed
            else:
                top_seed = seed
                home_school = school
    if neutral_flag:
        home_school = None
    
    # play first game
    schools = [bracket[0],bracket[1]]
    team_1_prob = play_match(tournament_data,pablo_data,schools,home_school,avg_school)
    # who won?
    score = random.random()
    if score <= team_1_prob:
        game_1_winner = schools[1]
        game_1_loser = schools[0]
    else:
        game_1_winner = schools[0]
        game_1_loser = schools[1]

    # play second game
    schools = [bracket[2],bracket[3]]
    team_1_prob = play_match(tournament_data,pablo_data,schools,home_school,avg_school)
    # who won?
    score = random.random()
    if score <= team_1_prob:
        game_2_winner = schools[1]
        game_2_loser = schools[0]
    else:
        game_2_winner = schools[0]
        game_2_loser = schools[1]

    # play third game
    schools = [game_1_winner,game_2_winner]
    team_1_prob = play_match(tournament_data,pablo_data,schools,home_school,avg_school)
    # who won?
    score = random.random()
    if score <= team_1_prob:
        game_3_winner = schools[1]
        game_3_loser = schools[0]
    else:
        game_3_winner = schools[0]
        game_3_loser = schools[1]

    winners = [game_3_winner,game_3_loser,game_1_loser,game_2_loser]
    return winners


# bracket check
def bracket_check(tournament_data,text_window=None) -> bool:
    halt = False
    if text_window:
        text_window.delete("1.0","end")
        out_string = ""
    for quad in tournament_data["BRACKET"]:
        for school in tournament_data["BRACKET"][quad]:
            school_data = tournament_data["SCHOOLS"].get(school)
            if not school_data:
                halt = True
                if text_window:
                    out_string += "No data found for school: "+str(school)+" in quad: "+str(quad)+"\n"
                else:
                    raise ValueError("No data found for school: "+str(school)+" in quad: "+str(quad))
    if text_window:
        out_string += "Open tournament JSON file and add missing schools to SCHOOLS data or correct errors in brackets."
        text_window.insert("1.0",out_string)
    return halt

# bracket list
def bracket_list(tournament_data) -> list:
    br_list = []
    for quad in tournament_data["BRACKET"]:
        for school in tournament_data["BRACKET"][quad]:
            br_list.append(school)
    return br_list



# average pablo score
def median_pablo(tournament_data,pablo_data) -> int:
    pablos = []
    for quad in tournament_data["BRACKET"]:
        for school in tournament_data["BRACKET"][quad]:
            if school == "Defeated":
                continue
            this_school = Team(school)
            this_school.load_from_dict(tournament_data["SCHOOLS"])
            this_school.find_pablo(pablo_data)
            pablos.append(this_school.rating)
    median = statistics.median(pablos)
    return round(median)
            


# run tournament
def run_tournament(tournament_data,pablo_data,number_of_runs,avg_school=None) -> dict:
    results = {}
    for i in range(number_of_runs):
        # make results buckets
        regionals = {}
        losers = {
            "round 1": [],
            "round 2": [],
            "round 3": [],
            "round 4": [],
            "round 5": [],
            "round 6": [],
        }

        # play subregionals
        for quad in tournament_data["BRACKET"]:
            bracket = make_quad_list(tournament_data,quad)
            winners = play_quad(tournament_data,pablo_data,bracket,False,avg_school)
            regionals[quad] = winners[0]
            losers["round 1"].append(winners[2])
            losers["round 1"].append(winners[3])
            losers["round 2"].append(winners[1])
        
        # play regionals
        ff = []
        r1 = [regionals["UL1"],regionals["UL4"],regionals["UL2"],regionals["UL3"]]
        r2 = [regionals["LL1"],regionals["LL4"],regionals["LL2"],regionals["LL3"]]
        r3 = [regionals["UR1"],regionals["UR4"],regionals["UR2"],regionals["UR3"]]
        r4 = [regionals["LR1"],regionals["LR4"],regionals["LR2"],regionals["LR3"]]
        winners = play_quad(tournament_data,pablo_data,r1,False,avg_school)
        ff = [winners[0]]
        losers["round 3"].append(winners[2])
        losers["round 3"].append(winners[3])
        losers["round 4"].append(winners[1])
        winners = play_quad(tournament_data,pablo_data,r2,False,avg_school)
        ff.append(winners[0])
        losers["round 3"].append(winners[2])
        losers["round 3"].append(winners[3])
        losers["round 4"].append(winners[1])
        winners = play_quad(tournament_data,pablo_data,r3,False,avg_school)
        ff.append(winners[0])
        losers["round 3"].append(winners[2])
        losers["round 3"].append(winners[3])
        losers["round 4"].append(winners[1])
        winners = play_quad(tournament_data,pablo_data,r4,False,avg_school)
        ff.append(winners[0])
        losers["round 3"].append(winners[2])
        losers["round 3"].append(winners[3])
        losers["round 4"].append(winners[1])

        # play ff
        winners = play_quad(tournament_data,pablo_data,ff,True,avg_school)
        champion = winners[0]
        losers["round 5"].append(winners[2])
        losers["round 5"].append(winners[3])
        losers["round 6"].append(winners[1])
    
        # record results
        champ_school = results.get(champion)
        if not champ_school:
            results[champion] = {"champion": 1}
        else:
            old_total = champ_school.get("champion",0)
            results[champion]["champion"] = old_total + 1
        runner_school = results.get(losers["round 6"][0])
        if not runner_school:
            results[losers["round 6"][0]] = {"runner up": 1}
        else:
            old_total = runner_school.get("runner up",0)
            results[losers["round 6"][0]]["runner up"] = old_total + 1
        for school in losers["round 5"]:
            ff_school = results.get(school)
            if not ff_school:
                results[school] = {"FF": 1}
            else:
                old_total = ff_school.get("FF",0)
                results[school]["FF"] = old_total + 1
        for school in losers["round 4"]:
            elite_school = results.get(school)
            if not elite_school:
                results[school] = {"E8": 1}
            else:
                old_total = elite_school.get("E8",0)
                results[school]["E8"] = old_total + 1
        for school in losers["round 3"]:
            sweet_school = results.get(school)
            if not sweet_school:
                results[school] = {"S6": 1}
            else:
                old_total = sweet_school.get("S6",0)
                results[school]["S6"] = old_total + 1
        for school in losers["round 2"]:
            sub_school = results.get(school)
            if not sub_school:
                results[school] = {"R2": 1}
            else:
                old_total = sub_school.get("R2",0)
                results[school]["R2"] = old_total + 1
        for school in losers["round 1"]:
            done_school = results.get(school)
            if not done_school:
                results[school] = {"zilch": 1}
            else:
                old_total = done_school.get("zilch",0)
                results[school]["zilch"] = old_total + 1


    return results

def xxx(value,NUMBER_OF_RUNS) -> str:
    out_str = ""
    if value != 0:
        number_of_x = math.ceil(float(value)*20.0/float(NUMBER_OF_RUNS))
        for i in range(number_of_x):
            out_str += "X"
    return out_str

