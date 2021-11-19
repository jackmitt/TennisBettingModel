import pandas as pd
import numpy as np
import helpers as hp
from helpers import player
import datetime
import random
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression

def assemble_data():
    #combine matches first
    matches = pd.read_csv("./csv_data/bettingLines.csv", encoding = "ISO-8859-1")
    dict = pd.read_csv("./csv_data/bettingLines.csv", encoding = "ISO-8859-1").to_dict(orient="list")
    stats = pd.read_csv("C:/Users/JackMitt/Documents/tennis_atp/atp_matches_2000.csv", encoding = "ISO-8859-1")
    stats = stats.sort_values(by=["tourney_date"], kind = "mergesort", ignore_index = True)
    for col in stats.columns:
        if ("w_" in col or "l_" in col or col == "minutes" or "_ht" in col or "round" in col or "_id" in col):
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
                    if ("w_" in col or "l_" in col or col == "minutes" or "_ht" in col or "round" in col) or "_id" in col:
                        dict[col].append(stats.at[j,col])
                toVisit.remove(j)
                break
        if (not visited):
            for col in stats.columns:
                if ("w_" in col or "l_" in col or col == "minutes" or "_ht" in col or "round" in col or "_id" in col):
                    dict[col].append(np.nan)
        else:
            visited = False
    df = pd.DataFrame.from_dict(dict)
    df.to_csv("./csv_data/combined.csv", index = False)

def pre_match_stats(path = "./csv_data/"):
    keys = ["1stWin%","1stIn%","2ndWin%","2ndIn%","1stRtnWin%","2ndRtnWin%","Ace%","RtnSrv%","AcePer1stIn","Df%","DfPer2ndSrv","1stSrvEff","Def1stSrvEff","SrvRating","OppSrvRating","BpSaved%","BpWon%","RtnRating","OppRtnRating","Date"]
    cats = ["lf", "mf", "sf", "hard", "clay", "grass"]
    # newWin1 = -0.394
    # newWin2 = -0.240
    # newDef1 = 0.226
    # newDef2 = 0.249
    # done = False
    # data = pd.read_csv("./csv_data/combined.csv", encoding = "ISO-8859-1")
    # surfDict = {}
    # for s in ["All","Hard","Clay","Grass"]:
    #     surfDict[s] = {"win1":[],"win2":[],"in1":[],"in2":[]}
    # for index, row in data.iterrows():
    #     if (row["Date"].split("/")[2] == "2015"):
    #         break
    #     if (np.isnan(row["w_1stWon"])):
    #         continue
    #     if (row["w_svpt"] > 30 and row["l_svpt"] > 30 and row["w_svpt"] - row["w_1stIn"] - row["w_df"] > 0 and row["l_svpt"] - row["l_1stIn"] - row["l_df"] > 0 and row["Surface"] != "Carpet"):
    #         surfDict["All"]["win1"].append(row["w_1stWon"] / row["w_1stIn"])
    #         surfDict["All"]["win1"].append(row["l_1stWon"] / row["l_1stIn"])
    #         surfDict["All"]["win2"].append(row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]))
    #         surfDict["All"]["win2"].append(row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]))
    #         surfDict["All"]["in1"].append(row["w_1stIn"] / row["w_svpt"])
    #         surfDict["All"]["in1"].append(row["l_1stIn"] / row["l_svpt"])
    #         surfDict["All"]["in2"].append((row["w_svpt"] - row["w_1stIn"] - row["w_df"]) / (row["w_svpt"] - row["w_1stIn"]))
    #         surfDict["All"]["in2"].append((row["l_svpt"] - row["l_1stIn"] - row["l_df"]) / (row["l_svpt"] - row["l_1stIn"]))
    #         surfDict[row["Surface"]]["win1"].append(row["w_1stWon"] / row["w_1stIn"])
    #         surfDict[row["Surface"]]["win1"].append(row["l_1stWon"] / row["l_1stIn"])
    #         surfDict[row["Surface"]]["win2"].append(row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]))
    #         surfDict[row["Surface"]]["win2"].append(row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]))
    #         surfDict[row["Surface"]]["in1"].append(row["w_1stIn"] / row["w_svpt"])
    #         surfDict[row["Surface"]]["in1"].append(row["l_1stIn"] / row["l_svpt"])
    #         surfDict[row["Surface"]]["in2"].append((row["w_svpt"] - row["w_1stIn"] - row["w_df"]) / (row["w_svpt"] - row["w_1stIn"]))
    #         surfDict[row["Surface"]]["in2"].append((row["l_svpt"] - row["l_1stIn"] - row["l_df"]) / (row["l_svpt"] - row["l_1stIn"]))
    # distDict = {}
    # for s in ["All","Hard","Clay","Grass"]:
    #     distDict[s] = {"win1avg":np.average(surfDict[s]["win1"]),"win2avg":np.average(surfDict[s]["win2"]),"in1avg":np.average(surfDict[s]["in1"]),"in2avg":np.average(surfDict[s]["in2"]),"win1std":np.std(surfDict[s]["win1"]),"win2std":np.std(surfDict[s]["win2"]),"in1std":np.std(surfDict[s]["in1"]),"in2std":np.std(surfDict[s]["in2"])}
    # naiveWin1 = distDict["All"]["win1avg"] - newWin1*distDict["All"]["win1std"]
    # naiveWin2 = distDict["All"]["win2avg"] - newWin2*distDict["All"]["win2std"]
    # naiveIn1 = distDict["All"]["in1avg"] - 0.1*distDict["All"]["in1std"]
    # naiveIn2 = distDict["All"]["in2avg"] - 0.1*distDict["All"]["in2std"]

    players = {}
    data = pd.read_csv("./csv_data/combined.csv", encoding = "ISO-8859-1")
    dict = pd.read_csv("./csv_data/combined.csv", encoding = "ISO-8859-1").to_dict(orient="list")
    for cat in ["lf", "mf", "sf", "surf"]:
        for key in keys:
            if ("Date" in key):
                continue
            for x in ["w_","l_"]:
                dict[x + cat + "_" + key] = []
    for index, row in data.iterrows():
        print (index)
        if (row["Surface"] == "Carpet"):
            for cat in ["lf", "mf", "sf", "surf"]:
                for key in keys:
                    if ("Date" in key):
                        continue
                    for x in ["w_","l_"]:
                        dict[x + cat + "_" + key].append(np.nan)
            continue
        wFound = False
        lFound = False
        wKey = ""
        lKey = ""
        if (row["winner_id"] in players):
            wKey = row["winner_id"]
            wFound = True
        if (row["loser_id"] in players):
            lKey = row["loser_id"]
            lFound = True



        if (wFound and lFound):
            today = datetime.date(int(row["Date"].split("/")[2]), int(row["Date"].split("/")[0]), int(row["Date"].split("/")[1]))
            #Deleting games that are more than x days old for medium form and short form
            players[wKey].update_form(today=today, med_form_days = 548, short_form_days = 182)
            for cat in ["lf", "mf", "sf", "surf"]:
                for key in keys:
                    if ("Date" in key):
                        continue
                    if (cat == "surf"):
                        dict["w_" + cat + "_" + key].append(players[wKey].get_avg(row["Surface"].lower(), key))
                    else:
                        dict["w_" + cat + "_" + key].append(players[wKey].get_avg(cat, key))
                    if (cat == "surf"):
                        dict["l_" + cat + "_" + key].append(players[lKey].get_avg(row["Surface"].lower(), key))
                    else:
                        dict["l_" + cat + "_" + key].append(players[lKey].get_avg(cat, key))
        else:
            for cat in ["lf", "mf", "sf", "surf"]:
                for key in keys:
                    if ("Date" in key):
                        continue
                    for x in ["w_","l_"]:
                        dict[x + cat + "_" + key].append(np.nan)


        if (not wFound):
            wKey = row["winner_id"]
            players[wKey] = player(keys, cats, [row["winner_id"], row["Winner"], row["winner_ht"]])
        if (not lFound):
            lKey = row["loser_id"]
            players[lKey] = player(keys, cats, [row["loser_id"], row["Loser"], row["loser_ht"]])
        if (row["w_svpt"] > 20 and row["l_svpt"] > 20 and row["w_svpt"] - row["w_1stIn"] - row["w_df"] > 0 and row["l_svpt"] - row["l_1stIn"] - row["l_df"] > 0 and row["l_1stIn"] > 0 and row["l_2ndWon"] > 0 and row["w_2ndWon"] > 0):
            players[wKey].add_match_stats(row, "w")
            players[lKey].add_match_stats(row, "l")

    df = pd.DataFrame.from_dict(dict)
    df.to_csv(path+"preMatchExpectations.csv", index = False)

def train_test_split(splitYear = 2015, path="./csv_data/"):
    data = pd.read_csv(path + "preMatchExpectations.csv", encoding = "ISO-8859-1")
    test = False
    trainRows = []
    testRows = []
    for index, row in data.iterrows():
        #Excluding first 2000, 2001, 2002 to build up stats before trying to train
        if (int(row["Date"].split("/")[2]) < 2003):
            continue
        if (int(row["Date"].split("/")[2]) == splitYear):
            test = True
        if (test and not np.isnan(row["w_lf_1stWin%"]) and row["Comment"] == "Completed" and not np.isnan(row["PSW"]) and row["Surface"] != "Carpet" and not np.isnan(row["w_surf_1stWin%"]) and not np.isnan(row["w_mf_1stWin%"]) and not np.isnan(row["w_sf_1stWin%"]) and not np.isnan(row["l_surf_1stWin%"]) and not np.isnan(row["l_mf_1stWin%"]) and not np.isnan(row["l_sf_1stWin%"]) and not np.isnan(row["l_lf_1stWin%"])):
            testRows.append(index)
        elif (not test and not np.isnan(row["w_lf_1stWin%"]) and row["Comment"] == "Completed" and not np.isnan(row["PSW"]) and row["Surface"] != "Carpet" and not np.isnan(row["w_surf_1stWin%"]) and not np.isnan(row["w_mf_1stWin%"]) and not np.isnan(row["w_sf_1stWin%"]) and not np.isnan(row["l_surf_1stWin%"]) and not np.isnan(row["l_mf_1stWin%"]) and not np.isnan(row["l_sf_1stWin%"]) and not np.isnan(row["l_lf_1stWin%"])):
            trainRows.append(index)
    data.iloc[trainRows].to_csv(path + "preMatchExpectations_train.csv", index = False)
    data.iloc[testRows].to_csv(path + "preMatchExpectations_test.csv", index = False)

def logistic_regression(path="./csv_data/", features = ["lf","mf","sf","surf","book"]):
    train = pd.read_csv(path + "preMatchExpectations_train.csv", encoding = "ISO-8859-1")
    test = pd.read_csv(path + "preMatchExpectations_test.csv", encoding = "ISO-8859-1")
    keys = ["1stWin%","1stIn%","2ndWin%","2ndIn%","1stRtnWin%","2ndRtnWin%","Ace%","RtnSrv%","AcePer1stIn","Df%","DfPer2ndSrv","1stSrvEff","Def1stSrvEff","SrvRating","OppSrvRating","BpSaved%","BpWon%","RtnRating","OppRtnRating"]
    cats = ["lf", "mf", "sf", "surf"]

    dict = {"Player 1":[], "Player 2":[], "Book Rtg":[], "Player 1 Odds":[], "Player 2 Odds":[], "Player 1 Win":[]}
    for cat in cats:
        for key in keys:
            for x in ["p1","p2"]:
                dict[x + "_" + cat + "_" + key] = []
                dict[x + "_" + cat + "_" + key] = []

    for index, row in train.iterrows():
        num = random.randint(0,1)
        if (num == 0):
            dict["Player 1"].append(row["Winner"])
            dict["Player 2"].append(row["Loser"])
            if (row["PSW"] > 1):
                dict["Book Rtg"].append(-np.log(1/(1/row["PSW"]) - 1))
            else:
                dict["Book Rtg"].append(5.5)
            dict["Player 1 Odds"].append(row["PSW"])
            dict["Player 2 Odds"].append(row["PSL"])
            dict["Player 1 Win"].append(1)
            for cat in cats:
                for key in keys:
                    dict["p1_" + cat + "_" + key].append(row["w_" + cat + "_" + key])
                    dict["p2_" + cat + "_" + key].append(row["l_" + cat + "_" + key])
        elif (num == 1):
            dict["Player 2"].append(row["Winner"])
            dict["Player 1"].append(row["Loser"])
            if (row["PSL"] > 1):
                dict["Book Rtg"].append(-np.log(1/(1/row["PSL"]) - 1))
            else:
                dict["Book Rtg"].append(5.5)
            dict["Player 2 Odds"].append(row["PSW"])
            dict["Player 1 Odds"].append(row["PSL"])
            dict["Player 1 Win"].append(0)
            for cat in cats:
                for key in keys:
                    dict["p1_" + cat + "_" + key].append(row["l_" + cat + "_" + key])
                    dict["p2_" + cat + "_" + key].append(row["w_" + cat + "_" + key])
    for key in dict:
        train[key] = dict[key]




    dict = {"Player 1":[], "Player 2":[], "Book Rtg":[], "Player 1 Odds":[], "Player 2 Odds":[], "Player 1 Win":[]}
    for cat in cats:
        for key in keys:
            for x in ["p1","p2"]:
                dict[x + "_" + cat + "_" + key] = []
                dict[x + "_" + cat + "_" + key] = []

    for index, row in test.iterrows():
        num = random.randint(0,1)
        if (num == 0):
            dict["Player 1"].append(row["Winner"])
            dict["Player 2"].append(row["Loser"])
            if (row["PSW"] > 1):
                dict["Book Rtg"].append(-np.log(1/(1/row["PSW"]) - 1))
            else:
                dict["Book Rtg"].append(5.5)
            dict["Player 1 Odds"].append(row["PSW"])
            dict["Player 2 Odds"].append(row["PSL"])
            dict["Player 1 Win"].append(1)
            for cat in cats:
                for key in keys:
                    dict["p1_" + cat + "_" + key].append(row["w_" + cat + "_" + key])
                    dict["p2_" + cat + "_" + key].append(row["l_" + cat + "_" + key])
        elif (num == 1):
            dict["Player 2"].append(row["Winner"])
            dict["Player 1"].append(row["Loser"])
            if (row["PSL"] > 1):
                dict["Book Rtg"].append(-np.log(1/(1/row["PSL"]) - 1))
            else:
                dict["Book Rtg"].append(5.5)
            dict["Player 2 Odds"].append(row["PSW"])
            dict["Player 1 Odds"].append(row["PSL"])
            dict["Player 1 Win"].append(0)
            for cat in cats:
                for key in keys:
                    dict["p1_" + cat + "_" + key].append(row["l_" + cat + "_" + key])
                    dict["p2_" + cat + "_" + key].append(row["w_" + cat + "_" + key])
    for key in dict:
        test[key] = dict[key]

    xCols = []
    if ("lf" in features):
        for key in keys:
            for x in ["p1","p2"]:
                xCols.append(x + "_lf_" + key)
    if ("mf" in features):
        for key in keys:
            for x in ["p1","p2"]:
                xCols.append(x + "_mf_" + key)
    if ("sf" in features):
        for key in keys:
            for x in ["p1","p2"]:
                xCols.append(x + "_sf_" + key)
    if ("surf" in features):
        for key in keys:
            for x in ["p1","p2"]:
                xCols.append(x + "_surf_" + key)
    if ("book" in features):
        xCols.append("Book Rtg")


    #
    # modelDict = {}
    # for col in xCols:
    #     modelDict[col] = LinearRegression(fit_intercept = False).fit(X = train["Book Rtg"].to_numpy().reshape(-1,1), y = train[col].to_numpy().reshape(-1,1))
    #
    # dict = {}
    # for index, row in train.iterrows():
    #     for col in xCols:
    #         feature = train.at[index, "Book Rtg"]
    #         if (col + "_above_expectation" not in dict):
    #             dict[col + "_above_expectation"] = []
    #         dict[col + "_above_expectation"].append(train.at[index, col] - modelDict[col].predict(feature.reshape(1,-1))[0][0])
    # for key in dict:
    #     train[key] = dict[key]
    #
    # dict = {}
    # for index, row in test.iterrows():
    #     for col in xCols:
    #         feature = test.at[index, "Book Rtg"]
    #         if (col + "_above_expectation" not in dict):
    #             dict[col + "_above_expectation"] = []
    #         dict[col + "_above_expectation"].append(test.at[index, col] - modelDict[col].predict(feature.reshape(1,-1))[0][0])
    # for key in dict:
    #     test[key] = dict[key]

    predictions = []
    tempcols = []
    for x in xCols:
        tempcols.append(x)
    tempcols.append("Player 1")
    tempcols.append("Player 2")
    tempcols.append("Player 1 Odds")
    tempcols.append("Player 2 Odds")
    tempcols.append("Player 1 Win")
    train = pd.DataFrame(train, columns = tempcols).dropna()
    test = pd.DataFrame(test, columns = tempcols).dropna()
    y_train = train["Player 1 Win"]
    #xCols = ["p1_expected_1stServePoint%_above_expectation", "p1_expected_2ndServePoint%_above_expectation", "p2_expected_1stServePoint%_above_expectation", "p2_expected_2ndServePoint%_above_expectation", "p1_adj_expected_1stServePoint%_above_expectation", "p1_adj_expected_2ndServePoint%_above_expectation", "p2_adj_expected_1stServePoint%_above_expectation", "p2_adj_expected_2ndServePoint%_above_expectation", "p1_surf_adj_expected_1stServePoint%_above_expectation", "p1_surf_adj_expected_2ndServePoint%_above_expectation", "p2_surf_adj_expected_1stServePoint%_above_expectation", "p2_surf_adj_expected_2ndServePoint%_above_expectation", "Book Rtg"]
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


    test.to_csv(path + "predictions.csv", index = False)
