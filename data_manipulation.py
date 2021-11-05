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
    newWin1 = -0.394
    newWin2 = -0.240
    newDef1 = 0.226
    newDef2 = 0.249
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
                players[hp.last_f_convert(row["winner_name"])] = {}
                for surface in ["All", "Hard", "Clay", "Grass", "Carpet"]:
                    players[hp.last_f_convert(row["winner_name"])][surface] = {"1stWin%":[],"1stIn%":[],"2ndWin%":[],"2ndIn%":[],"Def1st%":[],"Def2nd%":[],"1stWin%Adj":[],"2ndWin%Adj":[],"Def1st%Adj":[],"Def2nd%Adj":[]}
            if (hp.last_f_convert(row["loser_name"]) not in players):
                players[hp.last_f_convert(row["loser_name"])] = {}
                for surface in ["All", "Hard", "Clay", "Grass", "Carpet"]:
                    players[hp.last_f_convert(row["loser_name"])][surface] = {"1stWin%":[],"1stIn%":[],"2ndWin%":[],"2ndIn%":[],"Def1st%":[],"Def2nd%":[],"1stWin%Adj":[],"2ndWin%Adj":[],"Def1st%Adj":[],"Def2nd%Adj":[]}
            if (row["w_svpt"] > 20 and row["l_svpt"] > 20 and row["w_svpt"] - row["w_1stIn"] - row["w_df"] > 0):
                nAll = len(players[hp.last_f_convert(row["loser_name"])]["All"]["1stWin%"])
                nSurf = len(players[hp.last_f_convert(row["loser_name"])][row["surface"]]["1stWin%"])
                if (nAll > 10):
                    players[hp.last_f_convert(row["winner_name"])]["All"]["1stWin%Adj"].append(((row["w_1stWon"] / row["w_1stIn"] - win1avg) / win1std) - np.average(players[hp.last_f_convert(row["loser_name"])]["All"]["Def1st%Adj"]))
                    players[hp.last_f_convert(row["winner_name"])]["All"]["2ndWin%Adj"].append(((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]) - win2avg) / win2std) - np.average(players[hp.last_f_convert(row["loser_name"])]["All"]["Def2nd%Adj"]))
                    players[hp.last_f_convert(row["winner_name"])]["All"]["Def1st%Adj"].append((((row["l_1stWon"] / row["l_1stIn"]) - win1avg) / win1std) - np.average(players[hp.last_f_convert(row["loser_name"])]["All"]["1stWin%Adj"]))
                    players[hp.last_f_convert(row["winner_name"])]["All"]["Def2nd%Adj"].append((((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])) - win2avg) / win2std) - np.average(players[hp.last_f_convert(row["loser_name"])]["All"]["2ndWin%Adj"]))
                elif (nAll > 0):
                    players[hp.last_f_convert(row["winner_name"])]["All"]["1stWin%Adj"].append(((row["w_1stWon"] / row["w_1stIn"] - win1avg) / win1std) - ((nAll * np.average(players[hp.last_f_convert(row["loser_name"])]["All"]["Def1st%Adj"])) + (10 - nAll) * newDef1) / 10)
                    players[hp.last_f_convert(row["winner_name"])]["All"]["2ndWin%Adj"].append(((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]) - win2avg) / win2std) - ((nAll * np.average(players[hp.last_f_convert(row["loser_name"])]["All"]["Def2nd%Adj"])) + (10 - nAll) * newDef2) / 10)
                    players[hp.last_f_convert(row["winner_name"])]["All"]["Def1st%Adj"].append((((row["l_1stWon"] / row["l_1stIn"]) - win1avg) / win1std) - ((nAll * np.average(players[hp.last_f_convert(row["loser_name"])]["All"]["1stWin%Adj"])) + (10 - nAll) * newWin1) / 10)
                    players[hp.last_f_convert(row["winner_name"])]["All"]["Def2nd%Adj"].append((((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])) - win2avg) / win2std) - ((nAll * np.average(players[hp.last_f_convert(row["loser_name"])]["All"]["2ndWin%Adj"])) + (10 - nAll) * newWin2) / 10)
                else:
                    players[hp.last_f_convert(row["winner_name"])]["All"]["1stWin%Adj"].append(((row["w_1stWon"] / row["w_1stIn"] - win1avg) / win1std) - newDef1)
                    players[hp.last_f_convert(row["winner_name"])]["All"]["2ndWin%Adj"].append(((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]) - win2avg) / win2std) - newDef2)
                    players[hp.last_f_convert(row["winner_name"])]["All"]["Def1st%Adj"].append((((row["l_1stWon"] / row["l_1stIn"]) - win1avg) / win1std) + newWin1)
                    players[hp.last_f_convert(row["winner_name"])]["All"]["Def2nd%Adj"].append((((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])) - win2avg) / win2std) + newWin2)
                if (nSurf > 10):
                    players[hp.last_f_convert(row["winner_name"])][row["surface"]]["1stWin%Adj"].append(((row["w_1stWon"] / row["w_1stIn"] - win1avg) / win1std) - np.average(players[hp.last_f_convert(row["loser_name"])][row["surface"]]["Def1st%Adj"]))
                    players[hp.last_f_convert(row["winner_name"])][row["surface"]]["2ndWin%Adj"].append(((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]) - win2avg) / win2std) - np.average(players[hp.last_f_convert(row["loser_name"])][row["surface"]]["Def2nd%Adj"]))
                    players[hp.last_f_convert(row["winner_name"])][row["surface"]]["Def1st%Adj"].append((((row["l_1stWon"] / row["l_1stIn"]) - win1avg) / win1std) - np.average(players[hp.last_f_convert(row["loser_name"])][row["surface"]]["1stWin%Adj"]))
                    players[hp.last_f_convert(row["winner_name"])][row["surface"]]["Def2nd%Adj"].append((((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])) - win2avg) / win2std) - np.average(players[hp.last_f_convert(row["loser_name"])][row["surface"]]["2ndWin%Adj"]))
                elif (nSurf > 0):
                    players[hp.last_f_convert(row["winner_name"])][row["surface"]]["1stWin%Adj"].append(((row["w_1stWon"] / row["w_1stIn"] - win1avg) / win1std) - ((nSurf * np.average(players[hp.last_f_convert(row["loser_name"])][row["surface"]]["Def1st%Adj"])) + (10 - nSurf) * newDef1) / 10)
                    players[hp.last_f_convert(row["winner_name"])][row["surface"]]["2ndWin%Adj"].append(((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]) - win2avg) / win2std) - ((nSurf * np.average(players[hp.last_f_convert(row["loser_name"])][row["surface"]]["Def2nd%Adj"])) + (10 - nSurf) * newDef2) / 10)
                    players[hp.last_f_convert(row["winner_name"])][row["surface"]]["Def1st%Adj"].append((((row["l_1stWon"] / row["l_1stIn"]) - win1avg) / win1std) - ((nSurf * np.average(players[hp.last_f_convert(row["loser_name"])][row["surface"]]["1stWin%Adj"])) + (10 - nSurf) * newWin1) / 10)
                    players[hp.last_f_convert(row["winner_name"])][row["surface"]]["Def2nd%Adj"].append((((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])) - win2avg) / win2std) - ((nSurf * np.average(players[hp.last_f_convert(row["loser_name"])][row["surface"]]["2ndWin%Adj"])) + (10 - nSurf) * newWin2) / 10)
                else:
                    players[hp.last_f_convert(row["winner_name"])][row["surface"]]["1stWin%Adj"].append(((row["w_1stWon"] / row["w_1stIn"] - win1avg) / win1std) - 0.1)
                    players[hp.last_f_convert(row["winner_name"])][row["surface"]]["2ndWin%Adj"].append(((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]) - win2avg) / win2std) - 0.1)
                    players[hp.last_f_convert(row["winner_name"])][row["surface"]]["Def1st%Adj"].append((((row["l_1stWon"] / row["l_1stIn"]) - win1avg) / win1std) + 0.1)
                    players[hp.last_f_convert(row["winner_name"])][row["surface"]]["Def2nd%Adj"].append((((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])) - win2avg) / win2std) + 0.1)

                nAll = len(players[hp.last_f_convert(row["winner_name"])]["All"]["1stWin%"])
                nSurf = len(players[hp.last_f_convert(row["winner_name"])][row["surface"]]["1stWin%"])
                if (nAll > 10):
                    players[hp.last_f_convert(row["loser_name"])]["All"]["1stWin%Adj"].append(((row["l_1stWon"] / row["l_1stIn"] - win1avg) / win1std) - np.average(players[hp.last_f_convert(row["winner_name"])]["All"]["Def1st%Adj"]))
                    players[hp.last_f_convert(row["loser_name"])]["All"]["2ndWin%Adj"].append(((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]) - win2avg) / win2std) - np.average(players[hp.last_f_convert(row["winner_name"])]["All"]["Def2nd%Adj"]))
                    players[hp.last_f_convert(row["loser_name"])]["All"]["Def1st%Adj"].append((((row["w_1stWon"] / row["w_1stIn"]) - win1avg) / win1std) - np.average(players[hp.last_f_convert(row["winner_name"])]["All"]["1stWin%Adj"]))
                    players[hp.last_f_convert(row["loser_name"])]["All"]["Def2nd%Adj"].append((((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])) - win2avg) / win2std) - np.average(players[hp.last_f_convert(row["winner_name"])]["All"]["2ndWin%Adj"]))
                elif (nAll > 0):
                    players[hp.last_f_convert(row["loser_name"])]["All"]["1stWin%Adj"].append(((row["l_1stWon"] / row["l_1stIn"] - win1avg) / win1std) - ((nAll * np.average(players[hp.last_f_convert(row["winner_name"])]["All"]["Def1st%Adj"])) + (10 - nAll) * newDef1) / 10)
                    players[hp.last_f_convert(row["loser_name"])]["All"]["2ndWin%Adj"].append(((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]) - win2avg) / win2std) - ((nAll * np.average(players[hp.last_f_convert(row["winner_name"])]["All"]["Def2nd%Adj"])) + (10 - nAll) * newDef2) / 10)
                    players[hp.last_f_convert(row["loser_name"])]["All"]["Def1st%Adj"].append((((row["w_1stWon"] / row["w_1stIn"]) - win1avg) / win1std) - ((nAll * np.average(players[hp.last_f_convert(row["winner_name"])]["All"]["1stWin%Adj"])) + (10 - nAll) * newWin1) / 10)
                    players[hp.last_f_convert(row["loser_name"])]["All"]["Def2nd%Adj"].append((((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])) - win2avg) / win2std) - ((nAll * np.average(players[hp.last_f_convert(row["winner_name"])]["All"]["2ndWin%Adj"])) + (10 - nAll) * newWin2) / 10)
                else:
                    players[hp.last_f_convert(row["loser_name"])]["All"]["1stWin%Adj"].append(((row["l_1stWon"] / row["l_1stIn"] - win1avg) / win1std) - newDef1)
                    players[hp.last_f_convert(row["loser_name"])]["All"]["2ndWin%Adj"].append(((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]) - win2avg) / win2std) - newDef2)
                    players[hp.last_f_convert(row["loser_name"])]["All"]["Def1st%Adj"].append((((row["w_1stWon"] / row["w_1stIn"]) - win1avg) / win1std) + newWin1)
                    players[hp.last_f_convert(row["loser_name"])]["All"]["Def2nd%Adj"].append((((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])) - win2avg) / win2std) + newWin2)
                if (nSurf > 10):
                    players[hp.last_f_convert(row["loser_name"])][row["surface"]]["1stWin%Adj"].append(((row["l_1stWon"] / row["l_1stIn"] - win1avg) / win1std) - np.average(players[hp.last_f_convert(row["winner_name"])][row["surface"]]["Def1st%Adj"]))
                    players[hp.last_f_convert(row["loser_name"])][row["surface"]]["2ndWin%Adj"].append(((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]) - win2avg) / win2std) - np.average(players[hp.last_f_convert(row["winner_name"])][row["surface"]]["Def2nd%Adj"]))
                    players[hp.last_f_convert(row["loser_name"])][row["surface"]]["Def1st%Adj"].append((((row["w_1stWon"] / row["w_1stIn"]) - win1avg) / win1std) - np.average(players[hp.last_f_convert(row["winner_name"])][row["surface"]]["1stWin%Adj"]))
                    players[hp.last_f_convert(row["loser_name"])][row["surface"]]["Def2nd%Adj"].append((((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])) - win2avg) / win2std) - np.average(players[hp.last_f_convert(row["winner_name"])][row["surface"]]["2ndWin%Adj"]))
                elif (nSurf > 0):
                    players[hp.last_f_convert(row["loser_name"])][row["surface"]]["1stWin%Adj"].append(((row["l_1stWon"] / row["l_1stIn"] - win1avg) / win1std) - ((nSurf * np.average(players[hp.last_f_convert(row["winner_name"])][row["surface"]]["Def1st%Adj"])) + (10 - nSurf) * newDef1) / 10)
                    players[hp.last_f_convert(row["loser_name"])][row["surface"]]["2ndWin%Adj"].append(((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]) - win2avg) / win2std) - ((nSurf * np.average(players[hp.last_f_convert(row["winner_name"])][row["surface"]]["Def2nd%Adj"])) + (10 - nSurf) * newDef2) / 10)
                    players[hp.last_f_convert(row["loser_name"])][row["surface"]]["Def1st%Adj"].append((((row["w_1stWon"] / row["w_1stIn"]) - win1avg) / win1std) - ((nSurf * np.average(players[hp.last_f_convert(row["winner_name"])][row["surface"]]["1stWin%Adj"])) + (10 - nSurf) * newWin1) / 10)
                    players[hp.last_f_convert(row["loser_name"])][row["surface"]]["Def2nd%Adj"].append((((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])) - win2avg) / win2std) - ((nSurf * np.average(players[hp.last_f_convert(row["winner_name"])][row["surface"]]["2ndWin%Adj"])) + (10 - nSurf) * newWin2) / 10)
                else:
                    players[hp.last_f_convert(row["loser_name"])][row["surface"]]["1stWin%Adj"].append(((row["l_1stWon"] / row["l_1stIn"] - win1avg) / win1std) - newDef1)
                    players[hp.last_f_convert(row["loser_name"])][row["surface"]]["2ndWin%Adj"].append(((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]) - win2avg) / win2std) - newDef2)
                    players[hp.last_f_convert(row["loser_name"])][row["surface"]]["Def1st%Adj"].append((((row["w_1stWon"] / row["w_1stIn"]) - win1avg) / win1std) + newWin1)
                    players[hp.last_f_convert(row["loser_name"])][row["surface"]]["Def2nd%Adj"].append((((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])) - win2avg) / win2std) + newWin2)

                players[hp.last_f_convert(row["winner_name"])]["All"]["1stWin%"].append(row["w_1stWon"] / row["w_1stIn"])
                players[hp.last_f_convert(row["winner_name"])]["All"]["1stIn%"].append(row["w_1stIn"] / row["w_svpt"])
                players[hp.last_f_convert(row["winner_name"])]["All"]["2ndWin%"].append(row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]))
                players[hp.last_f_convert(row["winner_name"])]["All"]["2ndIn%"].append((row["w_svpt"] - row["w_1stIn"] - row["w_df"]) / (row["w_svpt"] - row["w_1stIn"]))
                players[hp.last_f_convert(row["winner_name"])]["All"]["Def1st%"].append((row["l_1stWon"] / row["l_1stIn"]))
                players[hp.last_f_convert(row["winner_name"])]["All"]["Def2nd%"].append((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])))
                # players[hp.last_f_convert(row["winner_name"])][row["surface"]]["1stWin%"].append(row["w_1stWon"] / row["w_1stIn"])
                # players[hp.last_f_convert(row["winner_name"])][row["surface"]]["1stIn%"].append(row["w_1stIn"] / row["w_svpt"])
                # players[hp.last_f_convert(row["winner_name"])][row["surface"]]["2ndWin%"].append(row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]))
                # players[hp.last_f_convert(row["winner_name"])][row["surface"]]["2ndIn%"].append((row["w_svpt"] - row["w_1stIn"] - row["w_df"]) / (row["w_svpt"] - row["w_1stIn"]))
                # players[hp.last_f_convert(row["winner_name"])][row["surface"]]["Def1st%"].append((row["l_1stWon"] / row["l_1stIn"]))
                # players[hp.last_f_convert(row["winner_name"])][row["surface"]]["Def2nd%"].append((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])))

                players[hp.last_f_convert(row["loser_name"])]["All"]["1stWin%"].append(row["l_1stWon"] / row["l_1stIn"])
                players[hp.last_f_convert(row["loser_name"])]["All"]["1stIn%"].append(row["l_1stIn"] / row["l_svpt"])
                players[hp.last_f_convert(row["loser_name"])]["All"]["2ndWin%"].append(row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]))
                players[hp.last_f_convert(row["loser_name"])]["All"]["2ndIn%"].append((row["l_svpt"] - row["l_1stIn"] - row["l_df"]) / (row["l_svpt"] - row["l_1stIn"]))
                players[hp.last_f_convert(row["loser_name"])]["All"]["Def1st%"].append((row["w_1stWon"] / row["w_1stIn"]))
                players[hp.last_f_convert(row["loser_name"])]["All"]["Def2nd%"].append((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])))
                # players[hp.last_f_convert(row["loser_name"])][row["surface"]]["1stWin%"].append(row["l_1stWon"] / row["l_1stIn"])
                # players[hp.last_f_convert(row["loser_name"])][row["surface"]]["1stIn%"].append(row["l_1stIn"] / row["l_svpt"])
                # players[hp.last_f_convert(row["loser_name"])][row["surface"]]["2ndWin%"].append(row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]))
                # players[hp.last_f_convert(row["loser_name"])][row["surface"]]["2ndIn%"].append((row["l_svpt"] - row["l_1stIn"] - row["l_df"]) / (row["l_svpt"] - row["l_1stIn"]))
                # players[hp.last_f_convert(row["loser_name"])][row["surface"]]["Def1st%"].append((row["w_1stWon"] / row["w_1stIn"]))
                # players[hp.last_f_convert(row["loser_name"])][row["surface"]]["Def2nd%"].append((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])))

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
    dict["w_surf_adj_expected_1stServePoint%"] = []
    dict["w_surf_adj_expected_2ndServePoint%"] = []
    dict["l_surf_adj_expected_1stServePoint%"] = []
    dict["l_surf_adj_expected_2ndServePoint%"] = []
    dict["w_gp"] = []
    dict["l_gp"] = []
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
            if (len(players[wKey]["All"]["1stIn%"]) < 10):
                w_1st_in = (len(players[wKey]["All"]["1stIn%"]) * np.average(players[wKey]["All"]["1stIn%"]) + (10 - len(players[wKey]["All"]["1stIn%"])) * naiveIn1) / 10
                w_2nd_in = (len(players[wKey]["All"]["2ndIn%"]) * np.average(players[wKey]["All"]["2ndIn%"]) + (10 - len(players[wKey]["All"]["2ndIn%"])) * naiveIn2) / 10
                w_1st_win = (len(players[wKey]["All"]["1stWin%"]) * np.average(players[wKey]["All"]["1stWin%"]) + (10 - len(players[wKey]["All"]["1stWin%"])) * naiveWin1) / 10
                w_2nd_win = (len(players[wKey]["All"]["2ndWin%"]) * np.average(players[wKey]["All"]["2ndWin%"]) + (10 - len(players[wKey]["All"]["2ndWin%"])) * naiveWin2) / 10
                w_1st_def = (len(players[wKey]["All"]["Def1st%"]) * np.average(players[wKey]["All"]["Def1st%"]) - (10 - len(players[wKey]["All"]["Def1st%"])) * naiveWin1) / 10
                w_2nd_def = (len(players[wKey]["All"]["Def2nd%"]) * np.average(players[wKey]["All"]["Def2nd%"]) - (10 - len(players[wKey]["All"]["Def2nd%"])) * naiveWin2) / 10
                w_adj_1st_win = (len(players[wKey]["All"]["1stWin%Adj"]) * np.average(players[wKey]["All"]["1stWin%Adj"]) + (10 - len(players[wKey]["All"]["1stWin%Adj"])) * newWin1) / 10
                w_adj_2nd_win = (len(players[wKey]["All"]["2ndWin%Adj"]) * np.average(players[wKey]["All"]["2ndWin%Adj"]) + (10 - len(players[wKey]["All"]["2ndWin%Adj"])) * newWin2) / 10
                w_adj_1st_def = (len(players[wKey]["All"]["Def1st%Adj"]) * np.average(players[wKey]["All"]["Def1st%Adj"]) - (10 - len(players[wKey]["All"]["Def1st%Adj"])) * newDef1) / 10
                w_adj_2nd_def = (len(players[wKey]["All"]["Def2nd%Adj"]) * np.average(players[wKey]["All"]["Def2nd%Adj"]) - (10 - len(players[wKey]["All"]["Def2nd%Adj"])) * newDef2) / 10
            else:
                w_1st_in = np.average(players[wKey]["All"]["1stIn%"])
                w_2nd_in = np.average(players[wKey]["All"]["2ndIn%"])
                w_1st_win = np.average(players[wKey]["All"]["1stWin%"])
                w_2nd_win = np.average(players[wKey]["All"]["2ndWin%"])
                w_1st_def = np.average(players[wKey]["All"]["Def1st%"])
                w_2nd_def = np.average(players[wKey]["All"]["Def2nd%"])
                w_adj_1st_win = np.average(players[wKey]["All"]["1stWin%Adj"])
                w_adj_2nd_win = np.average(players[wKey]["All"]["2ndWin%Adj"])
                w_adj_1st_def = np.average(players[wKey]["All"]["Def1st%Adj"])
                w_adj_2nd_def = np.average(players[wKey]["All"]["Def2nd%Adj"])
            if (len(players[wKey][row["Surface"]]["1stWin%Adj"]) > 10):
                w_surf_adj_1st_win = np.average(players[wKey][row["Surface"]]["1stWin%Adj"])
                w_surf_adj_2nd_win = np.average(players[wKey][row["Surface"]]["2ndWin%Adj"])
                w_surf_adj_1st_def = np.average(players[wKey][row["Surface"]]["Def1st%Adj"])
                w_surf_adj_2nd_def = np.average(players[wKey][row["Surface"]]["Def2nd%Adj"])
            elif (len(players[wKey][row["Surface"]]["1stWin%Adj"]) > 0):
                w_surf_adj_1st_win = (len(players[wKey][row["Surface"]]["1stWin%Adj"]) * np.average(players[wKey][row["Surface"]]["1stWin%Adj"]) + (10 - len(players[wKey][row["Surface"]]["1stWin%Adj"])) * newWin1) / 10
                w_surf_adj_2nd_win = (len(players[wKey][row["Surface"]]["2ndWin%Adj"]) * np.average(players[wKey][row["Surface"]]["2ndWin%Adj"]) + (10 - len(players[wKey][row["Surface"]]["2ndWin%Adj"])) * newWin2) / 10
                w_surf_adj_1st_def = (len(players[wKey][row["Surface"]]["Def1st%Adj"]) * np.average(players[wKey][row["Surface"]]["Def1st%Adj"]) - (10 - len(players[wKey][row["Surface"]]["Def1st%Adj"])) * newDef1) / 10
                w_surf_adj_2nd_def = (len(players[wKey][row["Surface"]]["Def2nd%Adj"]) * np.average(players[wKey][row["Surface"]]["Def2nd%Adj"]) - (10 - len(players[wKey][row["Surface"]]["Def2nd%Adj"])) * newDef2) / 10
            else:
                w_surf_adj_1st_win = newWin1
                w_surf_adj_2nd_win = newWin2
                w_surf_adj_1st_def = newDef1
                w_surf_adj_2nd_def = newDef2
            if (len(players[lKey]["All"]["1stIn%"]) < 10):
                l_1st_in = (len(players[lKey]["All"]["1stIn%"]) * np.average(players[lKey]["All"]["1stIn%"]) + (10 - len(players[lKey]["All"]["1stIn%"])) * naiveIn1) / 10
                l_2nd_in = (len(players[lKey]["All"]["2ndIn%"]) * np.average(players[lKey]["All"]["2ndIn%"]) + (10 - len(players[lKey]["All"]["2ndIn%"])) * naiveIn2) / 10
                l_1st_win = (len(players[lKey]["All"]["1stWin%"]) * np.average(players[lKey]["All"]["1stWin%"]) + (10 - len(players[lKey]["All"]["1stWin%"])) * naiveWin1) / 10
                l_2nd_win = (len(players[lKey]["All"]["2ndWin%"]) * np.average(players[lKey]["All"]["2ndWin%"]) + (10 - len(players[lKey]["All"]["2ndWin%"])) * naiveWin2) / 10
                l_1st_def = (len(players[lKey]["All"]["Def1st%"]) * np.average(players[lKey]["All"]["Def1st%"]) - (10 - len(players[lKey]["All"]["Def1st%"])) * naiveWin1) / 10
                l_2nd_def = (len(players[lKey]["All"]["Def2nd%"]) * np.average(players[lKey]["All"]["Def2nd%"]) - (10 - len(players[lKey]["All"]["Def2nd%"])) * naiveWin2) / 10
                l_adj_1st_win = (len(players[lKey]["All"]["1stWin%Adj"]) * np.average(players[lKey]["All"]["1stWin%Adj"]) + (10 - len(players[lKey]["All"]["1stWin%Adj"])) * newWin1) / 10
                l_adj_2nd_win = (len(players[lKey]["All"]["2ndWin%Adj"]) * np.average(players[lKey]["All"]["2ndWin%Adj"]) + (10 - len(players[lKey]["All"]["2ndWin%Adj"])) * newWin2) / 10
                l_adj_1st_def = (len(players[lKey]["All"]["Def1st%Adj"]) * np.average(players[lKey]["All"]["Def1st%Adj"]) - (10 - len(players[lKey]["All"]["Def1st%Adj"])) * newDef1) / 10
                l_adj_2nd_def = (len(players[lKey]["All"]["Def2nd%Adj"]) * np.average(players[lKey]["All"]["Def2nd%Adj"]) - (10 - len(players[lKey]["All"]["Def2nd%Adj"])) * newDef2) / 10
            else:
                l_1st_in = np.average(players[lKey]["All"]["1stIn%"])
                l_2nd_in = np.average(players[lKey]["All"]["2ndIn%"])
                l_1st_win = np.average(players[lKey]["All"]["1stWin%"])
                l_2nd_win = np.average(players[lKey]["All"]["2ndWin%"])
                l_1st_def = np.average(players[lKey]["All"]["Def1st%"])
                l_2nd_def = np.average(players[lKey]["All"]["Def2nd%"])
                l_adj_1st_win = np.average(players[lKey]["All"]["1stWin%Adj"])
                l_adj_2nd_win = np.average(players[lKey]["All"]["2ndWin%Adj"])
                l_adj_1st_def = np.average(players[lKey]["All"]["Def1st%Adj"])
                l_adj_2nd_def = np.average(players[lKey]["All"]["Def2nd%Adj"])
            if (len(players[lKey][row["Surface"]]["1stWin%Adj"]) > 10):
                l_surf_adj_1st_win = np.average(players[lKey][row["Surface"]]["1stWin%Adj"])
                l_surf_adj_2nd_win = np.average(players[lKey][row["Surface"]]["2ndWin%Adj"])
                l_surf_adj_1st_def = np.average(players[lKey][row["Surface"]]["Def1st%Adj"])
                l_surf_adj_2nd_def = np.average(players[lKey][row["Surface"]]["Def2nd%Adj"])
            elif (len(players[lKey][row["Surface"]]["1stWin%Adj"]) > 0):
                l_surf_adj_1st_win = (len(players[lKey][row["Surface"]]["1stWin%Adj"]) * np.average(players[lKey][row["Surface"]]["1stWin%Adj"]) + (10 - len(players[lKey][row["Surface"]]["1stWin%Adj"])) * newWin1) / 10
                l_surf_adj_2nd_win = (len(players[lKey][row["Surface"]]["2ndWin%Adj"]) * np.average(players[lKey][row["Surface"]]["2ndWin%Adj"]) + (10 - len(players[lKey][row["Surface"]]["2ndWin%Adj"])) * newWin2) / 10
                l_surf_adj_1st_def = (len(players[lKey][row["Surface"]]["Def1st%Adj"]) * np.average(players[lKey][row["Surface"]]["Def1st%Adj"]) - (10 - len(players[lKey][row["Surface"]]["Def1st%Adj"])) * newDef1) / 10
                l_surf_adj_2nd_def = (len(players[lKey][row["Surface"]]["Def2nd%Adj"]) * np.average(players[lKey][row["Surface"]]["Def2nd%Adj"]) - (10 - len(players[lKey][row["Surface"]]["Def2nd%Adj"])) * newDef2) / 10
            else:
                l_surf_adj_1st_win = newWin1
                l_surf_adj_2nd_win = newWin2
                l_surf_adj_1st_def = newDef1
                l_surf_adj_2nd_def = newDef2

            dict["w_expected_1stServePoint%"].append(w_1st_in * (w_1st_win + l_1st_def) / 2)
            dict["w_expected_2ndServePoint%"].append(w_2nd_in * (w_2nd_win + l_2nd_def) / 2)
            dict["l_expected_1stServePoint%"].append(l_1st_in * (l_1st_win + w_1st_def) / 2)
            dict["l_expected_2ndServePoint%"].append(l_2nd_in * (l_2nd_win + w_2nd_def) / 2)
            dict["w_adj_expected_1stServePoint%"].append(w_1st_in * (w_adj_1st_win + l_adj_1st_def))
            dict["w_adj_expected_2ndServePoint%"].append(w_2nd_in * (w_adj_2nd_win + l_adj_2nd_def))
            dict["l_adj_expected_1stServePoint%"].append(l_1st_in * (l_adj_1st_win + w_adj_1st_def))
            dict["l_adj_expected_2ndServePoint%"].append(l_2nd_in * (l_adj_2nd_win + w_adj_2nd_def))
            dict["w_surf_adj_expected_1stServePoint%"].append(w_1st_in * (w_surf_adj_1st_win + l_surf_adj_1st_def))
            dict["w_surf_adj_expected_2ndServePoint%"].append(w_2nd_in * (w_surf_adj_2nd_win + l_surf_adj_2nd_def))
            dict["l_surf_adj_expected_1stServePoint%"].append(l_1st_in * (l_surf_adj_1st_win + w_surf_adj_1st_def))
            dict["l_surf_adj_expected_2ndServePoint%"].append(l_2nd_in * (l_surf_adj_2nd_win + w_surf_adj_2nd_def))
            dict["w_gp"].append(len(players[wKey]["All"]["1stIn%"]))
            dict["l_gp"].append(len(players[lKey]["All"]["1stIn%"]))
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
            dict["w_surf_adj_expected_1stServePoint%"].append(np.nan)
            dict["w_surf_adj_expected_2ndServePoint%"].append(np.nan)
            dict["l_surf_adj_expected_1stServePoint%"].append(np.nan)
            dict["l_surf_adj_expected_2ndServePoint%"].append(np.nan)
            dict["w_gp"].append(np.nan)
            dict["l_gp"].append(np.nan)
        if (not wFound):
            name = hp.cleanBetName(row["Winner"])[0] + " "
            for letter in hp.cleanBetName(row["Winner"])[1]:
                if (letter == ""):
                    break
                name = name + letter + "."
            wKey = name
            players[wKey] = {}
            for surface in ["All", "Hard", "Clay", "Grass", "Carpet"]:
                players[wKey][surface] = {"1stWin%":[],"1stIn%":[],"2ndWin%":[],"2ndIn%":[],"Def1st%":[],"Def2nd%":[],"1stWin%Adj":[],"2ndWin%Adj":[],"Def1st%Adj":[],"Def2nd%Adj":[]}
        if (not lFound):
            name = hp.cleanBetName(row["Loser"])[0] + " "
            for letter in hp.cleanBetName(row["Loser"])[1]:
                if (letter == ""):
                    break
                name = name + letter + "."
            lKey = name
            players[lKey] = {}
            for surface in ["All", "Hard", "Clay", "Grass", "Carpet"]:
                players[lKey][surface] = {"1stWin%":[],"1stIn%":[],"2ndWin%":[],"2ndIn%":[],"Def1st%":[],"Def2nd%":[],"1stWin%Adj":[],"2ndWin%Adj":[],"Def1st%Adj":[],"Def2nd%Adj":[]}
        if (row["w_svpt"] > 20 and row["l_svpt"] > 20 and row["w_svpt"] - row["w_1stIn"] - row["w_df"] > 0 and row["l_svpt"] - row["l_1stIn"] - row["l_df"] > 0):
            nAll = len(players[lKey]["All"]["1stWin%"])
            nSurf = len(players[lKey][row["Surface"]]["1stWin%Adj"])
            if (nAll > 10):
                players[wKey]["All"]["1stWin%Adj"].append(((row["w_1stWon"] / row["w_1stIn"] - win1avg) / win1std) - np.average(players[lKey]["All"]["Def1st%Adj"]))
                players[wKey]["All"]["2ndWin%Adj"].append(((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]) - win2avg) / win2std) - np.average(players[lKey]["All"]["Def2nd%Adj"]))
                players[wKey]["All"]["Def1st%Adj"].append((((row["l_1stWon"] / row["l_1stIn"]) - win1avg) / win1std) - np.average(players[lKey]["All"]["1stWin%Adj"]))
                players[wKey]["All"]["Def2nd%Adj"].append((((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])) - win2avg) / win2std) - np.average(players[lKey]["All"]["2ndWin%Adj"]))
            elif (nAll > 0):
                players[wKey]["All"]["1stWin%Adj"].append(((row["w_1stWon"] / row["w_1stIn"] - win1avg) / win1std) - ((nAll * np.average(players[lKey]["All"]["Def1st%Adj"])) + (10 - nAll) * newDef1) / 10)
                players[wKey]["All"]["2ndWin%Adj"].append(((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]) - win2avg) / win2std) - ((nAll * np.average(players[lKey]["All"]["Def2nd%Adj"])) + (10 - nAll) * newDef2) / 10)
                players[wKey]["All"]["Def1st%Adj"].append((((row["l_1stWon"] / row["l_1stIn"]) - win1avg) / win1std) - ((nAll * np.average(players[lKey]["All"]["1stWin%Adj"])) + (10 - nAll) * newWin1) / 10)
                players[wKey]["All"]["Def2nd%Adj"].append((((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])) - win2avg) / win2std) - ((nAll * np.average(players[lKey]["All"]["2ndWin%Adj"])) + (10 - nAll) * newWin2) / 10)
            else:
                players[wKey]["All"]["1stWin%Adj"].append(((row["w_1stWon"] / row["w_1stIn"] - win1avg) / win1std) - newDef1)
                players[wKey]["All"]["2ndWin%Adj"].append(((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]) - win2avg) / win2std) - newDef1)
                players[wKey]["All"]["Def1st%Adj"].append((((row["l_1stWon"] / row["l_1stIn"]) - win1avg) / win1std) + newWin1)
                players[wKey]["All"]["Def2nd%Adj"].append((((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])) - win2avg) / win2std) + newWin2)
            if (nSurf > 10):
                players[wKey][row["Surface"]]["1stWin%Adj"].append(((row["w_1stWon"] / row["w_1stIn"] - win1avg) / win1std) - np.average(players[lKey][row["Surface"]]["Def1st%Adj"]))
                players[wKey][row["Surface"]]["2ndWin%Adj"].append(((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]) - win2avg) / win2std) - np.average(players[lKey][row["Surface"]]["Def2nd%Adj"]))
                players[wKey][row["Surface"]]["Def1st%Adj"].append((((row["l_1stWon"] / row["l_1stIn"]) - win1avg) / win1std) - np.average(players[lKey][row["Surface"]]["1stWin%Adj"]))
                players[wKey][row["Surface"]]["Def2nd%Adj"].append((((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])) - win2avg) / win2std) - np.average(players[lKey][row["Surface"]]["2ndWin%Adj"]))
            elif (nSurf > 0):
                players[wKey][row["Surface"]]["1stWin%Adj"].append(((row["w_1stWon"] / row["w_1stIn"] - win1avg) / win1std) - ((nSurf * np.average(players[lKey][row["Surface"]]["Def1st%Adj"])) + (10 - nSurf) * newDef1) / 10)
                players[wKey][row["Surface"]]["2ndWin%Adj"].append(((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]) - win2avg) / win2std) - ((nSurf * np.average(players[lKey][row["Surface"]]["Def2nd%Adj"])) + (10 - nSurf) * newDef2) / 10)
                players[wKey][row["Surface"]]["Def1st%Adj"].append((((row["l_1stWon"] / row["l_1stIn"]) - win1avg) / win1std) - ((nSurf * np.average(players[lKey][row["Surface"]]["1stWin%Adj"])) + (10 - nSurf) * newWin1) / 10)
                players[wKey][row["Surface"]]["Def2nd%Adj"].append((((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])) - win2avg) / win2std) - ((nSurf * np.average(players[lKey][row["Surface"]]["2ndWin%Adj"])) + (10 - nSurf) * newWin2) / 10)
            else:
                players[wKey][row["Surface"]]["1stWin%Adj"].append(((row["w_1stWon"] / row["w_1stIn"] - win1avg) / win1std) - newDef1)
                players[wKey][row["Surface"]]["2ndWin%Adj"].append(((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]) - win2avg) / win2std) - newDef2)
                players[wKey][row["Surface"]]["Def1st%Adj"].append((((row["l_1stWon"] / row["l_1stIn"]) - win1avg) / win1std) + newWin1)
                players[wKey][row["Surface"]]["Def2nd%Adj"].append((((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])) - win2avg) / win2std) + newWin2)

            nAll = len(players[wKey]["All"]["1stWin%"])
            nSurf = len(players[wKey][row["Surface"]]["1stWin%Adj"])
            if (nAll > 10):
                players[lKey]["All"]["1stWin%Adj"].append(((row["l_1stWon"] / row["l_1stIn"] - win1avg) / win1std) - np.average(players[wKey]["All"]["Def1st%Adj"]))
                players[lKey]["All"]["2ndWin%Adj"].append(((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]) - win2avg) / win2std) - np.average(players[wKey]["All"]["Def2nd%Adj"]))
                players[lKey]["All"]["Def1st%Adj"].append((((row["w_1stWon"] / row["w_1stIn"]) - win1avg) / win1std) - np.average(players[wKey]["All"]["1stWin%Adj"]))
                players[lKey]["All"]["Def2nd%Adj"].append((((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])) - win2avg) / win2std) - np.average(players[wKey]["All"]["2ndWin%Adj"]))
            elif (nAll > 0):
                players[lKey]["All"]["1stWin%Adj"].append(((row["l_1stWon"] / row["l_1stIn"] - win1avg) / win1std) - ((nAll * np.average(players[wKey]["All"]["Def1st%Adj"])) + (10 - nAll) * newDef1) / 10)
                players[lKey]["All"]["2ndWin%Adj"].append(((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]) - win2avg) / win2std) - ((nAll * np.average(players[wKey]["All"]["Def2nd%Adj"])) + (10 - nAll) * newDef2) / 10)
                players[lKey]["All"]["Def1st%Adj"].append((((row["w_1stWon"] / row["w_1stIn"]) - win1avg) / win1std) - ((nAll * np.average(players[wKey]["All"]["1stWin%Adj"])) + (10 - nAll) * newWin1) / 10)
                players[lKey]["All"]["Def2nd%Adj"].append((((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])) - win2avg) / win2std) - ((nAll * np.average(players[wKey]["All"]["2ndWin%Adj"])) + (10 - nAll) * newWin2) / 10)
            else:
                players[lKey]["All"]["1stWin%Adj"].append(((row["l_1stWon"] / row["l_1stIn"] - win1avg) / win1std) - newDef1)
                players[lKey]["All"]["2ndWin%Adj"].append(((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]) - win2avg) / win2std) - newDef2)
                players[lKey]["All"]["Def1st%Adj"].append((((row["w_1stWon"] / row["w_1stIn"]) - win1avg) / win1std) + newWin1)
                players[lKey]["All"]["Def2nd%Adj"].append((((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])) - win2avg) / win2std) + newWin2)
            if (nSurf > 10):
                players[lKey][row["Surface"]]["1stWin%Adj"].append(((row["l_1stWon"] / row["l_1stIn"] - win1avg) / win1std) - np.average(players[wKey][row["Surface"]]["Def1st%Adj"]))
                players[lKey][row["Surface"]]["2ndWin%Adj"].append(((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]) - win2avg) / win2std) - np.average(players[wKey][row["Surface"]]["Def2nd%Adj"]))
                players[lKey][row["Surface"]]["Def1st%Adj"].append((((row["w_1stWon"] / row["w_1stIn"]) - win1avg) / win1std) - np.average(players[wKey][row["Surface"]]["1stWin%Adj"]))
                players[lKey][row["Surface"]]["Def2nd%Adj"].append((((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])) - win2avg) / win2std) - np.average(players[wKey][row["Surface"]]["2ndWin%Adj"]))
            elif (nSurf > 0):
                players[lKey][row["Surface"]]["1stWin%Adj"].append(((row["l_1stWon"] / row["l_1stIn"] - win1avg) / win1std) - ((nSurf * np.average(players[wKey][row["Surface"]]["Def1st%Adj"])) + (10 - nSurf) * newDef1) / 10)
                players[lKey][row["Surface"]]["2ndWin%Adj"].append(((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]) - win2avg) / win2std) - ((nSurf * np.average(players[wKey][row["Surface"]]["Def2nd%Adj"])) + (10 - nSurf) * newDef2) / 10)
                players[lKey][row["Surface"]]["Def1st%Adj"].append((((row["w_1stWon"] / row["w_1stIn"]) - win1avg) / win1std) - ((nSurf * np.average(players[wKey][row["Surface"]]["1stWin%Adj"])) + (10 - nSurf) * newWin1) / 10)
                players[lKey][row["Surface"]]["Def2nd%Adj"].append((((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])) - win2avg) / win2std) - ((nSurf * np.average(players[wKey][row["Surface"]]["2ndWin%Adj"])) + (10 - nSurf) * newWin2) / 10)
            else:
                players[lKey][row["Surface"]]["1stWin%Adj"].append(((row["l_1stWon"] / row["l_1stIn"] - win1avg) / win1std) - newDef1)
                players[lKey][row["Surface"]]["2ndWin%Adj"].append(((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]) - win2avg) / win2std) - newDef2)
                players[lKey][row["Surface"]]["Def1st%Adj"].append((((row["w_1stWon"] / row["w_1stIn"]) - win1avg) / win1std) + newWin1)
                players[lKey][row["Surface"]]["Def2nd%Adj"].append((((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])) - win2avg) / win2std) + newWin2)

            players[wKey]["All"]["1stWin%"].append(row["w_1stWon"] / row["w_1stIn"])
            players[wKey]["All"]["1stIn%"].append(row["w_1stIn"] / row["w_svpt"])
            players[wKey]["All"]["2ndWin%"].append(row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]))
            players[wKey]["All"]["2ndIn%"].append((row["w_svpt"] - row["w_1stIn"] - row["w_df"]) / (row["w_svpt"] - row["w_1stIn"]))
            players[wKey]["All"]["Def1st%"].append((row["l_1stWon"] / row["l_1stIn"]))
            players[wKey]["All"]["Def2nd%"].append((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])))
            # players[wKey][row["Surface"]]["1stWin%"].append(row["w_1stWon"] / row["w_1stIn"])
            # players[wKey][row["Surface"]]["1stIn%"].append(row["w_1stIn"] / row["w_svpt"])
            # players[wKey][row["Surface"]]["2ndWin%"].append(row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"]))
            # players[wKey][row["Surface"]]["2ndIn%"].append((row["w_svpt"] - row["w_1stIn"] - row["w_df"]) / (row["w_svpt"] - row["w_1stIn"]))
            # players[wKey][row["Surface"]]["Def1st%"].append((row["l_1stWon"] / row["l_1stIn"]))
            # players[wKey][row["Surface"]]["Def2nd%"].append((row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"])))

            players[lKey]["All"]["1stWin%"].append(row["l_1stWon"] / row["l_1stIn"])
            players[lKey]["All"]["1stIn%"].append(row["l_1stIn"] / row["l_svpt"])
            players[lKey]["All"]["2ndWin%"].append(row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]))
            players[lKey]["All"]["2ndIn%"].append((row["l_svpt"] - row["l_1stIn"] - row["l_df"]) / (row["l_svpt"] - row["l_1stIn"]))
            players[lKey]["All"]["Def1st%"].append((row["w_1stWon"] / row["w_1stIn"]))
            players[lKey]["All"]["Def2nd%"].append((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])))
            # players[lKey][row["Surface"]]["1stWin%"].append(row["l_1stWon"] / row["l_1stIn"])
            # players[lKey][row["Surface"]]["1stIn%"].append(row["l_1stIn"] / row["l_svpt"])
            # players[lKey][row["Surface"]]["2ndWin%"].append(row["l_2ndWon"] / (row["l_svpt"] - row["l_1stIn"] - row["l_df"]))
            # players[lKey][row["Surface"]]["2ndIn%"].append((row["l_svpt"] - row["l_1stIn"] - row["l_df"]) / (row["l_svpt"] - row["l_1stIn"]))
            # players[lKey][row["Surface"]]["Def1st%"].append((row["w_1stWon"] / row["w_1stIn"]))
            # players[lKey][row["Surface"]]["Def2nd%"].append((row["w_2ndWon"] / (row["w_svpt"] - row["w_1stIn"] - row["w_df"])))
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

def logistic_regression(path="./csv_data/"):
    train = pd.read_csv(path + "preMatchExpectations_train.csv", encoding = "ISO-8859-1")
    test = pd.read_csv(path + "preMatchExpectations_test.csv", encoding = "ISO-8859-1")

    dict = {"Player 1":[], "Player 2":[], "p1_expected_1stServePoint%":[], "p1_expected_2ndServePoint%":[], "p2_expected_1stServePoint%":[], "p2_expected_2ndServePoint%":[], "p1_adj_expected_1stServePoint%":[], "p1_adj_expected_2ndServePoint%":[], "p2_adj_expected_1stServePoint%":[], "p2_adj_expected_2ndServePoint%":[], "p1_surf_adj_expected_1stServePoint%":[], "p1_surf_adj_expected_2ndServePoint%":[], "p2_surf_adj_expected_1stServePoint%":[], "p2_surf_adj_expected_2ndServePoint%":[], "P1 G":[], "P2 G":[], "Player 1 Odds":[], "Player 2 Odds":[], "Player 1 Win":[]}

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
            dict["p1_surf_adj_expected_1stServePoint%"].append(row["w_surf_adj_expected_1stServePoint%"])
            dict["p1_surf_adj_expected_2ndServePoint%"].append(row["w_surf_adj_expected_2ndServePoint%"])
            dict["p2_surf_adj_expected_1stServePoint%"].append(row["l_surf_adj_expected_1stServePoint%"])
            dict["p2_surf_adj_expected_2ndServePoint%"].append(row["l_surf_adj_expected_2ndServePoint%"])
            dict["P1 G"].append("w_gp")
            dict["P2 G"].append("l_gp")
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
            dict["p2_surf_adj_expected_1stServePoint%"].append(row["w_surf_adj_expected_1stServePoint%"])
            dict["p2_surf_adj_expected_2ndServePoint%"].append(row["w_surf_adj_expected_2ndServePoint%"])
            dict["p1_surf_adj_expected_1stServePoint%"].append(row["l_surf_adj_expected_1stServePoint%"])
            dict["p1_surf_adj_expected_2ndServePoint%"].append(row["l_surf_adj_expected_2ndServePoint%"])
            dict["P1 G"].append("l_gp")
            dict["P2 G"].append("w_gp")
            dict["Player 2 Odds"].append(row["PSW"])
            dict["Player 1 Odds"].append(row["PSL"])
            dict["Player 1 Win"].append(0)
    for key in dict:
        train[key] = dict[key]

    dict = {"Player 1":[], "Player 2":[], "p1_expected_1stServePoint%":[], "p1_expected_2ndServePoint%":[], "p2_expected_1stServePoint%":[], "p2_expected_2ndServePoint%":[], "p1_adj_expected_1stServePoint%":[], "p1_adj_expected_2ndServePoint%":[], "p2_adj_expected_1stServePoint%":[], "p2_adj_expected_2ndServePoint%":[], "p1_surf_adj_expected_1stServePoint%":[], "p1_surf_adj_expected_2ndServePoint%":[], "p2_surf_adj_expected_1stServePoint%":[], "p2_surf_adj_expected_2ndServePoint%":[], "P1 G":[], "P2 G":[], "Player 1 Odds":[], "Player 2 Odds":[], "Player 1 Win":[]}

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
            dict["p1_surf_adj_expected_1stServePoint%"].append(row["w_surf_adj_expected_1stServePoint%"])
            dict["p1_surf_adj_expected_2ndServePoint%"].append(row["w_surf_adj_expected_2ndServePoint%"])
            dict["p2_surf_adj_expected_1stServePoint%"].append(row["l_surf_adj_expected_1stServePoint%"])
            dict["p2_surf_adj_expected_2ndServePoint%"].append(row["l_surf_adj_expected_2ndServePoint%"])
            dict["P1 G"].append(row["w_gp"])
            dict["P2 G"].append(row["l_gp"])
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
            dict["p2_surf_adj_expected_1stServePoint%"].append(row["w_surf_adj_expected_1stServePoint%"])
            dict["p2_surf_adj_expected_2ndServePoint%"].append(row["w_surf_adj_expected_2ndServePoint%"])
            dict["p1_surf_adj_expected_1stServePoint%"].append(row["l_surf_adj_expected_1stServePoint%"])
            dict["p1_surf_adj_expected_2ndServePoint%"].append(row["l_surf_adj_expected_2ndServePoint%"])
            dict["P1 G"].append(row["l_gp"])
            dict["P2 G"].append(row["w_gp"])
            dict["Player 2 Odds"].append(row["PSW"])
            dict["Player 1 Odds"].append(row["PSL"])
            dict["Player 1 Win"].append(0)
    for key in dict:
        test[key] = dict[key]

    predictions = []
    y_train = train["Player 1 Win"]
    xCols = ["p1_expected_1stServePoint%", "p1_expected_2ndServePoint%", "p2_expected_1stServePoint%", "p2_expected_2ndServePoint%", "p1_adj_expected_1stServePoint%", "p1_adj_expected_2ndServePoint%", "p2_adj_expected_1stServePoint%", "p2_adj_expected_2ndServePoint%", "p1_surf_adj_expected_1stServePoint%", "p1_surf_adj_expected_2ndServePoint%", "p2_surf_adj_expected_1stServePoint%", "p2_surf_adj_expected_2ndServePoint%"]
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


    test.to_csv(path + "predictions2.csv", index = False)
