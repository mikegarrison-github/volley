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
def run_conference(number_of_runs, number_of_matches) -> dict:
    results = {}
    for school in runtime.CONFERENCE:
        results[school]={"wins":[],"placements":[]}
    for i in range(number_of_runs):
        season_results = {}
        for week in runtime.CONF_SCHED:
            for match in runtime.CONF_SCHED[week]:
                home_prob = pablo.pablo_odds(runtime.SCHOOLS[match[1]]["pablo"],runtime.SCHOOLS[match[0]]["pablo"],"H")
                score = random.random()
                if score <= home_prob:
                    wins = season_results.get(match[1],0)
                    season_results[match[1]] = wins + 1
                else:
                    wins = season_results.get(match[0],0)
                    season_results[match[0]] = wins + 1
        standings = {}
        for school in runtime.CONFERENCE:
            wins = season_results.get(school,0)
            percentage = float(wins) / float(number_of_matches)
            standings[school] = percentage
        ordered_list = sorted(standings.items(), key=lambda item: item[1], reverse=True)
        place = 1
        count = 0
        current_percentage = 1.0
        for item in ordered_list:
            school,percentage = item
            if percentage == current_percentage:
                standings[school] = place
                count += 1
            else:
                place += count
                standings[school] = place
                count = 1
                current_percentage = percentage
        for school in runtime.CONFERENCE:
            past_results = results[school]
            wins = past_results["wins"]
            placements = past_results["placements"]
            wins.append(season_results.get(school,0))
            placements.append(standings[school])
            results[school] = {"wins":wins,"placements":placements}
    return results

# run
NUMBER_OF_RUNS = 1000
NUMBER_OF_MATCHES = 4
final_results = run_conference(NUMBER_OF_RUNS, NUMBER_OF_MATCHES)
print("\nList of all schools\n-------------------")
for school in final_results:
    wins = final_results[school]["wins"]
    mean_wins = statistics.mean(wins)
    median_wins = statistics.median(wins)
    std_wins = statistics.stdev(wins)
    print(str(school)+" mean wins: "+str(mean_wins)+" median wins: "+str(median_wins))
