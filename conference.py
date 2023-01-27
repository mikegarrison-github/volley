import random
import runtime
import pablo
import statistics
import json
from classes import Team, PabloWeeklyRating

def read_conference_data(file) -> dict:
    conf_data = json.load(file)
    return conf_data



# # average pablo score
# def median_pablo(conf_data) -> int:
#     pablos = []
#     for school in conf_data["CONFERENCE"].items():
#         rk_name = school["rk name"]
#         rating, rank, hca, pablo_date = pablo.find_pablo(rk_name)
#         pablos.append(rating)
#     median = statistics.median(pablos)
#     return round(median)
            
# run conference
def run_conference(number_of_runs, number_of_matches, results, pablo_data, conf_data) -> dict:
    for i in range(number_of_runs):
        season_results = {}
        for week in conf_data["CONF_SCHED"]:
            for match in conf_data["CONF_SCHED"][week]:
                home_team = Team(match[1])
                visiting_team = Team(match[0])
                if home_team.name == "Defeated":
                    home_team.set_names("Defeated","Defeated")
                else:
                    home_team.set_names(conf_data["CONFERENCE"][home_team.name]["my name"],conf_data["CONFERENCE"][home_team.name]["rk name"])
                if visiting_team.name == "Defeated":
                    visiting_team.set_names("Defeated","Defeated")
                else:
                    visiting_team.set_names(conf_data["CONFERENCE"][visiting_team.name]["my name"],conf_data["CONFERENCE"][visiting_team.name]["rk name"])
                home_team.find_pablo(pablo_data)
                visiting_team.find_pablo(pablo_data)
                home_prob = home_team.chance_to_win(pablo_data,visiting_team,"H")
                score = random.random()
                if score <= home_prob:
                    wins = season_results.get(home_team.name,0)
                    season_results[home_team.name] = wins + 1
                else:
                    wins = season_results.get(visiting_team.name,0)
                    season_results[visiting_team.name] = wins + 1
        standings = {}
        for school in conf_data["CONFERENCE"]:
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
        for school in conf_data["CONFERENCE"]:
            past_results = results[school]
            wins = past_results["expected wins"]
            placements = past_results["expected placements"]
            wins.append(season_results.get(school,0))
            placements.append(standings[school])
            results[school]["expected wins"] = wins
            results[school]["expected placements"] = placements
    return results

# find current records
def find_current_records(number_of_matches, conf_data) -> dict:
    results = {}
    for school in conf_data["CONFERENCE"]:
        results[school]={"wins":0,"losses":0,"unplayed":0}
    for week in conf_data["CONF_SCHED"]:
        for match in conf_data["CONF_SCHED"][week]:
            home_team = match[1]
            visiting_team = match[0]
            if home_team == "Defeated":
                results[visiting_team]["wins"] += 1
            elif visiting_team == "Defeated":
                results[home_team]["wins"] += 1
            else:
                results[home_team]["unplayed"] += 1
                results[visiting_team]["unplayed"] += 1
    for school in conf_data["CONFERENCE"]:
        results[school]["losses"] = number_of_matches - results[school]["wins"] - results[school]["unplayed"]
    standings = {}
    for school in conf_data["CONFERENCE"]:
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
    for school in conf_data["CONFERENCE"]:
        results[school]["placement"] = standings[school]
    return results

def make_schedules_and_odds(results, hca, conf_data) -> str:
    match_text = None
    odds_text = None
    rank_text = None
    out_text = "match lines\n"
    for week in conf_data["CONF_SCHED"]:
        out_text += "Week "+str(week)+"\n"
        for match in conf_data["CONF_SCHED"][week]:
            if (match[0]!="Defeated") and (match[1]!="Defeated"):
                home_prob = pablo.pablo_odds(results[match[1]]["rating"],results[match[0]]["rating"],"H",hca)
                match_text = str(conf_data["CONFERENCE"][match[0]]["my name"])+"&#064;"+str(conf_data["CONFERENCE"][match[1]]["my name"])
                if round((home_prob)*100)>=45 and round((home_prob)*100)<=55:
                    odds_text = str(conf_data["CONFERENCE"][match[0]]["my name"])+" ("+str(round((1-home_prob)*100))+"%) @ "+str(conf_data["CONFERENCE"][match[1]]["my name"])+" ("+str(round((home_prob)*100))+"%) -- Outcome: TBD\n"
                else:
                    odds_text = None
                if results[match[0]]["rank"]<=25 and results[match[1]]["rank"]<=25:
                    rank_text = "#"+str(results[match[0]]["rank"])+" "+str(conf_data["CONFERENCE"][match[0]]["my name"])+" ("+str(round((1-home_prob)*100))+"%) @ "+"#"+str(results[match[1]]["rank"])+" "+str(conf_data["CONFERENCE"][match[1]]["my name"])+" ("+str(round((home_prob)*100))+"%) -- Outcome: TBD\n"
                else:
                    rank_text = None
            else:
                match_text = None
            if match_text:
                if rank_text:
                    match_text = '[font color="gold"]'+match_text+"[/font]\n"
                elif odds_text:
                    match_text = '[font color="red"]'+match_text+"[/font]\n"
                else:
                    match_text += "\n"
                out_text += match_text
                if odds_text:
                    out_text += odds_text
                if rank_text:
                    out_text += rank_text
    return out_text
        
