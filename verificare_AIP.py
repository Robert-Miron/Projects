import requests
from bs4 import BeautifulSoup
import pandas as pd

lista = ['6', '7', '8', '9', '10', '11', '12']
data_list = []
for i in lista:
    r = requests.get("https://flightplan.romatsa.ro/aixm45/aixm/manage/DesignatedPoint/DesignatedPoint?page=" + i)
    link = BeautifulSoup(r.text, "html.parser")  # asta contine tot html-ul paginii respective
    title = link.find_all('div')
    header = []
    ok = 0
    for i in title:
        for tr_index in i.find_all('table'):
            if ok == 0:
                for td_index in tr_index.find_all('tr'):
                    td_list = []
                    ok1 = 0
                    if td_index.find_all('th'):
                        header = [th_index.get_text() for th_index in td_index.find_all('th')]
                    for j, trd_index in enumerate(list(td_index.find_all('td'))):
                        td_list.append(trd_index.get_text())
                        ok1 = 1
                    if ok1 == 1:
                        data_list.append(td_list)
                    ok = 1
            else:
                break
df = pd.DataFrame(data_list, columns=header)
df.to_csv('Designated_Points_Database.xls')
print(df)
coord = pd.read_excel("Designated_Points.xls")
for i in range(len(coord.index)):
    coord.loc[i].at['LONG'] = int(coord.loc[i].at['LONG'][:-1])
    coord.loc[i].at['LAT'] = int(coord.loc[i].at['LAT'][:-1])
for i in range(len(df.index)):
    df.loc[i].at['Geolong']=int(round(float(df.loc[i].at['Geolong'][1:-1])))
    df.loc[i].at['Geolat'] =int(round(float(df.loc[i].at['Geolat'][:-1])))
k = 0
for i in range(len(df.index)):
    if df.loc[i].at['Codeid'] != coord.loc[k].at['Name']:
        print('Punctul',df.loc[i].at['Codeid'],'cu coordonatele',df.loc[i].at['Geolat'],'N si ',df.loc[i].at['Geolong'],'E nu exista in AIP')
        i+=1
    else:
        if coord.loc[k].at['LAT'] != df.loc[i].at['Geolat']:
            print("Punctul ",df.loc[i].at['Codeid'],"cu coordonatele", df.loc[i].at['Geolat'], "N si ",df.loc[i].at['Geolong'],"E are coordonatele gresite in baza de date. Ar fi trebuit sa aiba coordonatele ",coord.loc[k].at['LAT']," N si ", coord.loc[k].at['LONG'],".")
        k+=1
