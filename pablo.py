from scipy.stats import norm
import runtime
import pandas as pd
import numpy as np

def find_pablo (rk_name, pablo_data):
    school_data = pablo_data[rk_name]
    rating = school_data["rating"]
    rank = school_data["rank"]
    return rating, rank

def read_pablo_data() -> tuple[dict,int,str]:
    out_data = {}
    rk_page = runtime.RKPAGE
    with open(rk_page,'r') as f:
        pablo_page = pd.read_html(f.read())
    pbl_tbl = pablo_page[0]
    hca = int(pbl_tbl.columns[0].split()[-1])
    pablo_date = str(pbl_tbl.columns[0].split()[3]) + " " + str(pbl_tbl.columns[0].split()[4])
    data = pbl_tbl.to_numpy()
    data = np.delete(data,0,0)
    for school in data:
        name = school[1]
        rank = int(school[0])
        pablo_rating = int(school[2])
        out_data[name] = {"rating":pablo_rating,"rank":rank}
    out_data["Defeated"] = {"rating":-9999,"rank":999}
    return out_data, hca, pablo_date

def pablo_odds(team_1_pablo, team_2_pablo=None, hca_flag=None, hca=None) -> float:
    if not team_2_pablo:
        team_2_pablo = 5000
    if not hca_flag:
        hca_flag = "N"
    if not hca:
        hca = 200
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