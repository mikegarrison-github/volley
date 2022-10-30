from scipy.stats import norm
import runtime

hca = runtime.HCA

def pablo_odds(team_1_pablo, team_2_pablo=None, hca_flag=None) -> float:
    if not team_2_pablo:
        team_2_pablo = 5000
    if not hca_flag:
        hca_flag = "N"
    if hca_flag == "H":
        team_1_pablo_adj = team_1_pablo + hca
    else:
        team_1_pablo_adj = team_1_pablo
    if hca_flag == "A":
        team_2_pablo_adj = team_2_pablo + hca
    else:
        team_2_pablo_adj = team_2_pablo
    difference = float(team_1_pablo_adj - team_2_pablo_adj)
    team_1_prob = norm.cdf(difference/1000)
    return team_1_prob