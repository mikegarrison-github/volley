from scipy.stats import norm
from pablo import pablo_odds

stanford = 7405
washington = 6980

print("S at Stanford: "+str(pablo_odds(stanford,washington,"H")))
print("S at Washington: "+str(pablo_odds(stanford,washington,"A")))
print("W at Stanford: "+str(pablo_odds(washington,stanford,"A")))
print("W at Washington: "+str(pablo_odds(washington,stanford,"H")))
print("Washington neutral v average team: "+str(pablo_odds(washington)))