import random
import runtime
import pablo
import statistics

random.seed()



# average pablo score
def median_pablo() -> int:
    pablos = []
    for school in runtime.CONFERENCE:
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
NUMBER_OF_MATCHES = 8
final_results = run_conference(NUMBER_OF_RUNS, NUMBER_OF_MATCHES)
# sort schools
sorted_list_of_schools = sorted(runtime.CONFERENCE)
_pablo = {}
for school in sorted_list_of_schools:
    _pablo[school] = runtime.SCHOOLS[school]["pablo"]
pablo_sorted_list = [x for (x,y) in sorted(_pablo.items(), key=lambda item: item[1], reverse=True)]
_wins = {}
for school in pablo_sorted_list:
    _wins[school] = statistics.mean(final_results[school]["wins"])
wins_sorted_list = [x for (x,y) in sorted(_wins.items(), key=lambda item: item[1], reverse=True)]
print("\nList of all schools\n-------------------")
for school in wins_sorted_list:
    wins = final_results[school]["wins"]
    mean_wins = statistics.mean(wins)
    median_wins = statistics.median(wins)
    std_wins = statistics.stdev(wins)
    high_wins = sorted([mean_wins+std_wins,0,NUMBER_OF_MATCHES])[1]
    low_wins = sorted([mean_wins-std_wins,0,NUMBER_OF_MATCHES])[1]
    print(str(school)+" Expected wins: "+str(round(high_wins,1))+" to "+str(round(low_wins,1))+" -- median wins: "+str(round(median_wins)))
print("\nPlaces\n-------------------")
for school in wins_sorted_list:
    number_of_teams = len(runtime.CONFERENCE)
    wins = final_results[school]["placements"]
    mean_wins = statistics.mean(wins)
    median_wins = statistics.median(wins)
    std_wins = statistics.stdev(wins)
    high_wins = sorted([mean_wins+std_wins,1,number_of_teams])[1]
    low_wins = sorted([mean_wins-std_wins,1,number_of_teams])[1]
    print(str(school)+" Expected placement: "+str(round(low_wins,1))+" to "+str(round(high_wins,1))+" -- median placement: "+str(round(median_wins)))
