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
    df.to_csv("./csv_data/combined.csv", index = False)

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
    data = pd.read_csv("./csv_data/combined.csv", encoding = "ISO-8859-1")
    dict = pd.read_csv("./csv_data/combined.csv", encoding = "ISO-8859-1").to_dict(orient="list")
    dict["w_expected_1stServePoint%"] = []
    dict["w_expected_2ndServePoint%"] = []
    dict["l_expected_1stServePoint%"] = []
    dict["l_expected_2ndServePoint%"] = []
    for index, row in data.iterrows():
        #print (index)
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
            dict["w_expected_1stServePoint%"].append(np.average(players[wKey]["1stIn%"]) * (np.average(players[wKey]["1stWin%"]) + np.average(players[lKey]["Def1st%"])) / 2)
            dict["w_expected_2ndServePoint%"].append(np.average(players[wKey]["2ndIn%"]) * (np.average(players[wKey]["2ndWin%"]) + np.average(players[lKey]["Def2nd%"])) / 2)
            dict["l_expected_1stServePoint%"].append(np.average(players[lKey]["1stIn%"]) * (np.average(players[lKey]["1stWin%"]) + np.average(players[wKey]["Def1st%"])) / 2)
            dict["l_expected_2ndServePoint%"].append(np.average(players[lKey]["2ndIn%"]) * (np.average(players[lKey]["2ndWin%"]) + np.average(players[wKey]["Def2nd%"])) / 2)
        else:
            if (not wFound):
                print (hp.cleanBetName(row["Winner"]))
            if (not lFound):
                print (hp.cleanBetName(row["Loser"]))
            dict["w_expected_1stServePoint%"].append(np.nan)
            dict["w_expected_2ndServePoint%"].append(np.nan)
            dict["l_expected_1stServePoint%"].append(np.nan)
            dict["l_expected_2ndServePoint%"].append(np.nan)
        if (not wFound):
            name = hp.cleanBetName(row["Winner"])[0] + " "
            for letter in hp.cleanBetName(row["Winner"])[1]:
                if (letter == ""):
                    break
                name = name + letter + "."
            wKey = name
            players[wKey] = {"1stWin%":[],"1stIn%":[],"2ndWin%":[],"2ndIn%":[],"Def1st%":[],"Def2nd%":[]}
        if (not lFound):
            name = hp.cleanBetName(row["Loser"])[0] + " "
            for letter in hp.cleanBetName(row["Loser"])[1]:
                if (letter == ""):
                    break
                name = name + letter + "."
            lKey = name
            players[lKey] = {"1stWin%":[],"1stIn%":[],"2ndWin%":[],"2ndIn%":[],"Def1st%":[],"Def2nd%":[]}
        if (row["w_svpt"] > 20 and row["l_svpt"] > 20 and row["w_svpt"] - row["w_1stIn"] - row["w_df"] > 0 and row["l_svpt"] - row["l_1stIn"] - row["l_df"] > 0):
            players[wKey]["1stWin%"].append(row["w_1stWon"] / row["w_1stIn"])
            players[wKey]["1stIn%"].append(row["w_1stIn"] / row["w_svpt"])
            players[wKey]["2ndWin%"].append(row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]))
            players[wKey]["2ndIn%"].append((row["w_svpt"] - row["w_1stIn"] - row["w_df"]) / (row["w_svpt"] - row["w_1stIn"]))
            players[wKey]["Def1st%"].append(1 - (row["l_1stWon"] / row["l_1stIn"]))
            players[wKey]["Def2nd%"].append(1 - (row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])))

            players[lKey]["1stWin%"].append(row["l_1stWon"] / row["l_1stIn"])
            players[lKey]["1stIn%"].append(row["l_1stIn"] / row["l_svpt"])
            players[lKey]["2ndWin%"].append(row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]))
            players[lKey]["2ndIn%"].append((row["l_svpt"] - row["l_1stIn"] - row["l_df"]) / (row["l_svpt"] - row["l_1stIn"]))
            players[lKey]["Def1st%"].append(1 - (row["w_1stWon"] / row["w_1stIn"]))
            players[lKey]["Def2nd%"].append(1 - (row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])))
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

#def logistic_regression():
