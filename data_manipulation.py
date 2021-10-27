import pandas as pd
import numpy as np
import helpers as hp
import datetime

def assemble_data():
    #combine matches first
    matches = pd.read_csv("./csv_data/bettingLines.csv", encoding = "ISO-8859-1")
    dict = pd.read_csv("./csv_data/bettingLines.csv", encoding = "ISO-8859-1").to_dict(orient="list")
    stats = pd.read_csv("C:/Users/JackMitt/Documents/tennis_atp/atp_matches_2000.csv", encoding = "ISO-8859-1")
    stats = stats.sort_values(by=["tourney_date"], kind = "mergesort", ignore_index = True)
    for col in stats.columns:
        if ("w_" in col or "l_" in col):
            dict[col] = []
    for i in range(0, len(matches.index)):
        print (i, matches.at[i,"Date"].split("/")[2])
        iDate = datetime.date(int(matches.at[i,"Date"].split("/")[2]), int(matches.at[i,"Date"].split("/")[0]), int(matches.at[i,"Date"].split("/")[1]))
        if (i != 0 and (int(matches.at[i,"Date"].split("/")[2]) != int(matches.at[i-1,"Date"].split("/")[2]) or i == len(matches.index) - 1)):
            stats = pd.read_csv("C:/Users/JackMitt/Documents/tennis_atp/atp_matches_" + matches.at[i,"Date"].split("/")[2] + ".csv", encoding = "ISO-8859-1")
            stats = stats.sort_values(by=["tourney_date"], kind = "mergesort", ignore_index = True)
        toVisit = list(range(0, len(stats.index)))
        visited = False
        for j in toVisit:
            jDate = datetime.date(int(str(stats.at[j,"tourney_date"])[:4]), int(str(stats.at[j,"tourney_date"])[4:6]), int(str(stats.at[j,"tourney_date"])[6:8]))
            if (abs(jDate - iDate).days < 18 and hp.same_name(matches.at[i,"Winner"], stats.at[j,"winner_name"]) and hp.same_name(matches.at[i,"Loser"], stats.at[j,"loser_name"])):
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
    play = {"players":[]}
    for key in players:
        play["players"].append(key)
    df = pd.DataFrame.from_dict(play)
    df.to_csv("./players.csv", index = False)
    data = pd.read_csv("./combined.csv", encoding = "ISO-8859-1")
    dict = pd.read_csv("./combined.csv", encoding = "ISO-8859-1").to_dict(orient="list")
    dict["w_expected_1stServePoint%"] = []
    dict["w_expected_2ndServePoint%"] = []
    dict["l_expected_1stServePoint%"] = []
    dict["l_expected_2ndServePoint%"] = []
    for index, row in data.iterrows():
        #print (index)
        if (hp.cleanBetName(row["Winner"]) in players and hp.cleanBetName(row["Loser"]) in players):
            dict["w_expected_1stServePoint%"].append(np.average(players[hp.cleanBetName(row["Winner"])]["1stIn%"]) * (np.average(players[hp.cleanBetName(row["Winner"])]["1stWin%"]) + np.average(players[hp.cleanBetName(row["Loser"])]["Def1st%"])) / 2)
            dict["w_expected_2ndServePoint%"].append(np.average(players[hp.cleanBetName(row["Winner"])]["2ndIn%"]) * (np.average(players[hp.cleanBetName(row["Winner"])]["2ndWin%"]) + np.average(players[hp.cleanBetName(row["Loser"])]["Def2nd%"])) / 2)
            dict["l_expected_1stServePoint%"].append(np.average(players[hp.cleanBetName(row["Loser"])]["1stIn%"]) * (np.average(players[hp.cleanBetName(row["Loser"])]["1stWin%"]) + np.average(players[hp.cleanBetName(row["Winner"])]["Def1st%"])) / 2)
            dict["l_expected_2ndServePoint%"].append(np.average(players[hp.cleanBetName(row["Loser"])]["2ndIn%"]) * (np.average(players[hp.cleanBetName(row["Loser"])]["2ndWin%"]) + np.average(players[hp.cleanBetName(row["Winner"])]["Def2nd%"])) / 2)
        else:
            if (hp.cleanBetName(row["Winner"]) not in players):
                print (hp.cleanBetName(row["Winner"]))
            if (hp.cleanBetName(row["Loser"]) not in players):
                print (hp.cleanBetName(row["Loser"]))
            dict["w_expected_1stServePoint%"].append(np.nan)
            dict["w_expected_2ndServePoint%"].append(np.nan)
            dict["l_expected_1stServePoint%"].append(np.nan)
            dict["l_expected_2ndServePoint%"].append(np.nan)
        if (hp.cleanBetName(row["Winner"]) not in players):
            players[hp.cleanBetName(row["Winner"])] = {"1stWin%":[],"1stIn%":[],"2ndWin%":[],"2ndIn%":[],"Def1st%":[],"Def2nd%":[]}
        if (hp.cleanBetName(row["Loser"]) not in players):
            players[hp.cleanBetName(row["Loser"])] = {"1stWin%":[],"1stIn%":[],"2ndWin%":[],"2ndIn%":[],"Def1st%":[],"Def2nd%":[]}
        if (row["w_svpt"] > 20 and row["l_svpt"] > 20 and row["w_svpt"] - row["w_1stIn"] - row["w_df"] > 0 and row["l_svpt"] - row["l_1stIn"] - row["l_df"] > 0):
            players[hp.cleanBetName(row["Winner"])]["1stWin%"].append(row["w_1stWon"] / row["w_1stIn"])
            players[hp.cleanBetName(row["Winner"])]["1stIn%"].append(row["w_1stIn"] / row["w_svpt"])
            players[hp.cleanBetName(row["Winner"])]["2ndWin%"].append(row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]))
            players[hp.cleanBetName(row["Winner"])]["2ndIn%"].append((row["w_svpt"] - row["w_1stIn"] - row["w_df"]) / (row["w_svpt"] - row["w_1stIn"]))
            players[hp.cleanBetName(row["Winner"])]["Def1st%"].append(1 - (row["l_1stWon"] / row["l_1stIn"]))
            players[hp.cleanBetName(row["Winner"])]["Def2nd%"].append(1 - (row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])))

            players[hp.cleanBetName(row["Loser"])]["1stWin%"].append(row["l_1stWon"] / row["l_1stIn"])
            players[hp.cleanBetName(row["Loser"])]["1stIn%"].append(row["l_1stIn"] / row["l_svpt"])
            players[hp.cleanBetName(row["Loser"])]["2ndWin%"].append(row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]))
            players[hp.cleanBetName(row["Loser"])]["2ndIn%"].append((row["l_svpt"] - row["l_1stIn"] - row["l_df"]) / (row["l_svpt"] - row["l_1stIn"]))
            players[hp.cleanBetName(row["Loser"])]["Def1st%"].append(1 - (row["w_1stWon"] / row["w_1stIn"]))
            players[hp.cleanBetName(row["Loser"])]["Def2nd%"].append(1 - (row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])))
    df = pd.DataFrame.from_dict(dict)
    df.to_csv("./preMatchExpectations.csv", index = False)
