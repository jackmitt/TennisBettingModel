import numpy as np
import pandas as pd
import datetime
import random

def same_name(betName, statName):
    betName = betName.lower()
    statName = statName.lower()
    bLast = ""
    sLast = ""
    for x in betName.split():
        if (x == betName.split()[len(betName.split()) - 1]):
            bFirstLetter = x.split(".")[0]
            break
        bLast = bLast + x
    bLast = bLast.replace("-", "")
    bLast = bLast.replace("'", "")
    for x in statName.split():
        if (x == statName.split()[0]):
            sFirstLetter = statName.split()[0][0]
            continue
        sLast = sLast + x
    sLast = sLast.replace("-", "")
    sLast = sLast.replace("'", "")
    if ((bLast in sLast or sLast in bLast) and sFirstLetter == bFirstLetter):
        return (True)
    else:
        return (False)

def last_f_convert(firstLast):
    firstLast = firstLast.lower()
    sLast = ""
    for x in firstLast.split():
        if (x == firstLast.split()[0]):
            sFirstLetter = firstLast.split()[0][0]
            continue
        sLast = sLast + x
    sLast = sLast.replace("-", "")
    sLast = sLast.replace("'", "")
    return (sLast + " " + sFirstLetter + '.')

def cleanBetName(lastF):
    lastF = lastF.lower()
    bLast = ""
    for x in lastF.split():
        if (x == lastF.split()[len(lastF.split()) - 1]):
            bFirstLetter = x.split(".")
            break
        bLast = bLast + x
    bLast = bLast.replace("-", "")
    bLast = bLast.replace("'", "")
    return (bLast, bFirstLetter)

def logit(pct):
    return (-np.log(1/(pct) - 1))

class player:
    def __init__(self, keys, cats, info):
        self.keys = keys
        self.cats = cats
        self.dict = {"id":info[0],"name":info[1],"height":info[2]}
        for cat in cats:
            for i in range(len(keys)):
                self.dict[cat + "_" + keys[i]] = []

    def add_match_stats(self, row, wl):
        if (wl == "w"):
            wlT = "l"
        else:
            wlT = "w"
        for cat in self.cats:
            if ((cat == "hard" and cat != row["Surface"].lower()) or (cat == "clay" and cat != row["Surface"].lower()) or (cat == "grass" and cat != row["Surface"].lower())):
                continue
            self.dict[cat + "_1stWin%"].append(row[wl + "_1stWon"] / row[wl + "_1stIn"])
            self.dict[cat + "_1stIn%"].append(row[wl + "_1stIn"] / row[wl + "_svpt"])
            self.dict[cat + "_1stWin*In%"].append((row[wl + "_1stWon"] / row[wl + "_1stIn"]) * (row[wl + "_1stIn"] / row[wl + "_svpt"]))
            self.dict[cat + "_2ndWin%"].append(row[wl + "_2ndWon"] / (row[wl + "_svpt"] - row[wl + "_1stIn"] - row[wl + "_df"]))
            self.dict[cat + "_2ndIn%"].append((row[wl + "_svpt"] - row[wl + "_1stIn"] - row[wl + "_df"]) / (row[wl + "_svpt"] - row[wl + "_1stIn"]))
            self.dict[cat + "_2ndWin*In%"].append((row[wl + "_2ndWon"] / (row[wl + "_svpt"] - row[wl + "_1stIn"] - row[wl + "_df"])) * ((row[wl + "_svpt"] - row[wl + "_1stIn"] - row[wl + "_df"]) / (row[wl + "_svpt"] - row[wl + "_1stIn"])))
            self.dict[cat + "_1stRtnWin%"].append(1 - (row[wlT + "_1stWon"] / row[wlT + "_1stIn"]))
            self.dict[cat + "_2ndRtnWin%"].append(1 - (row[wlT + "_2ndWon"] / (row[wlT + "_svpt"] - row[wlT + "_1stIn"] - row[wlT + "_df"])))
            self.dict[cat + "_Ace%"].append(row[wl + "_ace"] / row[wl + "_svpt"])
            self.dict[cat + "_RtnSrv%"].append(1 - row[wlT + "_ace"] / row[wlT + "_svpt"])
            self.dict[cat + "_AcePer1stIn"].append(row[wl + "_ace"] / row[wl + "_1stIn"])
            self.dict[cat + "_Df%"].append(row[wl + "_df"] / row[wl + "_svpt"])
            self.dict[cat + "_DfPer2ndSrv"].append(row[wl + "_df"] / (row[wl + "_svpt"] - row[wl + "_1stIn"]))
            self.dict[cat + "_1stSrvEff"].append((row[wl + "_1stWon"] / row[wl + "_1stIn"]) / (row[wl + "_2ndWon"] / (row[wl + "_svpt"] - row[wl + "_1stIn"] - row[wl + "_df"])))
            self.dict[cat + "_Def1stSrvEff"].append((row[wlT + "_1stWon"] / row[wlT + "_1stIn"]) / (row[wlT + "_2ndWon"] / (row[wlT + "_svpt"] - row[wlT + "_1stIn"] - row[wlT + "_df"])))
            self.dict[cat + "_SrvRating"].append((row[wl + "_ace"] / row[wl + "_svpt"]) - (row[wl + "_df"] / row[wl + "_svpt"]) + (row[wl + "_1stIn"] / row[wl + "_svpt"]) + (row[wl + "_1stWon"] / row[wl + "_1stIn"]) + (row[wl + "_2ndWon"] / (row[wl + "_svpt"] - row[wl + "_1stIn"] - row[wl + "_df"])))
            self.dict[cat + "_OppSrvRating"].append((row[wlT + "_ace"] / row[wlT + "_svpt"]) - (row[wlT + "_df"] / row[wlT + "_svpt"]) + (row[wlT + "_1stIn"] / row[wlT + "_svpt"]) + (row[wlT + "_1stWon"] / row[wlT + "_1stIn"]) + (row[wlT + "_2ndWon"] / (row[wlT + "_svpt"] - row[wlT + "_1stIn"] - row[wlT + "_df"])))
            try:
                self.dict[cat + "_BpSaved%"].append(row[wl + "_bpSaved"] / row[wl + "_bpFaced"])
            except:
                pass
            try:
                self.dict[cat + "_BpWon%"].append(1 - row[wlT + "_bpSaved"] / row[wlT + "_bpFaced"])
            except:
                pass
            self.dict[cat + "_RtnRating"].append((1 - (row[wlT + "_1stWon"] / row[wlT + "_1stIn"])) + (1 - (row[wlT + "_2ndWon"] / (row[wlT + "_svpt"] - row[wlT + "_1stIn"] - row[wlT + "_df"]))))
            self.dict[cat + "_OppRtnRating"].append((1 - (row[wl + "_1stWon"] / row[wl + "_1stIn"])) + (1 - (row[wl + "_2ndWon"] / (row[wl + "_svpt"] - row[wl + "_1stIn"] - row[wl + "_df"]))))
            self.dict[cat + "_Date"].append(datetime.date(int(row["Date"].split("/")[2]), int(row["Date"].split("/")[0]), int(row["Date"].split("/")[1])))

    def update_form(self, today, med_form_days = 548, short_form_days = 182):
        for i in range(len(self.dict["mf_Date"])):
            if (abs(today - self.dict["mf_Date"][i]).days < med_form_days):
                for key in self.keys:
                    del self.dict["mf_" + key][:i]
                break
        for i in range(len(self.dict["sf_Date"])):
            if (abs(today - self.dict["sf_Date"][i]).days < short_form_days):
                for key in self.keys:
                    del self.dict["sf_" + key][:i]
                break

    def get_avg(self, cat, key):
        if (key == "gp"):
            return (self.gp(ref = cat))
        return (np.average(self.dict[cat + "_" + key]))


    def gp(self, ref = "lf"):
        if (ref == "lf"):
            return (len(dict[self.cats[0] + "_" + self.keys[0]]))
        else:
            return (len(dict[ref + "_" + self.keys[0]]))

def MCMC_game(in1, win1, in2, win2, num_sim = 1000):
    #states: (0,0), (15,0), (0,15), (30,0), (15,15), (0,30), (40,0), (30,15), (15,30), (0,40), (40,15), (15,40), deuce, adv_server, adv_returner, win_server, win_returner
    sw = in1 * win1 + (1 - in1) * in2 * (win2)
    rw = 1 - sw
    markov_chain = []
    for i in range(17):
        markov_chain.append([])
        for k in range(17):
            markov_chain[i].append(0)
    markov_chain[0][1] = sw
    markov_chain[0][2] = rw
    markov_chain[1][3] = sw
    markov_chain[1][4] = rw
    markov_chain[2][4] = sw
    markov_chain[2][5] = rw
    markov_chain[3][6] = sw
    markov_chain[3][7] = rw
    markov_chain[4][7] = sw
    markov_chain[4][8] = rw
    markov_chain[5][8] = sw
    markov_chain[5][9] = rw
    markov_chain[6][15] = sw
    markov_chain[6][10] = rw
    markov_chain[7][10] = sw
    markov_chain[7][12] = rw
    markov_chain[8][12] = sw
    markov_chain[8][11] = rw
    markov_chain[9][11] = sw
    markov_chain[9][16] = rw
    markov_chain[10][15] = sw
    markov_chain[10][13] = rw
    markov_chain[11][14] = sw
    markov_chain[11][16] = rw
    markov_chain[12][13] = sw
    markov_chain[12][14] = rw
    markov_chain[13][15] = sw
    markov_chain[13][12] = rw
    markov_chain[14][12] = sw
    markov_chain[14][16] = rw
    markov_chain[15][15] = 1
    markov_chain[16][16] = 1


    serve_wins = 0
    for i in range(num_sim):
        cur_state = 0
        while (cur_state != 15 and cur_state != 16):
            rng = random.randint(0, 10000) / 10000
            total = 0
            for j in range(17):
                total += markov_chain[cur_state][j]
                if (rng < total):
                    cur_state = j
                    break
        if (cur_state == 15):
            serve_wins += 1

    return (serve_wins / num_sim)
