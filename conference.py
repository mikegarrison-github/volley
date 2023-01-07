import random
import runtime
import pablo
import statistics

# average pablo score
def median_pablo() -> int:
    pablos = []
    for school in runtime.CONFERENCE.items():
        rk_name = school["rk name"]
        rating, rank, hca, pablo_date = pablo.find_pablo(rk_name)
        pablos.append(rating)
    median = statistics.median(pablos)
    return round(median)
            
# run conference
def run_conference(number_of_runs, number_of_matches, results, hca) -> dict:
    for i in range(number_of_runs):
        season_results = {}
        for week in runtime.CONF_SCHED:
            for match in runtime.CONF_SCHED[week]:
                home_prob = pablo.pablo_odds(results[match[1]]["rating"],results[match[0]]["rating"],"H",hca)
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
            wins = past_results["expected wins"]
            placements = past_results["expected placements"]
            wins.append(season_results.get(school,0))
            placements.append(standings[school])
            results[school]["expected wins"] = wins
            results[school]["expected placements"] = placements
    return results

# find current records
def find_current_records(number_of_matches) -> dict:
    results = {}
    for school in runtime.CONFERENCE:
        results[school]={"wins":0,"losses":0,"unplayed":0}
    for week in runtime.CONF_SCHED:
        for match in runtime.CONF_SCHED[week]:
            home_team = match[1]
            visiting_team = match[0]
            if home_team == "Defeated":
                results[visiting_team]["wins"] += 1
            elif visiting_team == "Defeated":
                results[home_team]["wins"] += 1
            else:
                results[home_team]["unplayed"] += 1
                results[visiting_team]["unplayed"] += 1
    for school in runtime.CONFERENCE:
        results[school]["losses"] = number_of_matches - results[school]["wins"] - results[school]["unplayed"]
    standings = {}
    for school in runtime.CONFERENCE:
        wins = results[school]["wins"]
        losses = results[school]["losses"]
        percentage = float(wins) / float(wins + losses)
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
        results[school]["placement"] = standings[school]
    return results
