from scipy.stats import norm
import pandas as pd
import numpy as np
from datetime import date



class Team:
    def __init__(self, name=None, rating=None, rank=None, seed=None) -> None:
        if name:
            self.name = name
        else:
            self.name = "team key name"
        if rating:
            self.rating = int(rating)
        else:
            self.rating = 5000
        if rank:
            self.rank = int(rank)
        else:
            self.rank = 888
        if seed:
            self.seed = int(seed)
        else:
            self.seed = 888
        self.rk_name = "team rk name"
        self.my_name = "my team name"

    def set_names(self,my_name=None,rk_name=None) -> None:
        if my_name:
            self.my_name = my_name
        if rk_name:
            self.rk_name = rk_name

    def find_pablo(self,pablo_weekly_rating) -> tuple[int,int]:
        self.rating,self.rank = pablo_weekly_rating.find_pablo(self.rk_name)
        return self.rating,self.rank

    def chance_to_win(self,pablo_weekly_rating,other_team,HCA_flag="N") -> float:
        try:
            other_team_rating = other_team.rating
        except:
            other_team_rating = 5000
        hca = pablo_weekly_rating.hca
        if HCA_flag == "H":
            effective_rating = self.rating + hca
        elif HCA_flag == "A":
            effective_rating = self.rating - hca
        else:
            effective_rating = self.rating
        difference = float(effective_rating - other_team_rating)
        chance = norm.cdf(difference/1000)
        return chance

    def load_from_dict(self,dict_in) -> None:
        team = dict_in.get(self.name)
        if team:
            my_name = team.get("my name")
            if my_name:
                self.my_name = my_name
            rk_name = team.get("rk name")
            if rk_name:
                self.rk_name = rk_name
            rating = team.get("rating")
            if rating:
                self.rating = rating
            rank = team.get("rank")
            if rank:
                self.rank = rank
            seed = team.get("seed")
            if seed:
                self.seed = seed


class PabloWeeklyRating:
    def __init__(self,file_name="RichKern.com Pablo Rankings.html") -> None:
        self.pablo_data_dict = {}
        with open(file_name,'r') as f:
            pablo_page = pd.read_html(f.read())
        pbl_tbl = pablo_page[0]
        self.hca = int(pbl_tbl.columns[0].split()[-1])
        self.pablo_date = str(pbl_tbl.columns[0].split()[3]) + " " + str(pbl_tbl.columns[0].split()[4])
        today = date(today)
        self.run_date = today.strftime("%B %d")
        data = pbl_tbl.to_numpy()
        data = np.delete(data,0,0)
        for school in data:
            name = school[1]
            rank = int(school[0])
            pablo_rating = int(school[2])
            self.pablo_data_dict[name] = {"rating":pablo_rating,"rank":rank}
        self.pablo_data_dict["Defeated"] = {"rating":-9999,"rank":999}
    
    def find_pablo(self, rk_name=None) -> tuple[int,int]:
        data = self.pablo_data_dict.get(rk_name)
        if data:
            rank = int(data["rank"])
            rating = int(data["rating"])
        else:
            rank = 888
            rating = 5000
        return rating,rank
