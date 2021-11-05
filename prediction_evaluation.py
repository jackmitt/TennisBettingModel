import pandas as pd
import numpy as np
import datetime

def kellyStake(p, decOdds):
    return (p - (1 - p)/(decOdds - 1))

def simulateKellyBets(bankroll, kellyDiv = 1, pred_path = "./csv_data/predictions.csv"):
    pred = pd.read_csv(pred_path, encoding = "ISO-8859-1")
    baseBR = bankroll
    netSum = 0
    myEdge = []
    actEdge = []
    for index, row in pred.iterrows():
        if (row["Player 1 Prob"] > 1 / row["Player 1 Odds"]):
            myEdge.append(row["Player 1 Prob"] - 1 / row["Player 1 Odds"])
            actEdge.append(row["Player 1 Win"] - 1 / row["Player 1 Odds"])
            if (row["Player 1 Win"] == 1):
                bankroll += bankroll * kellyStake(row["Player 1 Prob"], row["Player 1 Odds"]) * (row["Player 1 Odds"] - 1) / kellyDiv
                netSum += baseBR * kellyStake(row["Player 1 Prob"], row["Player 1 Odds"]) * (row["Player 1 Odds"] - 1) / kellyDiv
            elif (row["Player 1 Win"] == 0):
                bankroll -= bankroll * kellyStake(row["Player 1 Prob"], row["Player 1 Odds"]) / kellyDiv
                netSum -= baseBR * kellyStake(row["Player 1 Prob"], row["Player 1 Odds"]) / kellyDiv
        elif (1 - row["Player 1 Prob"] > 1 / row["Player 2 Odds"]):
            myEdge.append(1 - row["Player 1 Prob"] - 1 / row["Player 2 Odds"])
            actEdge.append(1 - row["Player 1 Win"] - 1 / row["Player 2 Odds"])
            if (row["Player 1 Win"] == 0):
                bankroll += bankroll * kellyStake(1 - row["Player 1 Prob"], row["Player 2 Odds"]) * (row["Player 2 Odds"] - 1) / kellyDiv
                netSum += baseBR * kellyStake(1 - row["Player 1 Prob"], row["Player 2 Odds"]) * (row["Player 2 Odds"] - 1) / kellyDiv
            elif (row["Player 1 Win"] == 1):
                bankroll -= bankroll * kellyStake(1 - row["Player 1 Prob"], row["Player 2 Odds"]) / kellyDiv
                netSum -= baseBR * kellyStake(1 - row["Player 1 Prob"], row["Player 2 Odds"]) / kellyDiv
        else:
            myEdge.append(np.nan)
            actEdge.append(np.nan)
        print (bankroll)
    pred["My Edge"] = myEdge
    pred["Actual Edge"] = actEdge
    pred.to_csv("./csv_data/predictions.csv", index = False)
    print(netSum)

def simulateFixedBets(bankroll, pred_path = "./csv_data/predictions.csv"):
    pred = pd.read_csv(pred_path, encoding = "ISO-8859-1")
    size = bankroll * 0.01
    for index, row in pred.iterrows():
        if (row["Player 1 Prob"] > 1 / row["Player 1 Odds"]):
            if (row["Player 1 Win"] == 1):
                bankroll += size * (row["Player 1 Odds"] - 1)
            elif (row["Player 1 Win"] == 0):
                bankroll -= size
        elif (1 - row["Player 1 Prob"] > 1 / row["Player 2 Odds"]):
            if (row["Player 1 Win"] == 0):
                bankroll += size * (row["Player 2 Odds"] - 1)
            elif (row["Player 1 Win"] == 1):
                bankroll -= size
        print (bankroll)
