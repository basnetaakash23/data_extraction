from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import json
from flask import Flask, jsonify, request
from collections import OrderedDict
import threading

number_clubs = 20
class Epl():

    def __init__(self, browser):
        self._browser = browser
        self.dict_teams = OrderedDict()
        self.dict_topscorers = OrderedDict()
        self.top_assists = OrderedDict()
        self.top_passes = OrderedDict()
        self.hit_woodwork =OrderedDict()
        

    def extract_table(self):
        self._browser.get("https://www.premierleague.com/tables")
        self._browser.maximize_window()
        time.sleep(2)
        index = 1
        
        while(index < number_clubs*2): # times two due to the nature of table in premier league.com
            each_club = OrderedDict()
        
            team_pos = self._browser.find_element_by_xpath("/html/body/main/div[2]/div[1]/div[5]/div/div/div/table/tbody/tr["+str(index)+"]/td[2]/span[1]")
            #print(team_pos.text)
            team_pos = '0'+str(team_pos.text) if int(team_pos.text)<10 else str(team_pos.text)
            each_club["position"] = team_pos

            team_name = self._browser.find_element_by_xpath("/html/body/main/div[2]/div[1]/div[5]/div/div/div/table/tbody/tr["+str(index)+"]/td[3]/a/span[2]")
            #print(team_name.text)
            each_club["clubName"] = team_name.text

            matches_played = self._browser.find_element_by_xpath("/html/body/main/div[2]/div[1]/div[5]/div/div/div/table/tbody/tr["+str(index)+"]/td[4]")
            #print(matches_played.text)
            each_club["matchesPlayed"] = matches_played.text

            matches_won = self._browser.find_element_by_xpath("/html/body/main/div[2]/div[1]/div[5]/div/div/div/table/tbody/tr["+str(index)+"]/td[5]")
            #print(matches_won.text)
            each_club["matchesWon"] = matches_won.text

            matches_drawn = self._browser.find_element_by_xpath("/html/body/main/div[2]/div[1]/div[5]/div/div/div/table/tbody/tr["+str(index)+"]/td[6]")
            #print(matches_drawn.text)
            each_club["matchesDrawn"] = matches_drawn.text

            matches_lost = self._browser.find_element_by_xpath("/html/body/main/div[2]/div[1]/div[5]/div/div/div/table/tbody/tr["+str(index)+"]/td[7]")
            #print(matches_lost.text)
            each_club["matchesLost"] = matches_lost.text

            goal_scored = self._browser.find_element_by_xpath("/html/body/main/div[2]/div[1]/div[5]/div/div/div/table/tbody/tr["+str(index)+"]/td[8]")
            #print(goal_scored.text)
            each_club["goalsScored"] = goal_scored.text

            goal_against = self._browser.find_element_by_xpath("/html/body/main/div[2]/div[1]/div[5]/div/div/div/table/tbody/tr["+str(index)+"]/td[9]")
            #print(goal_against.text)
            each_club["goalAgainst"] = goal_against.text

            goal_diff = self._browser.find_element_by_xpath("/html/body/main/div[2]/div[1]/div[5]/div/div/div/table/tbody/tr["+str(index)+"]/td[10]")
            #print(goal_diff.text)
            each_club["goalDiff"] = goal_diff.text

            total_points = self._browser.find_element_by_xpath("/html/body/main/div[2]/div[1]/div[5]/div/div/div/table/tbody/tr["+str(index)+"]/td[11]")
            #print(total_points.text)
            each_club["totalPoints"] = total_points.text

            #creating the key as the club position
            self.dict_teams[team_pos] = each_club
            
            index += 2

    def extract_topscorers(self):
        self._browser.get("https://www.premierleague.com/stats/top/players/goals?se=363")
        time.sleep(2)
        self._browser.maximize_window()
        return self.extract_data(self.dict_topscorers)
            
    def extract_topassists(self):
        self._browser.get("https://www.premierleague.com/stats/top/players/goal_assist?se=363")
        time.sleep(2)
        self._browser.maximize_window()
        return self.extract_data(self.top_assists)
        

    def extract_passes(self):
        self._browser.get("https://www.premierleague.com/stats/top/players/total_pass")
        time.sleep(2)
        self._browser.maximize_window()
        return self.extract_data(self.top_passes)
        

    def extract_hitwoodwork(self):
        self._browser.get("https://www.premierleague.com/stats/top/players/hit_woodwork")
        time.sleep(2)
        self._browser.maximize_window()
        return self.extract_data(self.hit_woodwork)
        

    def extract_data(self, d):
        self._d = d

        index = 1
        while(index < 21):
            ind_passes = {}
            
            try:
                position = self._browser.find_element_by_xpath("/html/body/main/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr["+str(index)+"]/td[1]/strong").text
            #position = '0'+str(position.text) if int(position.text)<10 else str(position.text)
                ind_passes["position"] = position

            except:
                pass

            try:
                player = self._browser.find_element_by_xpath("/html/body/main/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr["+str(index)+"]/td[2]/a").text
                ind_passes["player"] = player

            except:
                pass

            try:
                club = self._browser.find_element_by_xpath("/html/body/main/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr["+str(index)+"]/td[3]/a").text
                ind_passes["club"] = club

            except:
                pass

            try:
                nationality = self._browser.find_element_by_xpath("/html/body/main/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr["+str(index)+"]/td[4]/div/span[2]").text
                ind_passes["nationality"] = nationality
            
            except:
                pass

            try:
                passes = self._browser.find_element_by_xpath("/html/body/main/div[2]/div/div[2]/div[1]/div[2]/table/tbody/tr["+str(index)+"]/td[5]").text
                ind_passes["stat"] = passes

            except:
                pass

            self._d['0'+str(index) if index<10 else str(index)] = ind_passes
            index += 1

        return self._d

    def write_json(self, object, name):
        with open(str(name)+'.json','w') as f:
            f.write(json.dumps(object))

    def run(self):
        t1 = threading.Thread(target = self.extract_table)
        t2 = threading.Thread(target = self.extract_topscorers)
        t3 = threading.Thread(target = self.extract_topassists)
        t4 = threading.Thread(target = self.extract_passes)
        t5 = threading.Thread(target =self.extract_hitwoodwork)
        t1.run()
        t2.run()
        t3.run()
        t4.run()
        t5.run()
        return self.dict_teams, self.dict_topscorers, self.top_assists, self.top_passes, self.hit_woodwork

app = Flask(__name__)

@app.route('/hit_woodwork', methods = ['GET', 'POST'])
def eplHitWoodwork():
    if(request.method == 'GET'):
        return jsonify(hit_woodwork)

@app.route('/top_passes', methods = ['GET', 'POST'])
def eplTopPasses():
    if(request.method == 'GET'):
        return jsonify(passes)

@app.route('/top_assists', methods = ['GET', 'POST'])
def eplTopAssists():
    if(request.method == 'GET'):
        return jsonify(assists)

@app.route('/top_scorers', methods = ['GET', 'POST'])
def eplTopScorer():
    if(request.method == 'GET'):
        return jsonify(scorersdoc)

@app.route('/epl_table', methods = ['GET', 'POST'])
def eplTable():
    if(request.method == 'GET'):
        return jsonify(teams)

@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
        return jsonify(scorers)


if __name__ == "__main__":
    chr_options = Options()
    chr_options.add_argument("--no-sandbox")
    chr_options.add_experimental_option("detach", True)
    # chr_options.headless = True
    # chr_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome("./linux/chromedriver",options = chr_options)
    epl = Epl(browser)
    teams, scorers, assists, passes , hit_woodwork = epl.run()
    #teams = epl.extract_table()

    print(teams)
    print("Scorers",scorers)
    print("assists", assists)
    epl.write_json(teams, "table")
    epl.write_json(scorers, "topscorer")
    epl.write_json(assists,"topassists")
    epl.write_json(passes,"mostpasses")
    epl.write_json(hit_woodwork,"hitwoodwork")

    browser.quit()

    #Opening a flask application
    
    app.run(debug = True)

    






