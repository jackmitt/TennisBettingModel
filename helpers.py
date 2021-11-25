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

def MC_game(in1, win1, in2, win2, bpWin = -1, mcmc = False, num_sim = 1000):
    if (mcmc):
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
    else:
        p = in1 * win1 + (1 - in1) * in2 * (win2)
        if (bpWin == -1):
            bp = in1 * win1 + (1 - in1) * in2 * (win2)
        else:
            bp = bpWin
        return (p**2*(5*p**2 - 4*p**3 + 4*(p-1)**2*p*bp - (2*(p-1)**2*bp**2*(p*(4*bp-2)-2*bp-3))/(2*bp**2-2*bp+1)))

#https://www.researchgate.net/publication/318135127_A_new_markovian_model_for_tennis_matches
#https://www.cis.upenn.edu/~bhusnur4/cit592_fall2013/NeKe2005.pdf
def set_prob(p1_in1, p1_win1, p1_in2, p1_win2, p2_in1, p2_win1, p2_in2, p2_win2):
    #pa = p1 serve win      qb = p1 return win      pb = p2 serve win       qa = p2 return win
    pa = p1_in1 * p1_win1 + (1 - p1_in1) * p1_in2 * (p1_win2)
    qa = 1 - pa
    pb = p2_in1 * p2_win1 + (1 - p2_in1) * p2_in2 * (p2_win2)
    qb = 1 - pb
    #tiebreak cases: 7-0, 7-1, 7-2, 7-3, 7-4, 7-5, *win 2 in a row after 6-6* --- the union of these cases is the prob of p1 winning the set, 1 - the union for p2
    tc1 = pa**3*qb**4
    tc2 = 3*pa**3*qa*qb**4 + 4*pa**4*pb*qb**3
    tc3 = 16*pa**4*qa*pb*qb**3 + 6*pa**5*pb**2*qb**2 + 6*pa**3*qa**2*qb**4
    tc4 = 40*pa**3*qa**2*pb*qb**4 + 10*pa**2*qa**3*qb**5 + 4*pa**5*pb**3*qb**2 + 30*pa**4*qa*pb**2*qb**3
    tc5 = 50*pa**4*qa*pb**3*qb**3 + 5*pa**5*pb**4*qb**2 + 50*pa**2*qa**3*pb*qb**5 + 5*pa*qa**4*qb**6 + 100*pa**3*qa**2*pb**2*qb**4
    tc6 = 30*pa**2*qa**4*pb*qb**5 + pa*qa**5*qb**6 + 200*pa**4*qa**2*pb**3*qb**3 + 75*pa**5*qa*pb**4*qb**2 + 150*pa**3*qa**3*pb**2*qb**4 + 6*pa**6*pb**5*qb
    tc1x = pb**3*qa**4
    tc2x = 3*pb**3*qb*qa**4 + 4*pb**4*pa*qa**3
    tc3x = 16*pb**4*qb*pa*qa**3 + 6*pb**5*pa**2*qa**2 + 6*pb**3*qb**2*qa**4
    tc4x = 40*pb**3*qb**2*pa*qa**4 + 10*pb**2*qb**3*qa**5 + 4*pb**5*pa**3*qa**2 + 30*pb**4*qb*pa**2*qa**3
    tc5x = 50*pb**4*qb*pa**3*qa**3 + 5*pb**5*pa**4*qa**2 + 50*pb**2*qb**3*pa*qa**5 + 5*pb*qb**4*qa**6 + 100*pb**3*qb**2*pa**2*qa**4
    tc6x = 30*pb**2*qb**4*pa*qa**5 + pb*qb**5*qa**6 + 200*pb**4*qb**2*pa**3*qa**3 + 75*pb**5*qb*pa**4*qa**2 + 150*pb**3*qb**3*pa**2*qa**4 + 6*pb**6*pa**5*qa
    tc7 = (1 - (tc1 + tc2 + tc3 + tc4 + tc5 + tc6 + tc1x + tc2x + tc3x + tc4x + tc5x + tc6x)) * (pa*qb) / (1 - pa*pb - qa*qb)
    p1_tiebreak_win = tc1 + tc2 + tc3 + tc4 + tc5 + tc6 + tc7
    #aa - p1 serve win      ba = p1 return win      bb = p2 serve win       ab = p2 return win
    aa = MC_game(p1_in1, p1_win1, p1_in2, p1_win2)
    ab = 1 - aa
    bb = MC_game(p2_in1, p2_win1, p2_in2, p2_win2)
    ba = 1 - bb
    #cases (from p1 perspective): 6-0, 6-1, 6-2, 6-3, 6-4, 7-5, 7-6 --- the union of these cases is the prob of p1 winning the set, 1 - the union for p2
    c1 = aa**3 * ba**3
    c2 = 3*aa**4*bb*ba**2 + 3*aa**3*ab*ba**3
    c3 = 3*aa**4*bb**2*ba**2 + 12*aa**3*bb*ab*ba**3 + 6*aa**2*ab**2*ba**4
    c4 = 4*aa**5*bb**3*ba + 24*aa**4*ab*bb**2*ba**2 + 24*aa**3*ab**2*bb*ba**3 + 4*aa**2*ab**3*ba**4
    c5 = aa**5*bb**4*ba + 20*aa**4*ab*bb**3*ba**2 + 60*aa**3*ab**2*bb**2*ba**3 + 40*aa**2*ab**3*bb*ba**4 + 5*aa*ab**4*ba**5
    c6 = aa**6*bb**5*ba + 25*aa**5*ab*bb**4*ba**2 + 100*aa**4*ab**2*bb**3*ba**3 + 100*aa**3*ab**3*bb**2*ba**4 + 25*aa**2*ab**4*bb*ba**5 + aa*ab**5*ba**6
    c7 = p1_tiebreak_win * (aa**6*bb**6 + 26*aa**5*ab*bb**5*ba + 125*aa**4*ab**2*bb**4*ba**2 + 200*aa**3*ab**3*bb**3*ba**3 + 250*aa**2*ab**4*bb**2*ba**4 + 26*aa*ab**5*bb*ba**5 + ab**6*ba**6)
    return (c1 + c2 + c3 + c4 + c5 + c6 + c7)
