import random
import runtime
import pablo
import statistics
import math
import json
from classes import Team,PabloWeeklyRating



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
def bracket_check(tournament_data) -> None:
    for quad in tournament_data["BRACKET"]:
        for school in tournament_data["BRACKET"][quad]:
            school_data = tournament_data["SCHOOLS"].get(school)
            if not school_data:
                raise ValueError("No data found for school: "+str(school)+" in quad: "+str(quad))

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

def main():
    # run
    random.seed()

    NUMBER_OF_RUNS = 1000
    tournament_data = read_data()
    pablo_data = PabloWeeklyRating()

    bracket_check(tournament_data)

    final_results = run_tournament(tournament_data, pablo_data, NUMBER_OF_RUNS)
    print("\nList of all schools\n-------------------")
    for school in final_results:
        print(str(school)+" Champs: "+str(final_results[school].get("champion",0))+" #2: "+str(final_results[school].get("runner up",0))+" FF: "+str(final_results[school].get("FF",0)))
        print(" -- Elite 8: "+str(final_results[school].get("E8",0))+" Sweet 16: "+str(final_results[school].get("S6",0))+" won a match: "+str(final_results[school].get("R2",0)))
        print(" -- one and done: "+str(final_results[school].get("zilch",0)))
    print("\nOdds determined by using the "+runtime.PABLO_DATE+" pablo ratings and the regional home court determined by best surviving seed. Final Four is assumed to be neutral court. Tournament simulation uses random number generator and the pablo-determined odds. Results are based on "+str(NUMBER_OF_RUNS)+" simulations.")
    print("\nPercentage chances by tiers\n-------------------")
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
        if championships >= float(NUMBER_OF_RUNS)*0.05:
            champ_pct = championships / float(NUMBER_OF_RUNS) * 100
            list_of_champs.append([name,champ_pct])
            locked = True
        if semis >= float(NUMBER_OF_RUNS)*0.10 or locked:
            semi_pct = semis / float(NUMBER_OF_RUNS) * 100
            list_of_semis.append([name,semi_pct])
            locked = True
        if f4 >= float(NUMBER_OF_RUNS)*0.16 or locked:
            f4_pct = f4 / float(NUMBER_OF_RUNS) * 100
            list_of_FF.append([name,f4_pct])
            locked = True
        if e8 >= float(NUMBER_OF_RUNS)*0.25 or locked:
            e8_pct = e8 / float(NUMBER_OF_RUNS) * 100
            list_of_E8.append([name,e8_pct])
            locked = True
        if s16 >= float(NUMBER_OF_RUNS)*0.33 or locked:
            s16_pct = s16 / float(NUMBER_OF_RUNS) * 100
            list_of_S16.append([name,s16_pct])
            locked = True
        if r2 >= float(NUMBER_OF_RUNS)*0.50 or locked:
            r2_pct = r2 / float(NUMBER_OF_RUNS) * 100
            list_of_R2.append([name,r2_pct])
    # list of champions
    sorted_list_of_champs = sorted(list_of_champs,key=lambda x: x[1],reverse=True)
    print("\nChampion (cutoff at 5%)")
    for champs in sorted_list_of_champs:
        print(str(champs[0])+": "+str(int(round(champs[1],0)))+"%")
    # list of teams reaching semis
    sorted_list_of_semis = sorted(list_of_semis,key=lambda x: x[1],reverse=True)
    print("\nFinalist (cutoff at 10%)")
    for semis in sorted_list_of_semis:
        print(str(semis[0])+": "+str(int(round(semis[1],0)))+"%")
    # list of teams reaching FF
    sorted_list_of_FF = sorted(list_of_FF,key=lambda x: x[1],reverse=True)
    print("\nFinal Four (cutoff at 16%)")
    for teams in sorted_list_of_FF:
        print(str(teams[0])+": "+str(int(round(teams[1],0)))+"%")
    # list of teams reaching E8
    sorted_list_of_E8 = sorted(list_of_E8,key=lambda x: x[1],reverse=True)
    print("\nElite Eight (cutoff at 25%)")
    for teams in sorted_list_of_E8:
        print(str(teams[0])+": "+str(int(round(teams[1],0)))+"%")
    # list of teams reaching S16
    sorted_list_of_S16 = sorted(list_of_S16,key=lambda x: x[1],reverse=True)
    print("\nSweet 16 (cutoff at 33%)")
    for teams in sorted_list_of_S16:
        print(str(teams[0])+": "+str(int(round(teams[1],0)))+"%")
    # list of teams reaching round 2
    sorted_list_of_R2 = sorted(list_of_R2,key=lambda x: x[1],reverse=True)
    print("\nRound 2 (cutoff at 50%)")
    for teams in sorted_list_of_R2:
        print(str(teams[0])+": "+str(int(round(teams[1],0)))+"%")
    # estimated finish graphs
    print("\nSimulated Number Of Wins (blocks of up to 5%):")
    print("Each X represents "+str(int(0.05*NUMBER_OF_RUNS))+" simulated tournaments. The last X (or the first one, if there is only one) represents from 1 to "+str(int(0.05*NUMBER_OF_RUNS))+" simulations.")
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
        print("\n"+name+" most common number of wins is "+most_common_finish)
        print("6: "+xxx(results["6"],NUMBER_OF_RUNS))
        print("5: "+xxx(results["5"],NUMBER_OF_RUNS))
        print("4: "+xxx(results["4"],NUMBER_OF_RUNS))
        print("3: "+xxx(results["3"],NUMBER_OF_RUNS))
        print("2: "+xxx(results["2"],NUMBER_OF_RUNS))
        print("1: "+xxx(results["1"],NUMBER_OF_RUNS))
        print("0: "+xxx(results["0"],NUMBER_OF_RUNS))
    avg_pablo = median_pablo(tournament_data,pablo_data)
    print("\n\nAverage (median) pablo score of remaining teams: "+str(avg_pablo))
    # do bracket strength test
    print("\nResults when schools have average pablo score:")
    br_list = bracket_list(tournament_data)
    diff_list = []
    for school in br_list:
        name = str(school)
        if name == "Defeated":
            continue
        final_results = run_tournament(tournament_data, pablo_data, 15, school)
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
        champ_pct = float(championships) / 15.0
        semi_pct = float(semis) / 15.0
        f4_pct = float(f4) / 15.0
        e8_pct = float(e8) / 15.0
        s16_pct = float(s16) / 15.0
        r2_pct = float(r2) / 15.0
        diff_list.append([school,champ_pct,f4_pct,s16_pct])
    sorted_diff_list = sorted(diff_list,key=lambda x: x[1],reverse=True)
    print("\nFour easiest paths to the championship")
    for school in sorted_diff_list[0:4]:
        print(str(school[0])+": "+str(round(school[1],1))+"%")
    sorted_diff_list = sorted(diff_list,key=lambda x: x[2],reverse=True)
    print("\nEight easiest paths to the Final Four")
    for school in sorted_diff_list[0:8]:
        print(str(school[0])+": "+str(round(school[2],1))+"%")
    sorted_diff_list = sorted(diff_list,key=lambda x: x[3],reverse=True)
    print("\nSixteen easiest paths to the Sweet 16")
    for school in sorted_diff_list[0:20]:
        print(str(school[0])+": "+str(round(school[3],1))+"%")

if __name__ == "__main__":
    main()