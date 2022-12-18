import pandas as pd
import numpy as np

rk_page = 'RichKern.com Pablo Rankings.html'
with open(rk_page,'r') as f:
    pablo_page = pd.read_html(f.read())
pbl_tbl = pablo_page[0]
hca=pbl_tbl.columns[0].split()[-1]
pablo_date = str(pbl_tbl.columns[0].split()[3]) + " " + str(pbl_tbl.columns[0].split()[4])
print(hca)
print(pablo_date)
data = pbl_tbl.to_numpy()
data = np.delete(data,0,0)
for school in data:
    name = school[1]
    rank = school[0]
    pablo_rating = school[2]
pass