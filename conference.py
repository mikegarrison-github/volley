import random
import runtime
import pablo
import statistics

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


# average pablo score
def median_pablo() -> int:
    pablos = []
    for quad in runtime.BRACKET:
        for school in runtime.BRACKET[quad]:
            if school == "Defeated":
                continue
            school_data = runtime.SCHOOLS.get(school)
            pablos.append(school_data["pablo"])
    median = statistics.median(pablos)
    return round(median)
            


# run conference
def run_conference(number_of_runs) -> dict:
    results = {}
    for i in range(number_of_runs):
        season_results = {}
        for week in runtime.CONF_SCHED:
            for match in runtime.CONF_SCHED[week]:
                home_prob = pablo.pablo_odds(runtime.SCHOOLS[match[1]]["pablo"],runtime.SCHOOLS[match[0]]["pablo"],"H")
                score = random.random()
                if score <= home_prob:
                    wins = season_results.get(match[1],0)
                    season_results[match[1]] = wins + 1
                    wins = season_results.get(match[0],0)
                    season_results[match[0]] = wins
                else:
                    wins = season_results.get(match[0],0)
                    season_results[match[0]] = wins + 1
                    wins = season_results.get(match[1],0)
                    season_results[match[1]] = wins
        for school in season_results:
            total_wins = results.get(school,0)
            results[school] = total_wins + season_results[school]
    return results

# run
NUMBER_OF_RUNS = 1000
NUMBER_OF_MATCHES = 4
bracket_check()
final_results = run_conference(NUMBER_OF_RUNS)
print("\nList of all schools\n-------------------")
for school in final_results:
    total_wins = final_results.get(school,0)
    average_wins = float(total_wins)/float(NUMBER_OF_RUNS)
    total_losses = NUMBER_OF_RUNS * NUMBER_OF_MATCHES - total_wins
    average_losses = float(total_losses)/float(NUMBER_OF_RUNS)
    print(str(school)+" total wins: "+str(total_wins)+" total losse: "+str(total_losses))
    print(" -- average wins: "+str(average_wins)+" average_losses: "+str(average_losses))
