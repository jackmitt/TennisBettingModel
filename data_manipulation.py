import pandas as pd
import numpy as np
import helpers as hp
import datetime
import random
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

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
    df.to_csv("./csv_data/combined.csv", index = False)

def pre_match_stats():
    data = pd.read_csv("./csv_data/combined.csv", encoding = "ISO-8859-1")
    win1 = []
    win2 = []
    in1 = []
    in2 = []
    for index, row in data.iterrows():
        if (row["Date"].split("/")[2] == "2015"):
            break
        if (np.isnan(row["w_1stWon"])):
            continue
        if (row["w_svpt"] > 30 and row["l_svpt"] > 30 and row["w_svpt"] - row["w_1stIn"] - row["w_df"] > 0 and row["l_svpt"] - row["l_1stIn"] - row["l_df"] > 0):
            win1.append(row["w_1stWon"] / row["w_1stIn"])
            win1.append(row["l_1stWon"] / row["l_1stIn"])
            win2.append(row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]))
            win2.append(row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]))
            in1.append(row["w_1stIn"] / row["w_svpt"])
            in1.append(row["l_1stIn"] / row["l_svpt"])
            in2.append((row["w_svpt"] - row["w_1stIn"] - row["w_df"]) / (row["w_svpt"] - row["w_1stIn"]))
            in2.append((row["l_svpt"] - row["l_1stIn"] - row["l_df"]) / (row["l_svpt"] - row["l_1stIn"]))
    win1avg = np.average(win1)
    win2avg = np.average(win2)
    win1std = np.std(win1)
    win2std = np.std(win2)
    in1avg = np.average(in1)
    in2avg = np.average(in2)
    in1std = np.std(in1)
    in2std = np.std(in2)
    naiveWin1 = win1avg - 0.1*win1std
    naiveWin2 = win2avg - 0.1*win2std
    naiveIn1 = in1avg - 0.1*in1std
    naiveIn2 = in2avg - 0.1*in2std
    players = {}
    for year in range(1991, 2000):
        stats = pd.read_csv("C:/Users/JackMitt/Documents/tennis_atp/atp_matches_" + str(year) + ".csv", encoding = "ISO-8859-1")
        for index, row in stats.iterrows():
            print (index, year)
            if (hp.last_f_convert(row["winner_name"]) not in players):
                players[hp.last_f_convert(row["winner_name"])] = {"1stWin%":[],"1stIn%":[],"2ndWin%":[],"2ndIn%":[],"Def1st%":[],"Def2nd%":[],"1stWin%Adj":[],"2ndWin%Adj":[],"Def1st%Adj":[],"Def2nd%Adj":[]}
            if (hp.last_f_convert(row["loser_name"]) not in players):
                players[hp.last_f_convert(row["loser_name"])] = {"1stWin%":[],"1stIn%":[],"2ndWin%":[],"2ndIn%":[],"Def1st%":[],"Def2nd%":[],"1stWin%Adj":[],"2ndWin%Adj":[],"Def1st%Adj":[],"Def2nd%Adj":[]}
            if (row["w_svpt"] > 20 and row["l_svpt"] > 20 and row["w_svpt"] - row["w_1stIn"] - row["w_df"] > 0):
                if (len(players[hp.last_f_convert(row["loser_name"])]["1stWin%"]) > 0):
                    players[hp.last_f_convert(row["winner_name"])]["1stWin%Adj"].append(((row["w_1stWon"] / row["w_1stIn"] - win1avg) / win1std) - ((np.average(players[hp.last_f_convert(row["loser_name"])]["Def1st%"]) - win1avg) / win1std))
                    players[hp.last_f_convert(row["winner_name"])]["2ndWin%Adj"].append(((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]) - win2avg) / win2std) - ((np.average(players[hp.last_f_convert(row["loser_name"])]["Def2nd%"]) - win2avg) / win2std))
                    players[hp.last_f_convert(row["winner_name"])]["Def1st%Adj"].append((((row["l_1stWon"] / row["l_1stIn"]) - win1avg) / win1std) - ((np.average(players[hp.last_f_convert(row["loser_name"])]["1stWin%"]) - win1avg) / win1std))
                    players[hp.last_f_convert(row["winner_name"])]["Def2nd%Adj"].append((((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])) - win2avg) / win2std) - ((np.average(players[hp.last_f_convert(row["loser_name"])]["2ndWin%"]) - win2avg) / win2std))
                else:
                    players[hp.last_f_convert(row["winner_name"])]["1stWin%Adj"].append(((row["w_1stWon"] / row["w_1stIn"] - win1avg) / win1std))
                    players[hp.last_f_convert(row["winner_name"])]["2ndWin%Adj"].append(((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]) - win2avg) / win2std))
                    players[hp.last_f_convert(row["winner_name"])]["Def1st%Adj"].append((((row["l_1stWon"] / row["l_1stIn"]) - win1avg) / win1std))
                    players[hp.last_f_convert(row["winner_name"])]["Def2nd%Adj"].append((((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])) - win2avg) / win2std))

                if (len(players[hp.last_f_convert(row["winner_name"])]["1stWin%"]) > 0):
                    players[hp.last_f_convert(row["loser_name"])]["1stWin%Adj"].append(((row["l_1stWon"] / row["l_1stIn"] - win1avg) / win1std) - ((np.average(players[hp.last_f_convert(row["winner_name"])]["Def1st%"]) - win1avg) / win1std))
                    players[hp.last_f_convert(row["loser_name"])]["2ndWin%Adj"].append(((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]) - win2avg) / win2std) - ((np.average(players[hp.last_f_convert(row["winner_name"])]["Def2nd%"]) - win2avg) / win2std))
                    players[hp.last_f_convert(row["loser_name"])]["Def1st%Adj"].append((((row["w_1stWon"] / row["w_1stIn"]) - win1avg) / win1std) - ((np.average(players[hp.last_f_convert(row["winner_name"])]["1stWin%"]) - win1avg) / win1std))
                    players[hp.last_f_convert(row["loser_name"])]["Def2nd%Adj"].append((((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])) - win2avg) / win2std) - ((np.average(players[hp.last_f_convert(row["winner_name"])]["2ndWin%"]) - win2avg) / win2std))
                else:
                    players[hp.last_f_convert(row["loser_name"])]["1stWin%Adj"].append(((row["l_1stWon"] / row["l_1stIn"] - win1avg) / win1std))
                    players[hp.last_f_convert(row["loser_name"])]["2ndWin%Adj"].append(((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]) - win2avg) / win2std))
                    players[hp.last_f_convert(row["loser_name"])]["Def1st%Adj"].append((((row["w_1stWon"] / row["w_1stIn"]) - win1avg) / win1std))
                    players[hp.last_f_convert(row["loser_name"])]["Def2nd%Adj"].append((((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])) - win2avg) / win2std))

                players[hp.last_f_convert(row["winner_name"])]["1stWin%"].append(row["w_1stWon"] / row["w_1stIn"])
                players[hp.last_f_convert(row["winner_name"])]["1stIn%"].append(row["w_1stIn"] / row["w_svpt"])
                players[hp.last_f_convert(row["winner_name"])]["2ndWin%"].append(row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]))
                players[hp.last_f_convert(row["winner_name"])]["2ndIn%"].append((row["w_svpt"] - row["w_1stIn"] - row["w_df"]) / (row["w_svpt"] - row["w_1stIn"]))
                players[hp.last_f_convert(row["winner_name"])]["Def1st%"].append((row["l_1stWon"] / row["l_1stIn"]))
                players[hp.last_f_convert(row["winner_name"])]["Def2nd%"].append((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])))
                #players[hp.last_f_convert(row["winner_name"])]["Date"].append(datetime.date(int(str(row["tourney_date"])[:4]), int(str(row["tourney_date"])[4:6]), int(str(row["tourney_date"])[6:8])))

                players[hp.last_f_convert(row["loser_name"])]["1stWin%"].append(row["l_1stWon"] / row["l_1stIn"])
                players[hp.last_f_convert(row["loser_name"])]["1stIn%"].append(row["l_1stIn"] / row["l_svpt"])
                players[hp.last_f_convert(row["loser_name"])]["2ndWin%"].append(row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]))
                players[hp.last_f_convert(row["loser_name"])]["2ndIn%"].append((row["l_svpt"] - row["l_1stIn"] - row["l_df"]) / (row["l_svpt"] - row["l_1stIn"]))
                players[hp.last_f_convert(row["loser_name"])]["Def1st%"].append((row["w_1stWon"] / row["w_1stIn"]))
                players[hp.last_f_convert(row["loser_name"])]["Def2nd%"].append((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])))
                #players[hp.last_f_convert(row["loser_name"])]["Date"].append(datetime.date(int(str(row["tourney_date"])[:4]), int(str(row["tourney_date"])[4:6]), int(str(row["tourney_date"])[6:8])))
    play = {"players":[]}
    for key in players:
        play["players"].append(key)
    df = pd.DataFrame.from_dict(play)
    df.to_csv("./players.csv", index = False)
    data = pd.read_csv("./csv_data/combined.csv", encoding = "ISO-8859-1")
    dict = pd.read_csv("./csv_data/combined.csv", encoding = "ISO-8859-1").to_dict(orient="list")
    dict["w_expected_1stServePoint%"] = []
    dict["w_expected_2ndServePoint%"] = []
    dict["l_expected_1stServePoint%"] = []
    dict["l_expected_2ndServePoint%"] = []
    dict["w_adj_expected_1stServePoint%"] = []
    dict["w_adj_expected_2ndServePoint%"] = []
    dict["l_adj_expected_1stServePoint%"] = []
    dict["l_adj_expected_2ndServePoint%"] = []
    for index, row in data.iterrows():
        print (index)
        wFound = False
        lFound = False
        wKey = ""
        lKey = ""
        for key in players:
            if (hp.cleanBetName(row["Winner"])[0] in key and hp.cleanBetName(row["Winner"])[1][0] + "." in key):
                wFound = True
                wKey = key
            if (hp.cleanBetName(row["Loser"])[0] in key and hp.cleanBetName(row["Loser"])[1][0] + "." in key):
                lFound = True
                lKey = key
        if (wFound and lFound):
            if (len(players[wKey]["1stIn%"]) < 10):
                w_1st_in = (len(players[wKey]["1stIn%"]) * np.average(players[wKey]["1stIn%"]) + (10 - len(players[wKey]["1stIn%"])) * naiveIn1) / 10
                w_2nd_in = (len(players[wKey]["2ndIn%"]) * np.average(players[wKey]["2ndIn%"]) + (10 - len(players[wKey]["2ndIn%"])) * naiveIn2) / 10
                w_1st_win = (len(players[wKey]["1stWin%"]) * np.average(players[wKey]["1stWin%"]) + (10 - len(players[wKey]["1stWin%"])) * naiveWin1) / 10
                w_2nd_win = (len(players[wKey]["2ndWin%"]) * np.average(players[wKey]["2ndWin%"]) + (10 - len(players[wKey]["2ndWin%"])) * naiveWin2) / 10
                w_1st_def = (len(players[wKey]["Def1st%"]) * np.average(players[wKey]["Def1st%"]) - (10 - len(players[wKey]["Def1st%"])) * naiveWin1) / 10
                w_2nd_def = (len(players[wKey]["Def2nd%"]) * np.average(players[wKey]["Def2nd%"]) - (10 - len(players[wKey]["Def2nd%"])) * naiveWin2) / 10
                w_adj_1st_win = (len(players[wKey]["1stWin%Adj"]) * np.average(players[wKey]["1stWin%Adj"]) + (10 - len(players[wKey]["1stWin%Adj"])) * -0.1) / 10
                w_adj_2nd_win = (len(players[wKey]["2ndWin%Adj"]) * np.average(players[wKey]["2ndWin%Adj"]) + (10 - len(players[wKey]["2ndWin%Adj"])) * -0.1) / 10
                w_adj_1st_def = (len(players[wKey]["Def1st%Adj"]) * np.average(players[wKey]["Def1st%Adj"]) - (10 - len(players[wKey]["Def1st%Adj"])) * -0.1) / 10
                w_adj_2nd_def = (len(players[wKey]["Def2nd%Adj"]) * np.average(players[wKey]["Def2nd%Adj"]) - (10 - len(players[wKey]["Def2nd%Adj"])) * -0.1) / 10
            else:
                w_1st_in = np.average(players[wKey]["1stIn%"])
                w_2nd_in = np.average(players[wKey]["2ndIn%"])
                w_1st_win = np.average(players[wKey]["1stWin%"])
                w_2nd_win = np.average(players[wKey]["2ndWin%"])
                w_1st_def = np.average(players[wKey]["Def1st%"])
                w_2nd_def = np.average(players[wKey]["Def2nd%"])
                w_adj_1st_win = np.average(players[wKey]["1stWin%Adj"])
                w_adj_2nd_win = np.average(players[wKey]["2ndWin%Adj"])
                w_adj_1st_def = np.average(players[wKey]["Def1st%Adj"])
                w_adj_2nd_def = np.average(players[wKey]["Def2nd%Adj"])
            if (len(players[lKey]["1stIn%"]) < 10):
                l_1st_in = (len(players[lKey]["1stIn%"]) * np.average(players[lKey]["1stIn%"]) + (10 - len(players[lKey]["1stIn%"])) * naiveIn1) / 10
                l_2nd_in = (len(players[lKey]["2ndIn%"]) * np.average(players[lKey]["2ndIn%"]) + (10 - len(players[lKey]["2ndIn%"])) * naiveIn2) / 10
                l_1st_win = (len(players[lKey]["1stWin%"]) * np.average(players[lKey]["1stWin%"]) + (10 - len(players[lKey]["1stWin%"])) * naiveWin1) / 10
                l_2nd_win = (len(players[lKey]["2ndWin%"]) * np.average(players[lKey]["2ndWin%"]) + (10 - len(players[lKey]["2ndWin%"])) * naiveWin2) / 10
                l_1st_def = (len(players[lKey]["Def1st%"]) * np.average(players[lKey]["Def1st%"]) - (10 - len(players[lKey]["Def1st%"])) * naiveWin1) / 10
                l_2nd_def = (len(players[lKey]["Def2nd%"]) * np.average(players[lKey]["Def2nd%"]) - (10 - len(players[lKey]["Def2nd%"])) * naiveWin2) / 10
                l_adj_1st_win = (len(players[lKey]["1stWin%Adj"]) * np.average(players[lKey]["1stWin%Adj"]) + (10 - len(players[lKey]["1stWin%Adj"])) * -0.1) / 10
                l_adj_2nd_win = (len(players[lKey]["2ndWin%Adj"]) * np.average(players[lKey]["2ndWin%Adj"]) + (10 - len(players[lKey]["2ndWin%Adj"])) * -0.1) / 10
                l_adj_1st_def = (len(players[lKey]["Def1st%Adj"]) * np.average(players[lKey]["Def1st%Adj"]) - (10 - len(players[lKey]["Def1st%Adj"])) * -0.1) / 10
                l_adj_2nd_def = (len(players[lKey]["Def2nd%Adj"]) * np.average(players[lKey]["Def2nd%Adj"]) - (10 - len(players[lKey]["Def2nd%Adj"])) * -0.1) / 10
            else:
                l_1st_in = np.average(players[lKey]["1stIn%"])
                l_2nd_in = np.average(players[lKey]["2ndIn%"])
                l_1st_win = np.average(players[lKey]["1stWin%"])
                l_2nd_win = np.average(players[lKey]["2ndWin%"])
                l_1st_def = np.average(players[lKey]["Def1st%"])
                l_2nd_def = np.average(players[lKey]["Def2nd%"])
                l_adj_1st_win = np.average(players[lKey]["1stWin%Adj"])
                l_adj_2nd_win = np.average(players[lKey]["2ndWin%Adj"])
                l_adj_1st_def = np.average(players[lKey]["Def1st%Adj"])
                l_adj_2nd_def = np.average(players[lKey]["Def2nd%Adj"])

            dict["w_expected_1stServePoint%"].append(w_1st_in * (w_1st_win + l_1st_def) / 2)
            dict["w_expected_2ndServePoint%"].append(w_2nd_in * (w_2nd_win + l_2nd_def) / 2)
            dict["l_expected_1stServePoint%"].append(l_1st_in * (l_1st_win + w_1st_def) / 2)
            dict["l_expected_2ndServePoint%"].append(l_2nd_in * (l_2nd_win + w_2nd_def) / 2)
            dict["w_adj_expected_1stServePoint%"].append(w_1st_in * (w_adj_1st_win + l_adj_1st_def))
            dict["w_adj_expected_2ndServePoint%"].append(w_2nd_in * (w_adj_2nd_win + l_adj_2nd_def))
            dict["l_adj_expected_1stServePoint%"].append(l_1st_in * (l_adj_1st_win + w_adj_1st_def))
            dict["l_adj_expected_2ndServePoint%"].append(l_2nd_in * (l_adj_2nd_win + w_adj_2nd_def))
        else:
            if (not wFound):
                print (hp.cleanBetName(row["Winner"]))
            if (not lFound):
                print (hp.cleanBetName(row["Loser"]))
            dict["w_expected_1stServePoint%"].append(np.nan)
            dict["w_expected_2ndServePoint%"].append(np.nan)
            dict["l_expected_1stServePoint%"].append(np.nan)
            dict["l_expected_2ndServePoint%"].append(np.nan)
            dict["w_adj_expected_1stServePoint%"].append(np.nan)
            dict["w_adj_expected_2ndServePoint%"].append(np.nan)
            dict["l_adj_expected_1stServePoint%"].append(np.nan)
            dict["l_adj_expected_2ndServePoint%"].append(np.nan)
        if (not wFound):
            name = hp.cleanBetName(row["Winner"])[0] + " "
            for letter in hp.cleanBetName(row["Winner"])[1]:
                if (letter == ""):
                    break
                name = name + letter + "."
            wKey = name
            players[wKey] = {"1stWin%":[],"1stIn%":[],"2ndWin%":[],"2ndIn%":[],"Def1st%":[],"Def2nd%":[],"1stWin%Adj":[],"2ndWin%Adj":[],"Def1st%Adj":[],"Def2nd%Adj":[]}
        if (not lFound):
            name = hp.cleanBetName(row["Loser"])[0] + " "
            for letter in hp.cleanBetName(row["Loser"])[1]:
                if (letter == ""):
                    break
                name = name + letter + "."
            lKey = name
            players[lKey] = {"1stWin%":[],"1stIn%":[],"2ndWin%":[],"2ndIn%":[],"Def1st%":[],"Def2nd%":[],"1stWin%Adj":[],"2ndWin%Adj":[],"Def1st%Adj":[],"Def2nd%Adj":[]}
        if (row["w_svpt"] > 20 and row["l_svpt"] > 20 and row["w_svpt"] - row["w_1stIn"] - row["w_df"] > 0 and row["l_svpt"] - row["l_1stIn"] - row["l_df"] > 0):
            if (len(players[lKey]["1stWin%"]) > 0):
                players[wKey]["1stWin%Adj"].append(((row["w_1stWon"] / row["w_1stIn"] - win1avg) / win1std) - ((np.average(players[lKey]["Def1st%"]) - win1avg) / win1std))
                players[wKey]["2ndWin%Adj"].append(((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]) - win2avg) / win2std) - ((np.average(players[lKey]["Def2nd%"]) - win2avg) / win2std))
                players[wKey]["Def1st%Adj"].append((((row["l_1stWon"] / row["l_1stIn"]) - win1avg) / win1std) - ((np.average(players[lKey]["1stWin%"]) - win1avg) / win1std))
                players[wKey]["Def2nd%Adj"].append((((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])) - win2avg) / win2std) - ((np.average(players[lKey]["2ndWin%"]) - win2avg) / win2std))
            else:
                players[wKey]["1stWin%Adj"].append(((row["w_1stWon"] / row["w_1stIn"] - win1avg) / win1std))
                players[wKey]["2ndWin%Adj"].append(((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]) - win2avg) / win2std))
                players[wKey]["Def1st%Adj"].append((((row["l_1stWon"] / row["l_1stIn"]) - win1avg) / win1std))
                players[wKey]["Def2nd%Adj"].append((((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])) - win2avg) / win2std))

            if (len(players[wKey]["1stWin%"]) > 0):
                players[lKey]["1stWin%Adj"].append(((row["l_1stWon"] / row["l_1stIn"] - win1avg) / win1std) - ((np.average(players[wKey]["Def1st%"]) - win1avg) / win1std))
                players[lKey]["2ndWin%Adj"].append(((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]) - win2avg) / win2std) - ((np.average(players[wKey]["Def2nd%"]) - win2avg) / win2std))
                players[lKey]["Def1st%Adj"].append((((row["w_1stWon"] / row["w_1stIn"]) - win1avg) / win1std) - ((np.average(players[wKey]["1stWin%"]) - win1avg) / win1std))
                players[lKey]["Def2nd%Adj"].append((((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])) - win2avg) / win2std) - ((np.average(players[wKey]["2ndWin%"]) - win2avg) / win2std))
            else:
                players[lKey]["1stWin%Adj"].append(((row["l_1stWon"] / row["l_1stIn"] - win1avg) / win1std))
                players[lKey]["2ndWin%Adj"].append(((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]) - win2avg) / win2std))
                players[lKey]["Def1st%Adj"].append((((row["w_1stWon"] / row["w_1stIn"]) - win1avg) / win1std))
                players[lKey]["Def2nd%Adj"].append((((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])) - win2avg) / win2std))

            players[wKey]["1stWin%"].append(row["w_1stWon"] / row["w_1stIn"])
            players[wKey]["1stIn%"].append(row["w_1stIn"] / row["w_svpt"])
            players[wKey]["2ndWin%"].append(row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]))
            players[wKey]["2ndIn%"].append((row["w_svpt"] - row["w_1stIn"] - row["w_df"]) / (row["w_svpt"] - row["w_1stIn"]))
            players[wKey]["Def1st%"].append((row["l_1stWon"] / row["l_1stIn"]))
            players[wKey]["Def2nd%"].append((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])))

            players[lKey]["1stWin%"].append(row["l_1stWon"] / row["l_1stIn"])
            players[lKey]["1stIn%"].append(row["l_1stIn"] / row["l_svpt"])
            players[lKey]["2ndWin%"].append(row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]))
            players[lKey]["2ndIn%"].append((row["l_svpt"] - row["l_1stIn"] - row["l_df"]) / (row["l_svpt"] - row["l_1stIn"]))
            players[lKey]["Def1st%"].append((row["w_1stWon"] / row["w_1stIn"]))
            players[lKey]["Def2nd%"].append((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])))
    df = pd.DataFrame.from_dict(dict)
    df.to_csv("./csv_data/preMatchExpectations.csv", index = False)

def train_test_split(splitYear = 2015):
    data = pd.read_csv("./csv_data/preMatchExpectations.csv", encoding = "ISO-8859-1")
    test = False
    trainRows = []
    testRows = []
    for index, row in data.iterrows():
        if (int(row["Date"].split("/")[2]) == splitYear):
            test = True
        if (test and not np.isnan(row["w_expected_1stServePoint%"]) and row["Comment"] == "Completed"):
            testRows.append(index)
        elif (not test and not np.isnan(row["w_expected_1stServePoint%"]) and row["Comment"] == "Completed"):
            trainRows.append(index)
    data.iloc[trainRows].to_csv("./csv_data/preMatchExpectations_train.csv", index = False)
    data.iloc[testRows].to_csv("./csv_data/preMatchExpectations_test.csv", index = False)

def logistic_regression():
    train = pd.read_csv("./csv_data/preMatchExpectations_train.csv", encoding = "ISO-8859-1")
    test = pd.read_csv("./csv_data/preMatchExpectations_test.csv", encoding = "ISO-8859-1")

    dict = {"Player 1":[], "Player 2":[], "p1_expected_1stServePoint%":[], "p1_expected_2ndServePoint%":[], "p2_expected_1stServePoint%":[], "p2_expected_2ndServePoint%":[], "p1_adj_expected_1stServePoint%":[], "p1_adj_expected_2ndServePoint%":[], "p2_adj_expected_1stServePoint%":[], "p2_adj_expected_2ndServePoint%":[], "Player 1 Odds":[], "Player 2 Odds":[], "Player 1 Win":[]}

    for index, row in train.iterrows():
        num = random.randint(0,1)
        if (num == 0):
            dict["Player 1"].append(row["Winner"])
            dict["Player 2"].append(row["Loser"])
            dict["p1_expected_1stServePoint%"].append(row["w_expected_1stServePoint%"])
            dict["p1_expected_2ndServePoint%"].append(row["w_expected_2ndServePoint%"])
            dict["p2_expected_1stServePoint%"].append(row["l_expected_1stServePoint%"])
            dict["p2_expected_2ndServePoint%"].append(row["l_expected_2ndServePoint%"])
            dict["p1_adj_expected_1stServePoint%"].append(row["w_adj_expected_1stServePoint%"])
            dict["p1_adj_expected_2ndServePoint%"].append(row["w_adj_expected_2ndServePoint%"])
            dict["p2_adj_expected_1stServePoint%"].append(row["l_adj_expected_1stServePoint%"])
            dict["p2_adj_expected_2ndServePoint%"].append(row["l_adj_expected_2ndServePoint%"])
            dict["Player 1 Odds"].append(row["PSW"])
            dict["Player 2 Odds"].append(row["PSL"])
            dict["Player 1 Win"].append(1)
        elif (num == 1):
            dict["Player 2"].append(row["Winner"])
            dict["Player 1"].append(row["Loser"])
            dict["p2_expected_1stServePoint%"].append(row["w_expected_1stServePoint%"])
            dict["p2_expected_2ndServePoint%"].append(row["w_expected_2ndServePoint%"])
            dict["p1_expected_1stServePoint%"].append(row["l_expected_1stServePoint%"])
            dict["p1_expected_2ndServePoint%"].append(row["l_expected_2ndServePoint%"])
            dict["p2_adj_expected_1stServePoint%"].append(row["w_adj_expected_1stServePoint%"])
            dict["p2_adj_expected_2ndServePoint%"].append(row["w_adj_expected_2ndServePoint%"])
            dict["p1_adj_expected_1stServePoint%"].append(row["l_adj_expected_1stServePoint%"])
            dict["p1_adj_expected_2ndServePoint%"].append(row["l_adj_expected_2ndServePoint%"])
            dict["Player 2 Odds"].append(row["PSW"])
            dict["Player 1 Odds"].append(row["PSL"])
            dict["Player 1 Win"].append(0)
    for key in dict:
        train[key] = dict[key]

    dict = {"Player 1":[], "Player 2":[], "p1_expected_1stServePoint%":[], "p1_expected_2ndServePoint%":[], "p2_expected_1stServePoint%":[], "p2_expected_2ndServePoint%":[], "p1_adj_expected_1stServePoint%":[], "p1_adj_expected_2ndServePoint%":[], "p2_adj_expected_1stServePoint%":[], "p2_adj_expected_2ndServePoint%":[], "Player 1 Odds":[], "Player 2 Odds":[], "Player 1 Win":[]}

    for index, row in test.iterrows():
        num = random.randint(0,1)
        if (num == 0):
            dict["Player 1"].append(row["Winner"])
            dict["Player 2"].append(row["Loser"])
            dict["p1_expected_1stServePoint%"].append(row["w_expected_1stServePoint%"])
            dict["p1_expected_2ndServePoint%"].append(row["w_expected_2ndServePoint%"])
            dict["p2_expected_1stServePoint%"].append(row["l_expected_1stServePoint%"])
            dict["p2_expected_2ndServePoint%"].append(row["l_expected_2ndServePoint%"])
            dict["p1_adj_expected_1stServePoint%"].append(row["w_adj_expected_1stServePoint%"])
            dict["p1_adj_expected_2ndServePoint%"].append(row["w_adj_expected_2ndServePoint%"])
            dict["p2_adj_expected_1stServePoint%"].append(row["l_adj_expected_1stServePoint%"])
            dict["p2_adj_expected_2ndServePoint%"].append(row["l_adj_expected_2ndServePoint%"])
            dict["Player 1 Odds"].append(row["PSW"])
            dict["Player 2 Odds"].append(row["PSL"])
            dict["Player 1 Win"].append(1)
        elif (num == 1):
            dict["Player 2"].append(row["Winner"])
            dict["Player 1"].append(row["Loser"])
            dict["p2_expected_1stServePoint%"].append(row["w_expected_1stServePoint%"])
            dict["p2_expected_2ndServePoint%"].append(row["w_expected_2ndServePoint%"])
            dict["p1_expected_1stServePoint%"].append(row["l_expected_1stServePoint%"])
            dict["p1_expected_2ndServePoint%"].append(row["l_expected_2ndServePoint%"])
            dict["p2_adj_expected_1stServePoint%"].append(row["w_adj_expected_1stServePoint%"])
            dict["p2_adj_expected_2ndServePoint%"].append(row["w_adj_expected_2ndServePoint%"])
            dict["p1_adj_expected_1stServePoint%"].append(row["l_adj_expected_1stServePoint%"])
            dict["p1_adj_expected_2ndServePoint%"].append(row["l_adj_expected_2ndServePoint%"])
            dict["Player 2 Odds"].append(row["PSW"])
            dict["Player 1 Odds"].append(row["PSL"])
            dict["Player 1 Win"].append(0)
    for key in dict:
        test[key] = dict[key]

    predictions = []
    y_train = train["Player 1 Win"]
    xCols = ["p1_expected_1stServePoint%", "p1_expected_2ndServePoint%", "p2_expected_1stServePoint%", "p2_expected_2ndServePoint%", "p1_adj_expected_1stServePoint%", "p1_adj_expected_2ndServePoint%", "p2_adj_expected_1stServePoint%", "p2_adj_expected_2ndServePoint%"]
    scaler = StandardScaler()
    X_train = pd.DataFrame(train, columns = xCols)
    X_train[xCols] = scaler.fit_transform(X_train[xCols])
    X_test = pd.DataFrame(test, columns = xCols)
    X_test[xCols] = scaler.transform(X_test[xCols])
    model = LogisticRegression(max_iter = 100000, C = 999999999)
    model.fit(X = X_train, y = y_train)
    for p in model.predict_proba(X_test):
        if (model.classes_[1] == 1):
            predictions.append(p[1])
        else:
            predictions.append(p[0])
    test["Player 1 Prob"] = predictions


    test.to_csv("./csv_data/predictions.csv", index = False)
