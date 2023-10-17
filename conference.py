import random
import json
from classes import Team

def read_conference_data(file) -> dict:
    conf_data = json.load(file)
    return conf_data


            
# run conference
def run_conference(number_of_runs, number_of_matches, results, pablo_data, conf_data) -> dict:
    for i in range(number_of_runs):
        season_results = {}
        for week in conf_data["CONF_SCHED"]:
            for match in conf_data["CONF_SCHED"][week]:
                home_team = Team(match.get("home"))
                visiting_team = Team(match.get("away"))
                home_team.load_from_dict(conf_data["CONFERENCE"])
                visiting_team.load_from_dict(conf_data["CONFERENCE"])
                home_team.find_pablo(pablo_data)
                visiting_team.find_pablo(pablo_data)
                winner = match.get("winner")
                if winner:
                    wins = season_results.get(winner,0)
                    season_results[winner] = wins + 1
                else:
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

# run conference
def run_past_conference(number_of_runs, number_of_matches, results, pablo_data, conf_data) -> dict:
    for i in range(number_of_runs):
        season_results = {}
        season_prob_results = {}
        for week in conf_data["CONF_SCHED"]:
            for match in conf_data["CONF_SCHED"][week]:
                home_team = Team(match.get("home"))
                visiting_team = Team(match.get("away"))
                home_team.load_from_dict(conf_data["CONFERENCE"])
                visiting_team.load_from_dict(conf_data["CONFERENCE"])
                home_team.find_pablo(pablo_data)
                visiting_team.find_pablo(pablo_data)
                winner = match.get("winner")
                if winner:
                    wins = season_results.get(winner,0)
                    season_results[winner] = wins + 1
                    home_prob = home_team.chance_to_win(pablo_data,visiting_team,"H")
                    score = random.random()
                    if score <= home_prob:
                        prob_wins = season_prob_results.get(home_team.name,0)
                        season_prob_results[home_team.name] = prob_wins + 1
                    else:
                        prob_wins = season_prob_results.get(visiting_team.name,0)
                        season_prob_results[visiting_team.name] = prob_wins + 1
        for school in conf_data["CONFERENCE"]:
            past_results = results[school]
            wins = past_results["actual wins"]
            wins.append(season_results.get(school,0))
            prob_wins = past_results["probable wins"]
            prob_wins.append(season_prob_results.get(school,0))
            results[school]["actual wins"] = wins
            results[school]["probable wins"] = prob_wins
    return results

# find current records
def find_current_records(number_of_matches, conf_data) -> dict:
    results = {}
    for school in conf_data["CONFERENCE"]:
        results[school]={"wins":0,"losses":0,"unplayed":0}
    for week in conf_data["CONF_SCHED"]:
        for match in conf_data["CONF_SCHED"][week]:
            home_team = match.get("home")
            visiting_team = match.get("away")
            winner = match.get("winner")
            if winner:
                if winner == home_team:
                    results[home_team]["wins"] += 1
                elif winner == visiting_team:
                    results[visiting_team]["wins"] += 1
                else:
                    raise ValueError("Week: "+str(week)+" Match: "+str(match)+" winner must == either home or away team if not null")
            else:
                results[home_team]["unplayed"] += 1
                results[visiting_team]["unplayed"] += 1
    for school in conf_data["CONFERENCE"]:
        results[school]["losses"] = number_of_matches - results[school]["wins"] - results[school]["unplayed"]
    standings = {}
    for school in conf_data["CONFERENCE"]:
        wins = results[school]["wins"]
        losses = results[school]["losses"]
        if (wins + losses) > 0:
            percentage = float(wins) / float(wins + losses)
        else:
            percentage = 0.0
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

def make_schedules_and_odds(results, pablo_data, conf_data) -> str:
    match_text = None
    odds_text = None
    rank_text = None
    week_flag = False
    out_text = ""
    for week in conf_data["CONF_SCHED"]:
        temp_out_text = "Week "+str(week)+"\n"
        for match in conf_data["CONF_SCHED"][week]:
            home_team = Team(match.get("home"))
            visiting_team = Team(match.get("away"))
            winner = match.get("winner")
            home_team.load_from_dict(conf_data["CONFERENCE"]) # get name info
            visiting_team.load_from_dict(conf_data["CONFERENCE"])
            home_team.load_from_dict(results) # get rank and rating
            visiting_team.load_from_dict(results)
            if not winner:
                week_flag = True
                home_prob = home_team.chance_to_win(pablo_data,visiting_team,"H")
                match_text = str(visiting_team.my_name)+"&#064;"+str(home_team.my_name)
                if round((home_prob)*100)>=45 and round((home_prob)*100)<=55:
                    odds_text = str(visiting_team.my_name)+" ("+str(round((1-home_prob)*100))+"%) @ "+str(home_team.my_name)+" ("+str(round((home_prob)*100))+"%) -- Outcome: TBD\n"
                else:
                    odds_text = None
                if visiting_team.rank<=25 and home_team.rank<=25:
                    rank_text = "#"+str(visiting_team.rank)+" "+str(visiting_team.my_name)+" ("+str(round((1-home_prob)*100))+"%) @ "+"#"+str(home_team.rank)+" "+str(home_team.my_name)+" ("+str(round((home_prob)*100))+"%) -- Outcome: TBD\n"
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
                temp_out_text += match_text
                if odds_text:
                    temp_out_text += odds_text
                if rank_text:
                    temp_out_text += rank_text
        if week_flag:
            out_text = temp_out_text
            break
    return out_text
        
