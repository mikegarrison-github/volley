import random
import runtime
import pablo

random.seed()

NUMBER_OF_RUNS = 10000

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
for quad in runtime.BRACKET:
    for school in runtime.BRACKET[quad]:
        school_data = runtime.SCHOOLS.get(school)
        if not school_data:
            raise ValueError("No data found for school: "+str(school)+" in quad: "+str(quad))


# run tournament
for i in range(NUMBER_OF_RUNS):
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
   
    pass


    