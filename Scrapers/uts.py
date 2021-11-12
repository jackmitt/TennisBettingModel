from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
import time
from os.path import exists

if (not exists("./tourney_urls.csv")):
    tourney_urls = []
    browser = webdriver.Chrome(executable_path='chromedriver.exe')
    browser.get("https://www.ultimatetennisstatistics.com/tournamentEvents")
    browser.maximize_window()
    time.sleep(3)
    browser.refresh()
    time.sleep(3)
    browser.find_element_by_xpath("//*[@id='cookiesNotification']/button").click()
    while (1):
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        if (int(soup.find("tbody").find("tr").find("td").text.split("-")[2]) < 1991):
            break
        for row in soup.find("tbody").find_all("tr"):
            tourney_urls.append(row.find_all("td")[1].find("a")["href"])
        browser.find_element_by_xpath("//*[@id='tournamentEventsTable-footer']/div/div[1]/ul/li[8]/a").click()
        time.sleep(3)
    save = {}
    save["urls"] = tourney_urls
    dfFinal = pd.DataFrame.from_dict(save)
    dfFinal = dfFinal.drop_duplicates()
    dfFinal.to_csv("./tourney_urls.csv", index = False)
    browser.close()

if (not exists("./uts_stats.csv")):
    dict = {"date":[],"tournament":[],"level":[],"surface":[],"speed":[],"winner":[],"loser":[],"match_time":[],"point_time_sec":[],"game_time_min":[],"set_time_min":[],"total_games_played":[]}
    for x in (["w_","l_"]):
        dict[x + "ace%"] = []
        dict[x + "df%"] = []
        dict[x + "1st_serve_in%"] = []
        dict[x + "1st_serve_won%"] = []
        dict[x + "2nd_serve_won%"] = []
        dict[x + "break_pts_saved%"] = []
        dict[x + "svc_pts_won%"] = []
        dict[x + "1st_serve_rtn_won%"] = []
        dict[x + "2nd_serve_rtn_won%"] = []
        dict[x + "break_pts_won%"] = []
        dict[x + "rtn_pts_won%"] = []
        dict[x + "pts_dominance"] = []
        dict[x + "total_pts_won%"] = []
        dict[x + "aces"] = []
        dict[x + "aces_per_svc_game"] = []
        dict[x + "aces_per_set"] = []
        dict[x + "dfs"] = []
        dict[x + "dfs_per_2nd_serve%"] = []
        dict[x + "dfs_per_svc_game"] = []
        dict[x + "dfs_per_set"] = []
        dict[x + "aces_to_dfs_ratio"] = []
        dict[x + "1st_serve_effectiveness"] = []
        dict[x + "serve_rating"] = []
        dict[x + "svc_in_play_pts_won%"] = []
        dict[x + "pts_per_svc_game"] = []
        dict[x + "pts_lost_per_svc_game"] = []
        dict[x + "bps_per_svc_game"] = []
        dict[x + "svc_bps_per_set"] = []
        dict[x + "svc_games_won%"] = []
        dict[x + "svc_games_lost_per_set"] = []
        dict[x + "rtn_rating"] = []
        dict[x + "total_pts_won%"] = []
        dict[x + "rtn_in_play_pts_won%"] = []
        dict[x + "pts_per_rtn_game"] = []
        dict[x + "pts_won_per_rtn_game"] = []
        dict[x + "bps_per_rtn_game"] = []
        dict[x + "rtn_bps_per_set"] = []
        dict[x + "winner%"] = []
        dict[x + "unforced_error%"] = []
        dict[x + "forced_error%"] = []
        dict[x + "winners_to_UE_ratio"] = []
        dict[x + "winners_to_FE_against_ratio"] = []
        dict[x + "net_pts%"] = []
        dict[x + "net_pts_won%"] = []
        dict[x + "pts_won_at_net%"] = []
        dict[x + "max_serve_speed"] = []
        dict[x + "1st_serve_avg_speed"] = []
        dict[x + "2nd_serve_avg_speed"] = []
        dict[x + "avg_serve_speed"] = []
        dict[x + "1st_to_2nd_serve_speed_ratio"] = []
        dict[x + "max_to_avg_speed_ratio"] = []
        dict[x + "total_pts_played"] = []
        dict[x + "total_pts_won"] = []
        dict[x + "total_pts_won%"] = []
        dict[x + "rtn_to_svc_pts_ratio"] = []
        dict[x + "total_games_won"] = []
        dict[x + "games_won%"] = []
        dict[x + "games_dominance"] = []
        dict[x + "break_pts_ratio"] = []
else:
    dict = pd.read_csv("./uts_stats.csv", encoding = "ISO-8859-1").to_dict(orient="list")
    dict["tourney url"] = []
    for i in range(len(dict["date"])):
        dict["tourney url"].append(np.nan)

count = 0
urls = pd.read_csv("./tourney_urls.csv", encoding = "ISO-8859-1").to_dict(orient="list")["urls"]
browser = webdriver.Chrome(executable_path='chromedriver.exe')
browser.get("https://www.ultimatetennisstatistics.com/" + urls[0])
browser.maximize_window()
time.sleep(3)
browser.refresh()
time.sleep(3)
for tourney in urls:
    browser.get("https://www.ultimatetennisstatistics.com/" + tourney)
    time.sleep(3)
    games = []
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    for a in soup.find_all("a"):
        if (a.has_attr("id") and "matchStats" in a["id"]):
            games.append(a["id"].split("matchStats-")[1])
    for game in games:
        count += 1
        left = 0
        right = 0
        while(1):
            try:
                element = browser.find_element_by_xpath("//*[@id='matchStats-" + game + "']")
                browser.execute_script("arguments[0].scrollIntoView();", element)
                browser.find_element_by_xpath("//*[@id='matchStats-" + game + "']").click()
                break
            except:
                if (left < 4 and right == 0):
                    browser.find_element_by_xpath("//*[@id='roundLeft']").click()
                    left += 1
                else:
                    left = 0
                    browser.find_element_by_xpath("//*[@id='roundRight']").click()
                    right += 1
                    if (right == 4):
                        right = 0
        time.sleep(2)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        popup = soup.find(id = "matchStatsPopover-" + game)
        try:
            dict["match_time"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[16].find(class_="text-left").text)
        except:
            browser.find_element_by_xpath("//*[@id='matchStatsPopover-" + game + "']/div[3]/div[2]/button").click()
            continue
        dict["tourney url"].append(game)
        dict["date"].append(soup.find(class_="table table-condensed text-nowrap").find_all("tr")[2].find("td").text)
        dict["tournament"].append(soup.find("h3").get_text())
        dict["level"].append(soup.find(class_="table table-condensed text-nowrap").find_all("tr")[0].find("span").text)
        dict["surface"].append(soup.find(class_="table table-condensed text-nowrap").find_all("tr")[1].find("span").get_text())
        dict["speed"].append(soup.find(class_="table table-condensed text-nowrap").find_all("tr")[1].find(id="eventSpeed").text)
        dict["winner"].append(popup.find_all("b")[0].text)
        dict["loser"].append(popup.find_all("b")[2].text)
        dict["total_games_played"].append(popup.find(id="matchStats-" + game + "Total").find_all("tr")[5].find(class_="text-right").text)
        dict["point_time_sec"].append(popup.find(id="matchStats-" + game + "Total").find_all("tr")[13].find(class_="text-left").text)
        dict["game_time_min"].append(popup.find(id="matchStats-" + game + "Total").find_all("tr")[14].find(class_="text-left").text)
        dict["set_time_min"].append(popup.find(id="matchStats-" + game + "Total").find_all("tr")[15].find(class_="text-left").text)
        for x in ["w_","l_"]:
            if (x == "w_"):
                try:
                    dict[x + "ace%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[1].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "ace%"].append(np.nan)
                try:
                    dict[x + "df%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[2].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "df%"].append(np.nan)
                try:
                    dict[x + "1st_serve_in%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[3].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "1st_serve_in%"].append(np.nan)
                try:
                    dict[x + "1st_serve_won%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[4].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "1st_serve_won%"].append(np.nan)
                try:
                    dict[x + "2nd_serve_won%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[5].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "2nd_serve_won%"].append(np.nan)
                try:
                    dict[x + "break_pts_saved%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[6].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "break_pts_saved%"].append(np.nan)
                try:
                    dict[x + "svc_pts_won%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[7].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "svc_pts_won%"].append(np.nan)
                try:
                    dict[x + "1st_serve_rtn_won%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[9].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "1st_serve_rtn_won%"].append(np.nan)
                try:
                    dict[x + "2nd_serve_rtn_won%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[10].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "2nd_serve_rtn_won%"].append(np.nan)
                try:
                    dict[x + "break_pts_won%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[11].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "break_pts_won%"].append(np.nan)
                try:
                    dict[x + "rtn_pts_won%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[12].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "rtn_pts_won%"].append(np.nan)
                try:
                    dict[x + "pts_dominance"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[14].find(class_="text-right").text)
                except:
                    dict[x + "pts_dominance"].append(np.nan)
                try:
                    dict[x + "total_pts_won%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[15].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "total_pts_won%"].append(np.nan)
                try:
                    dict[x + "aces"].append(popup.find(id="matchStats-" + game + "AcesDFs").find_all("tr")[1].find(class_="text-right").text)
                except:
                    dict[x + "aces"].append(np.nan)
                try:
                    dict[x + "aces_per_svc_game"].append(popup.find(id="matchStats-" + game + "AcesDFs").find_all("tr")[3].find(class_="text-right pct-data").text)
                except:
                    dict[x + "aces_per_svc_game"].append(np.nan)
                try:
                    dict[x + "aces_per_set"].append(popup.find(id="matchStats-" + game + "AcesDFs").find_all("tr")[4].find(class_="text-right pct-data").text)
                except:
                    dict[x + "aces_per_set"].append(np.nan)
                try:
                    dict[x + "dfs"].append(popup.find(id="matchStats-" + game + "AcesDFs").find_all("tr")[6].find(class_="text-right").text)
                except:
                    dict[x + "dfs"].append(np.nan)
                try:
                    dict[x + "dfs_per_2nd_serve%"].append(popup.find(id="matchStats-" + game + "AcesDFs").find_all("tr")[8].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "dfs_per_2nd_serve%"].append(np.nan)
                try:
                    dict[x + "dfs_per_svc_game"].append(popup.find(id="matchStats-" + game + "AcesDFs").find_all("tr")[9].find(class_="text-right pct-data").text)
                except:
                    dict[x + "dfs_per_svc_game"].append(np.nan)
                try:
                    dict[x + "dfs_per_set"].append(popup.find(id="matchStats-" + game + "AcesDFs").find_all("tr")[10].find(class_="text-right pct-data").text)
                except:
                    dict[x + "dfs_per_set"].append(np.nan)
                try:
                    dict[x + "aces_to_dfs_ratio"].append(popup.find(id="matchStats-" + game + "AcesDFs").find_all("tr")[12].find(class_="text-right pct-data").text)
                except:
                    dict[x + "aces_to_dfs_ratio"].append(np.nan)
                try:
                    dict[x + "1st_serve_effectiveness"].append(popup.find(id="matchStats-" + game + "Serve").find_all("tr")[4].find(class_="text-right").text)
                except:
                    dict[x + "1st_serve_effectiveness"].append(np.nan)
                try:
                    dict[x + "serve_rating"].append(popup.find(id="matchStats-" + game + "Serve").find_all("tr")[5].find(class_="text-right").text)
                except:
                    dict[x + "serve_rating"].append(np.nan)
                try:
                    dict[x + "svc_in_play_pts_won%"].append(popup.find(id="matchStats-" + game + "Serve").find_all("tr")[8].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "svc_in_play_pts_won%"].append(np.nan)
                try:
                    dict[x + "pts_per_svc_game"].append(popup.find(id="matchStats-" + game + "Serve").find_all("tr")[9].find(class_="text-right pct-data").text)
                except:
                    dict[x + "pts_per_svc_game"].append(np.nan)
                try:
                    dict[x + "pts_lost_per_svc_game"].append(popup.find(id="matchStats-" + game + "Serve").find_all("tr")[10].find(class_="text-right pct-data").text)
                except:
                    dict[x + "pts_lost_per_svc_game"].append(np.nan)
                try:
                    dict[x + "bps_per_svc_game"].append(popup.find(id="matchStats-" + game + "Serve").find_all("tr")[12].find(class_="text-right pct-data").text)
                except:
                    dict[x + "bps_per_svc_game"].append(np.nan)
                try:
                    dict[x + "svc_bps_per_set"].append(popup.find(id="matchStats-" + game + "Serve").find_all("tr")[13].find(class_="text-right pct-data").text)
                except:
                    dict[x + "svc_bps_per_set"].append(np.nan)
                try:
                    dict[x + "svc_games_won%"].append(popup.find(id="matchStats-" + game + "Serve").find_all("tr")[15].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "svc_games_won%"].append(np.nan)
                try:
                    dict[x + "svc_games_lost_per_set"].append(popup.find(id="matchStats-" + game + "Serve").find_all("tr")[16].find(class_="text-right pct-data").text)
                except:
                    dict[x + "svc_games_lost_per_set"].append(np.nan)
                try:
                    dict[x + "rtn_rating"].append(popup.find(id="matchStats-" + game + "Return").find_all("tr")[3].find(class_="text-right").text)
                except:
                    dict[x + "rtn_rating"].append(np.nan)
                try:
                    dict[x + "rtn_in_play_pts_won%"].append(popup.find(id="matchStats-" + game + "Return").find_all("tr")[6].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "rtn_in_play_pts_won%"].append(np.nan)
                try:
                    dict[x + "pts_per_rtn_game"].append(popup.find(id="matchStats-" + game + "Return").find_all("tr")[7].find(class_="text-right pct-data").text)
                except:
                    dict[x + "pts_per_rtn_game"].append(np.nan)
                try:
                    dict[x + "pts_won_per_rtn_game"].append(popup.find(id="matchStats-" + game + "Return").find_all("tr")[8].find(class_="text-right pct-data").text)
                except:
                    dict[x + "pts_won_per_rtn_game"].append(np.nan)
                try:
                    dict[x + "bps_per_rtn_game"].append(popup.find(id="matchStats-" + game + "Return").find_all("tr")[10].find(class_="text-right pct-data").text)
                except:
                    dict[x + "bps_per_rtn_game"].append(np.nan)
                try:
                    dict[x + "rtn_bps_per_set"].append(popup.find(id="matchStats-" + game + "Return").find_all("tr")[11].find(class_="text-right pct-data").text)
                except:
                    dict[x + "rtn_bps_per_set"].append(np.nan)
                try:
                    dict[x + "winner%"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[1].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "winner%"].append(np.nan)
                try:
                    dict[x + "unforced_error%"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[2].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "unforced_error%"].append(np.nan)
                try:
                    dict[x + "forced_error%"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[3].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "forced_error%"].append(np.nan)
                try:
                    dict[x + "winners_to_UE_ratio"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[4].find(class_="text-right pct-data").text)
                except:
                    dict[x + "winners_to_UE_ratio"].append(np.nan)
                try:
                    dict[x + "winners_to_FE_against_ratio"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[5].find(class_="text-right pct-data").text)
                except:
                    dict[x + "winners_to_FE_against_ratio"].append(np.nan)
                try:
                    dict[x + "net_pts%"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[7].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "net_pts%"].append(np.nan)
                try:
                    dict[x + "net_pts_won%"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[8].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "net_pts_won%"].append(np.nan)
                try:
                    dict[x + "pts_won_at_net%"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[9].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "pts_won_at_net%"].append(np.nan)
                try:
                    dict[x + "max_serve_speed"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[11].find(class_="text-right").text.split(" km/h")[0])
                except:
                    dict[x + "max_serve_speed"].append(np.nan)
                try:
                    dict[x + "1st_serve_avg_speed"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[12].find(class_="text-right").text.split(" km/h")[0])
                except:
                    dict[x + "1st_serve_avg_speed"].append(np.nan)
                try:
                    dict[x + "2nd_serve_avg_speed"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[13].find(class_="text-right").text.split(" km/h")[0])
                except:
                    dict[x + "2nd_serve_avg_speed"].append(np.nan)
                try:
                    dict[x + "avg_serve_speed"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[14].find(class_="text-right").text.split(" km/h")[0])
                except:
                    dict[x + "avg_serve_speed"].append(np.nan)
                try:
                    dict[x + "1st_to_2nd_serve_speed_ratio"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[15].find(class_="text-right pct-data").text)
                except:
                    dict[x + "1st_to_2nd_serve_speed_ratio"].append(np.nan)
                try:
                    dict[x + "max_to_avg_speed_ratio"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[16].find(class_="text-right pct-data").text)
                except:
                    dict[x + "max_to_avg_speed_ratio"].append(np.nan)
                try:
                    dict[x + "total_pts_played"].append(popup.find(id="matchStats-" + game + "Total").find_all("tr")[1].find(class_="text-right").text)
                except:
                    dict[x + "total_pts_played"].append(np.nan)
                try:
                    dict[x + "total_pts_won"].append(popup.find(id="matchStats-" + game + "Total").find_all("tr")[2].find(class_="text-right").text)
                except:
                    dict[x + "total_pts_won"].append(np.nan)
                try:
                    dict[x + "rtn_to_svc_pts_ratio"].append(popup.find(id="matchStats-" + game + "Total").find_all("tr")[4].find(class_="text-right pct-data").text)
                except:
                    dict[x + "rtn_to_svc_pts_ratio"].append(np.nan)
                try:
                    dict[x + "total_games_won"].append(popup.find(id="matchStats-" + game + "Total").find_all("tr")[6].find(class_="text-right").text)
                except:
                    dict[x + "total_games_won"].append(np.nan)
                try:
                    dict[x + "games_won%"].append(popup.find(id="matchStats-" + game + "Total").find_all("tr")[7].find(class_="text-right pct-data").text.split("%")[0])
                except:
                    dict[x + "games_won%"].append(np.nan)
                try:
                    dict[x + "games_dominance"].append(popup.find(id="matchStats-" + game + "Total").find_all("tr")[10].find(class_="text-right").text)
                except:
                    dict[x + "games_dominance"].append(np.nan)
                try:
                    dict[x + "break_pts_ratio"].append(popup.find(id="matchStats-" + game + "Total").find_all("tr")[11].find(class_="text-right").text)
                except:
                    dict[x + "break_pts_ratio"].append(np.nan)
            else:
                try:
                    dict[x + "ace%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[1].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "ace%"].append(np.nan)
                try:
                    dict[x + "df%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[2].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "df%"].append(np.nan)
                try:
                    dict[x + "1st_serve_in%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[3].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "1st_serve_in%"].append(np.nan)
                try:
                    dict[x + "1st_serve_won%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[4].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "1st_serve_won%"].append(np.nan)
                try:
                    dict[x + "2nd_serve_won%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[5].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "2nd_serve_won%"].append(np.nan)
                try:
                    dict[x + "break_pts_saved%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[6].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "break_pts_saved%"].append(np.nan)
                try:
                    dict[x + "svc_pts_won%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[7].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "svc_pts_won%"].append(np.nan)
                try:
                    dict[x + "1st_serve_rtn_won%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[9].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "1st_serve_rtn_won%"].append(np.nan)
                try:
                    dict[x + "2nd_serve_rtn_won%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[10].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "2nd_serve_rtn_won%"].append(np.nan)
                try:
                    dict[x + "break_pts_won%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[11].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "break_pts_won%"].append(np.nan)
                try:
                    dict[x + "rtn_pts_won%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[12].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "rtn_pts_won%"].append(np.nan)
                try:
                    dict[x + "pts_dominance"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[14].find(class_="text-left").text)
                except:
                    dict[x + "pts_dominance"].append(np.nan)
                try:
                    dict[x + "total_pts_won%"].append(popup.find(id="matchStats-" + game + "Overview").find_all("tr")[15].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "total_pts_won%"].append(np.nan)
                try:
                    dict[x + "aces"].append(popup.find(id="matchStats-" + game + "AcesDFs").find_all("tr")[1].find(class_="text-left").text)
                except:
                    dict[x + "aces"].append(np.nan)
                try:
                    dict[x + "aces_per_svc_game"].append(popup.find(id="matchStats-" + game + "AcesDFs").find_all("tr")[3].find(class_="text-left pct-data").text)
                except:
                    dict[x + "aces_per_svc_game"].append(np.nan)
                try:
                    dict[x + "aces_per_set"].append(popup.find(id="matchStats-" + game + "AcesDFs").find_all("tr")[4].find(class_="text-left pct-data").text)
                except:
                    dict[x + "aces_per_set"].append(np.nan)
                try:
                    dict[x + "dfs"].append(popup.find(id="matchStats-" + game + "AcesDFs").find_all("tr")[6].find(class_="text-left").text)
                except:
                    dict[x + "dfs"].append(np.nan)
                try:
                    dict[x + "dfs_per_2nd_serve%"].append(popup.find(id="matchStats-" + game + "AcesDFs").find_all("tr")[8].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "dfs_per_2nd_serve%"].append(np.nan)
                try:
                    dict[x + "dfs_per_svc_game"].append(popup.find(id="matchStats-" + game + "AcesDFs").find_all("tr")[9].find(class_="text-left pct-data").text)
                except:
                    dict[x + "dfs_per_svc_game"].append(np.nan)
                try:
                    dict[x + "dfs_per_set"].append(popup.find(id="matchStats-" + game + "AcesDFs").find_all("tr")[10].find(class_="text-left pct-data").text)
                except:
                    dict[x + "dfs_per_set"].append(np.nan)
                try:
                    dict[x + "aces_to_dfs_ratio"].append(popup.find(id="matchStats-" + game + "AcesDFs").find_all("tr")[12].find(class_="text-left pct-data").text)
                except:
                    dict[x + "aces_to_dfs_ratio"].append(np.nan)
                try:
                    dict[x + "1st_serve_effectiveness"].append(popup.find(id="matchStats-" + game + "Serve").find_all("tr")[4].find(class_="text-left").text)
                except:
                    dict[x + "1st_serve_effectiveness"].append(np.nan)
                try:
                    dict[x + "serve_rating"].append(popup.find(id="matchStats-" + game + "Serve").find_all("tr")[5].find(class_="text-left").text)
                except:
                    dict[x + "serve_rating"].append(np.nan)
                try:
                    dict[x + "svc_in_play_pts_won%"].append(popup.find(id="matchStats-" + game + "Serve").find_all("tr")[8].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "svc_in_play_pts_won%"].append(np.nan)
                try:
                    dict[x + "pts_per_svc_game"].append(popup.find(id="matchStats-" + game + "Serve").find_all("tr")[9].find(class_="text-left pct-data").text)
                except:
                    dict[x + "pts_per_svc_game"].append(np.nan)
                try:
                    dict[x + "pts_lost_per_svc_game"].append(popup.find(id="matchStats-" + game + "Serve").find_all("tr")[10].find(class_="text-left pct-data").text)
                except:
                    dict[x + "pts_lost_per_svc_game"].append(np.nan)
                try:
                    dict[x + "bps_per_svc_game"].append(popup.find(id="matchStats-" + game + "Serve").find_all("tr")[12].find(class_="text-left pct-data").text)
                except:
                    dict[x + "bps_per_svc_game"].append(np.nan)
                try:
                    dict[x + "svc_bps_per_set"].append(popup.find(id="matchStats-" + game + "Serve").find_all("tr")[13].find(class_="text-left pct-data").text)
                except:
                    dict[x + "svc_bps_per_set"].append(np.nan)
                try:
                    dict[x + "svc_games_won%"].append(popup.find(id="matchStats-" + game + "Serve").find_all("tr")[15].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "svc_games_won%"].append(np.nan)
                try:
                    dict[x + "svc_games_lost_per_set"].append(popup.find(id="matchStats-" + game + "Serve").find_all("tr")[16].find(class_="text-left pct-data").text)
                except:
                    dict[x + "svc_games_lost_per_set"].append(np.nan)
                try:
                    dict[x + "rtn_rating"].append(popup.find(id="matchStats-" + game + "Return").find_all("tr")[3].find(class_="text-left").text)
                except:
                    dict[x + "rtn_rating"].append(np.nan)
                try:
                    dict[x + "rtn_in_play_pts_won%"].append(popup.find(id="matchStats-" + game + "Return").find_all("tr")[6].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "rtn_in_play_pts_won%"].append(np.nan)
                try:
                    dict[x + "pts_per_rtn_game"].append(popup.find(id="matchStats-" + game + "Return").find_all("tr")[7].find(class_="text-left pct-data").text)
                except:
                    dict[x + "pts_per_rtn_game"].append(np.nan)
                try:
                    dict[x + "pts_won_per_rtn_game"].append(popup.find(id="matchStats-" + game + "Return").find_all("tr")[8].find(class_="text-left pct-data").text)
                except:
                    dict[x + "pts_won_per_rtn_game"].append(np.nan)
                try:
                    dict[x + "bps_per_rtn_game"].append(popup.find(id="matchStats-" + game + "Return").find_all("tr")[10].find(class_="text-left pct-data").text)
                except:
                    dict[x + "bps_per_rtn_game"].append(np.nan)
                try:
                    dict[x + "rtn_bps_per_set"].append(popup.find(id="matchStats-" + game + "Return").find_all("tr")[11].find(class_="text-left pct-data").text)
                except:
                    dict[x + "rtn_bps_per_set"].append(np.nan)
                try:
                    dict[x + "winner%"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[1].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "winner%"].append(np.nan)
                try:
                    dict[x + "unforced_error%"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[2].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "unforced_error%"].append(np.nan)
                try:
                    dict[x + "forced_error%"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[3].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "forced_error%"].append(np.nan)
                try:
                    dict[x + "winners_to_UE_ratio"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[4].find(class_="text-left pct-data").text)
                except:
                    dict[x + "winners_to_UE_ratio"].append(np.nan)
                try:
                    dict[x + "winners_to_FE_against_ratio"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[5].find(class_="text-left pct-data").text)
                except:
                    dict[x + "winners_to_FE_against_ratio"].append(np.nan)
                try:
                    dict[x + "net_pts%"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[7].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "net_pts%"].append(np.nan)
                try:
                    dict[x + "net_pts_won%"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[8].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "net_pts_won%"].append(np.nan)
                try:
                    dict[x + "pts_won_at_net%"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[9].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "pts_won_at_net%"].append(np.nan)
                try:
                    dict[x + "max_serve_speed"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[11].find(class_="text-left").text.split(" km/h")[0])
                except:
                    dict[x + "max_serve_speed"].append(np.nan)
                try:
                    dict[x + "1st_serve_avg_speed"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[12].find(class_="text-left").text.split(" km/h")[0])
                except:
                    dict[x + "1st_serve_avg_speed"].append(np.nan)
                try:
                    dict[x + "2nd_serve_avg_speed"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[13].find(class_="text-left").text.split(" km/h")[0])
                except:
                    dict[x + "2nd_serve_avg_speed"].append(np.nan)
                try:
                    dict[x + "avg_serve_speed"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[14].find(class_="text-left").text.split(" km/h")[0])
                except:
                    dict[x + "avg_serve_speed"].append(np.nan)
                try:
                    dict[x + "1st_to_2nd_serve_speed_ratio"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[15].find(class_="text-left pct-data").text)
                except:
                    dict[x + "1st_to_2nd_serve_speed_ratio"].append(np.nan)
                try:
                    dict[x + "max_to_avg_speed_ratio"].append(popup.find(id="matchStats-" + game + "Other").find_all("tr")[16].find(class_="text-left pct-data").text)
                except:
                    dict[x + "max_to_avg_speed_ratio"].append(np.nan)
                try:
                    dict[x + "total_pts_played"].append(popup.find(id="matchStats-" + game + "Total").find_all("tr")[1].find(class_="text-left").text)
                except:
                    dict[x + "total_pts_played"].append(np.nan)
                try:
                    dict[x + "total_pts_won"].append(popup.find(id="matchStats-" + game + "Total").find_all("tr")[2].find(class_="text-left").text)
                except:
                    dict[x + "total_pts_won"].append(np.nan)
                try:
                    dict[x + "rtn_to_svc_pts_ratio"].append(popup.find(id="matchStats-" + game + "Total").find_all("tr")[4].find(class_="text-left pct-data").text)
                except:
                    dict[x + "rtn_to_svc_pts_ratio"].append(np.nan)
                try:
                    dict[x + "total_games_won"].append(popup.find(id="matchStats-" + game + "Total").find_all("tr")[6].find(class_="text-left").text)
                except:
                    dict[x + "total_games_won"].append(np.nan)
                try:
                    dict[x + "games_won%"].append(popup.find(id="matchStats-" + game + "Total").find_all("tr")[7].find(class_="text-left pct-data").text.split("%")[0])
                except:
                    dict[x + "games_won%"].append(np.nan)
                try:
                    dict[x + "games_dominance"].append(popup.find(id="matchStats-" + game + "Total").find_all("tr")[10].find(class_="text-left").text)
                except:
                    dict[x + "games_dominance"].append(np.nan)
                try:
                    dict[x + "break_pts_ratio"].append(popup.find(id="matchStats-" + game + "Total").find_all("tr")[11].find(class_="text-left").text)
                except:
                    dict[x + "break_pts_ratio"].append(np.nan)
        browser.find_element_by_xpath("//*[@id='matchStatsPopover-" + game + "']/div[3]/div[2]/button").click()
        if (count % 2500 == 5):
            dfFinal = pd.DataFrame.from_dict(dict)
            dfFinal = dfFinal.drop_duplicates()
            dfFinal.to_csv("./uts_stats.csv", index = False)
dfFinal = pd.DataFrame.from_dict(dict)
dfFinal = dfFinal.drop_duplicates()
dfFinal.to_csv("./uts_stats.csv", index = False)
browser.close()
