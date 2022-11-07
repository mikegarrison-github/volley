import random
import runtime
import pablo

random.seed()

def make_quad_list(quad) -> list:
    bracket = runtime.BRACKET[quad]
    return bracket


def play_quad(bracket, neutral_flag=False) -> list:
    
    # who is home?
    home_school = None
    top_seed = None
    for school in bracket:
        school_data = runtime.SCHOOLS[school]
        seed = school_data["seed"]
        if seed:
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
    if schools[0] == home_school:
        team_1_prob = pablo.pablo_odds(runtime.SCHOOLS[schools[0]]["pablo"],runtime.SCHOOLS[schools[1]]["pablo"],"H")
    elif schools[1] == home_school:
        team_1_prob = pablo.pablo_odds(runtime.SCHOOLS[schools[0]]["pablo"],runtime.SCHOOLS[schools[1]]["pablo"],"A")
    else:
        team_1_prob = pablo.pablo_odds(runtime.SCHOOLS[schools[0]]["pablo"],runtime.SCHOOLS[schools[1]]["pablo"],"N")
    # who won?
    score = random.random()
    if score <= team_1_prob:
        game_1_winner = schools[0]
        game_1_loser = schools[1]
    else:
        game_1_winner = schools[1]
        game_1_loser = schools[0]

    # play second game
    schools = [bracket[2],bracket[3]]
    if schools[0] == home_school:
        team_1_prob = pablo.pablo_odds(runtime.SCHOOLS[schools[0]]["pablo"],runtime.SCHOOLS[schools[1]]["pablo"],"H")
    elif schools[1] == home_school:
        team_1_prob = pablo.pablo_odds(runtime.SCHOOLS[schools[0]]["pablo"],runtime.SCHOOLS[schools[1]]["pablo"],"A")
    else:
        team_1_prob = pablo.pablo_odds(runtime.SCHOOLS[schools[0]]["pablo"],runtime.SCHOOLS[schools[1]]["pablo"],"N")
    # who won?
    score = random.random()
    if score <= team_1_prob:
        game_2_winner = schools[0]
        game_2_loser = schools[1]
    else:
        game_2_winner = schools[1]
        game_2_loser = schools[0]

    # play third game
    schools = [game_1_winner,game_2_winner]
    if schools[0] == home_school:
        team_1_prob = pablo.pablo_odds(runtime.SCHOOLS[schools[0]]["pablo"],runtime.SCHOOLS[schools[1]]["pablo"],"H")
    elif schools[1] == home_school:
        team_1_prob = pablo.pablo_odds(runtime.SCHOOLS[schools[0]]["pablo"],runtime.SCHOOLS[schools[1]]["pablo"],"A")
    else:
        team_1_prob = pablo.pablo_odds(runtime.SCHOOLS[schools[0]]["pablo"],runtime.SCHOOLS[schools[1]]["pablo"],"N")
    # who won?
    score = random.random()
    if score <= team_1_prob:
        game_3_winner = schools[0]
        game_3_loser = schools[1]
    else:
        game_3_winner = schools[1]
        game_3_loser = schools[0]

    winners = [game_3_winner,game_3_loser,game_1_loser,game_2_loser]
    return winners


# bracket check
def bracket_check() -> None:
    for quad in runtime.BRACKET:
        for school in runtime.BRACKET[quad]:
            school_data = runtime.SCHOOLS.get(school)
            if not school_data:
                raise ValueError("No data found for school: "+str(school)+" in quad: "+str(quad))


# run tournament
def run_tournament(number_of_runs) -> dict:
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
        for quad in runtime.BRACKET:
            bracket = make_quad_list(quad)
            winners = play_quad(bracket)
            regionals[quad] = winners[0]
            losers["round 1"].append(winners[2])
            losers["round 1"].append(winners[3])
            losers["round 2"].append(winners[1])
        
        # play regionals
        ff = []
        r1 = [regionals["1"],regionals["16"],regionals["8"],regionals["9"]]
        r2 = [regionals["2"],regionals["15"],regionals["7"],regionals["10"]]
        r3 = [regionals["3"],regionals["14"],regionals["6"],regionals["11"]]
        r4 = [regionals["4"],regionals["13"],regionals["5"],regionals["12"]]
        winners = play_quad(r1)
        ff = [winners[0]]
        losers["round 3"].append(winners[2])
        losers["round 3"].append(winners[3])
        losers["round 4"].append(winners[1])
        winners = play_quad(r4)
        ff.append(winners[0])
        losers["round 3"].append(winners[2])
        losers["round 3"].append(winners[3])
        losers["round 4"].append(winners[1])
        winners = play_quad(r3)
        ff.append(winners[0])
        losers["round 3"].append(winners[2])
        losers["round 3"].append(winners[3])
        losers["round 4"].append(winners[1])
        winners = play_quad(r2)
        ff.append(winners[0])
        losers["round 3"].append(winners[2])
        losers["round 3"].append(winners[3])
        losers["round 4"].append(winners[1])

        # play ff
        winners = play_quad(ff,True)
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

# run
NUMBER_OF_RUNS = 100000
bracket_check()
final_results = run_tournament(NUMBER_OF_RUNS)
for school in final_results:
    print(str(school)+" Champs: "+str(final_results[school].get("champion",0))+" #2: "+str(final_results[school].get("runner up",0))+" FF: "+str(final_results[school].get("FF",0)))
    print(" -- Elite 8: "+str(final_results[school].get("E8",0))+" Sweet 16: "+str(final_results[school].get("S6",0))+" won a match: "+str(final_results[school].get("R2",0)))
    print(" -- one and done: "+str(final_results[school].get("zilch",0)))
# list of champions
list_of_champs = []
for school in final_results:
    championships = float(final_results[school].get("champion",0))
    if championships >= float(NUMBER_OF_RUNS)*0.05:
        name = str(school)
        champ_pct = championships / float(NUMBER_OF_RUNS) * 100
        list_of_champs.append([name,champ_pct])
sorted_list_of_champs = sorted(list_of_champs,key=lambda x: x[1],reverse=True)
print("Championship Percentages")
for champs in sorted_list_of_champs:
    print(str(champs[0])+": "+str(round(champs[1],1)))
# list of teams reaching semis
list_of_semis = []
for school in final_results:
    championships = float(final_results[school].get("champion",0))
    runner = float(final_results[school].get("runner up",0))
    semis = championships + runner
    if semis >= float(NUMBER_OF_RUNS)*0.10 or championships >= float(NUMBER_OF_RUNS)*0.05:
        name = str(school)
        semi_pct = semis / float(NUMBER_OF_RUNS) * 100
        list_of_semis.append([name,semi_pct])
sorted_list_of_semis = sorted(list_of_semis,key=lambda x: x[1],reverse=True)
print("Semi-finalist Percentages")
for semis in sorted_list_of_semis:
    print(str(semis[0])+": "+str(round(semis[1],1)))
# list of teams reaching FF
list_of_FF = []
for school in final_results:
    championships = float(final_results[school].get("champion",0))
    runner = float(final_results[school].get("runner up",0))
    final4 = float(final_results[school].get("FF",0))
    semis = championships + runner
    f4 = championships + runner + final4
    if semis >= float(NUMBER_OF_RUNS)*0.10 or championships >= float(NUMBER_OF_RUNS)*0.05 or f4 >= float(NUMBER_OF_RUNS)*0.15:
        name = str(school)
        f4_pct = f4 / float(NUMBER_OF_RUNS) * 100
        list_of_FF.append([name,f4_pct])
sorted_list_of_FF = sorted(list_of_FF,key=lambda x: x[1],reverse=True)
print("Final Four Percentages")
for teams in sorted_list_of_FF:
    print(str(teams[0])+": "+str(round(teams[1],1)))
# list of teams reaching E8
list_of_E8 = []
for school in final_results:
    championships = float(final_results[school].get("champion",0))
    runner = float(final_results[school].get("runner up",0))
    final4 = float(final_results[school].get("FF",0))
    elite8 = float(final_results[school].get("E8",0))
    semis = championships + runner
    f4 = championships + runner + final4
    e8 = championships + runner + final4 + elite8
    if semis >= float(NUMBER_OF_RUNS)*0.10 or championships >= float(NUMBER_OF_RUNS)*0.05 or f4 >= float(NUMBER_OF_RUNS)*0.15 or e8 >= float(NUMBER_OF_RUNS)*0.20:
        name = str(school)
        e8_pct = e8 / float(NUMBER_OF_RUNS) * 100
        list_of_E8.append([name,e8_pct])
sorted_list_of_E8 = sorted(list_of_E8,key=lambda x: x[1],reverse=True)
print("Elite Eight Percentages")
for teams in sorted_list_of_E8:
    print(str(teams[0])+": "+str(round(teams[1],1)))
# list of teams reaching S16
list_of_S16 = []
for school in final_results:
    championships = float(final_results[school].get("champion",0))
    runner = float(final_results[school].get("runner up",0))
    final4 = float(final_results[school].get("FF",0))
    elite8 = float(final_results[school].get("E8",0))
    sweet16 = float(final_results[school].get("S6",0))
    semis = championships + runner
    f4 = championships + runner + final4
    e8 = championships + runner + final4 + elite8
    s16 = championships + runner + final4 + elite8 + sweet16
    if semis >= float(NUMBER_OF_RUNS)*0.10 or championships >= float(NUMBER_OF_RUNS)*0.05 or f4 >= float(NUMBER_OF_RUNS)*0.15 or e8 >= float(NUMBER_OF_RUNS)*0.20 or s16 >= float(NUMBER_OF_RUNS)*0.30:
        name = str(school)
        s16_pct = s16 / float(NUMBER_OF_RUNS) * 100
        list_of_S16.append([name,s16_pct])
sorted_list_of_S16 = sorted(list_of_S16,key=lambda x: x[1],reverse=True)
print("Sweet 16 Percentages")
for teams in sorted_list_of_S16:
    print(str(teams[0])+": "+str(round(teams[1],1)))
# list of teams reaching round 2
list_of_R2 = []
for school in final_results:
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
    if semis >= float(NUMBER_OF_RUNS)*0.10 or championships >= float(NUMBER_OF_RUNS)*0.05 or f4 >= float(NUMBER_OF_RUNS)*0.15 or e8 >= float(NUMBER_OF_RUNS)*0.20 or s16 >= float(NUMBER_OF_RUNS)*0.30 or r2 >= float(NUMBER_OF_RUNS)*0.50:
        name = str(school)
        r2_pct = r2 / float(NUMBER_OF_RUNS) * 100
        list_of_R2.append([name,r2_pct])
sorted_list_of_R2 = sorted(list_of_R2,key=lambda x: x[1],reverse=True)
print("Round 2 Percentages")
for teams in sorted_list_of_R2:
    print(str(teams[0])+": "+str(round(teams[1],1)))
