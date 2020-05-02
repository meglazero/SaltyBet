from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import random

class SaltyBetter():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(options=chrome_options)
        

    def login(self):
        self.driver.get('https://www.saltybet.com/authenticate?signin=1')

        sleep(2)

        options = open(r".\options.txt", "r")
        user = options.readline()
        userpass = options.readline()
        options.close()
        user = str(user[10:len(user)])
        userpass = str(userpass[10:len(userpass)])

        email = self.driver.find_element_by_xpath('//*[@id="email"]')
        email.send_keys(user)

        password = self.driver.find_element_by_xpath('//*[@id="pword"]')
        password.send_keys(userpass)

        sign_in = self.driver.find_element_by_xpath('//*[@id="signinform"]/div[3]/div/span/input')
        sign_in.click()

    def player1(self, wageBet):
        p1_button = self.driver.find_element_by_xpath('//*[@id="player1"]')
        print("Bet Team Red: " + str(wageBet))
        p1_button.click()
        sleep(60)

    def player2(self, wageBet):
        p2_button = self.driver.find_element_by_xpath('//*[@id="player2"]')
        p2_button.click()
        print("Bet Team Blue: " + str(wageBet))
        sleep(60)

    def autobet(self, wage):
        wager = self.driver.find_element_by_xpath('//*[@id="wager"]')
        balance = self.driver.find_element_by_xpath('//*[@id="balance"]')
        betStatus = self.driver.find_element_by_xpath('//*[@id="status"]')
        betOpen = len(betStatus.text)-7
        betClose = len(betStatus.text)-3
        bet = None
        i = 0
        try:
            tourney = self.driver.find_element_by_xpath('//*[@id="tournament-note"]')
        except:
            tourney = None

        print('Balance: ' + balance.text)

        while True:
            betSlice = betStatus.text[len(betStatus.text)-7:len(betStatus.text)-3]
            
            if(i > 60 or tourney == None):
                try:
                    tourney = self.driver.find_element_by_xpath('//*[@id="tournament-note"]')
                    i = 0
                except:
                    tourney = None
                    i = 0

            if(betSlice == ' Red' or betSlice == 'Blue'):
                if(betSlice == bet):
                    print('Bet correctly')
                elif(bet == None):
                    print('No bet info')
                else:
                    print('Bet incorrectly')
                sleep(5)
            if(tourney != None):
                try:
                    if(betSlice == 'OPEN'):
                        b = balance.text.replace(',', '')
                        wager.send_keys(b)
                        roulette = round(random.random())
                        sleep(1)
                        print('Balance: ' + balance.text)
                        if(roulette == 0):
                            bet = ' Red'
                            self.player1(b)
                        elif(roulette == 1):
                            bet = 'Blue'
                            self.player2(b)
                        i = 0
                    else:
                        sleep(1)
                        i+=1
                except:
                    print('Tourney bet failed')
            else:
                if(betSlice == 'OPEN'):
                    wager.send_keys(wage)
                    roulette = round(random.random())
                    sleep(1)
                    print('Balance: ' + balance.text)
                    if(roulette == 0):
                        bet = ' Red'
                        self.player1(wage)
                    elif(roulette == 1):
                        bet = 'Blue'
                        self.player2(wage)
                    i = 0
                else:
                    sleep(1)
                    i+=1

        

bet = SaltyBetter()
bet.login()
sleep(2)
bet.autobet(100)