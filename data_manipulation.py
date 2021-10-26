import pandas as pd
import numpy as np
import helpers as hp

def assemble_data():
    #combine matches first
    matches = pd.read_csv("./csv_data/bettingLines.csv", encoding = "ISO-8859-1")
    dict = pd.read_csv("./csv_data/bettingLines.csv", encoding = "ISO-8859-1").to_dict(orient="list")
    stats = pd.read_csv("C:/Users/JackMitt/Documents/tennis_atp/atp_matches_2000.csv", encoding = "ISO-8859-1")
    for col in stats.columns:
        if ("w_" in col or "l_" in col):
            dict[col] = []
    for i in range(0, len(matches.index)):
        print (i, matches.at[i,"Date"].split("/")[2])
        if (i % 1000 == 1):
            for key in dict:
                print (key, len(dict[key]))
        if (i != 0 and (int(matches.at[i,"Date"].split("/")[2]) != int(matches.at[i-1,"Date"].split("/")[2]) or i == len(matches.index) - 1)):
            stats = pd.read_csv("C:/Users/JackMitt/Documents/tennis_atp/atp_matches_" + matches.at[i,"Date"].split("/")[2] + ".csv", encoding = "ISO-8859-1")
        toVisit = list(range(0, len(stats.index)))
        visited = False
        for j in toVisit:
            if ((matches.at[i,"Location"] in stats.at[j,"tourney_name"] or matches.at[i,"Tournament"] == stats.at[j,"tourney_name"]) and hp.same_name(matches.at[i,"Winner"], stats.at[j,"winner_name"]) and hp.same_name(matches.at[i,"Loser"], stats.at[j,"loser_name"])):
                visited = True
                for col in stats.columns:
                    if ("w_" in col or "l_" in col):
                        dict[col].append(stats.at[j,col])
                toVisit.remove(j)
                break
        if (not visited):
            for col in stats.columns:
                if ("w_" in col or "l_" in col):
                    dict[col].append(np.nan)
        else:
            visited = False
    df = pd.DataFrame.from_dict(dict)
    df.to_csv("./combined.csv", index = False)

def pre_match_stats():
    players = {}
    for year in range(1991, 2000):
        stats = pd.read_csv("C:/Users/JackMitt/Documents/tennis_atp/atp_matches_" + str(year) + ".csv", encoding = "ISO-8859-1")
        for index, row in stats.iterrows():
            print (index, year)
            if (hp.last_f_convert(row["winner_name"]) not in players):
                players[hp.last_f_convert(row["winner_name"])] = {"1stWin%":[],"1stIn%":[],"2ndWin%":[],"2ndIn%":[],"Def1st%":[],"Def2nd%":[]}
            if (hp.last_f_convert(row["loser_name"]) not in players):
                players[hp.last_f_convert(row["loser_name"])] = {"1stWin%":[],"1stIn%":[],"2ndWin%":[],"2ndIn%":[],"Def1st%":[],"Def2nd%":[]}
            if (row["w_svpt"] > 20 and row["l_svpt"] > 20 and row["w_svpt"] - row["w_1stIn"] - row["w_df"] > 0):
                players[hp.last_f_convert(row["winner_name"])]["1stWin%"].append(row["w_1stWon"] / row["w_1stIn"])
                players[hp.last_f_convert(row["winner_name"])]["1stIn%"].append(row["w_1stIn"] / row["w_svpt"])
                players[hp.last_f_convert(row["winner_name"])]["2ndWin%"].append(row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]))
                players[hp.last_f_convert(row["winner_name"])]["2ndIn%"].append((row["w_svpt"] - row["w_1stIn"] - row["w_df"]) / (row["w_svpt"] - row["w_1stIn"]))
                players[hp.last_f_convert(row["winner_name"])]["Def1st%"].append(1 - (row["l_1stWon"] / row["l_1stIn"]))
                players[hp.last_f_convert(row["winner_name"])]["Def2nd%"].append(1 - (row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])))

                players[hp.last_f_convert(row["loser_name"])]["1stWin%"].append(row["l_1stWon"] / row["l_1stIn"])
                players[hp.last_f_convert(row["loser_name"])]["1stIn%"].append(row["l_1stIn"] / row["l_svpt"])
                players[hp.last_f_convert(row["loser_name"])]["2ndWin%"].append(row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]))
                players[hp.last_f_convert(row["loser_name"])]["2ndIn%"].append((row["l_svpt"] - row["l_1stIn"] - row["l_df"]) / (row["l_svpt"] - row["l_1stIn"]))
                players[hp.last_f_convert(row["loser_name"])]["Def1st%"].append(1 - (row["w_1stWon"] / row["w_1stIn"]))
                players[hp.last_f_convert(row["loser_name"])]["Def2nd%"].append(1 - (row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])))

    data = pd.read_csv("./combined.csv", encoding = "ISO-8859-1")
    dict = pd.read_csv("./combined.csv", encoding = "ISO-8859-1").to_dict(orient="list")
    dict["w_expected_1stServePoint%"] = []
    dict["w_expected_2ndServePoint%"] = []
    dict["l_expected_1stServePoint%"] = []
    dict["l_expected_2ndServePoint%"] = []
    # for index, row in data.iterrows():
