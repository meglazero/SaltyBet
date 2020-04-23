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

        email = self.driver.find_element_by_xpath('//*[@id="email"]')
        email.send_keys('meglazero.ex@gmail.com')

        password = self.driver.find_element_by_xpath('//*[@id="pword"]')
        password.send_keys('Godzilla1')

        sign_in = self.driver.find_element_by_xpath('//*[@id="signinform"]/div[3]/div/span/input')
        sign_in.click()

    def player1(self):
        p1_button = self.driver.find_element_by_xpath('//*[@id="player1"]')
        print("Bet Team Red")
        p1_button.click()
        sleep(60)

    def player2(self):
        p2_button = self.driver.find_element_by_xpath('//*[@id="player2"]')
        p2_button.click()
        print("Bet Team Blue")
        sleep(60)

    def autobet(self):
        wager = self.driver.find_element_by_xpath('//*[@id="wager"]')
        balance = self.driver.find_element_by_xpath('//*[@id="balance"]')
        betStatus = self.driver.find_element_by_xpath('//*[@id="status"]')
        betOpen = len(betStatus.text)-7
        betClose = len(betStatus.text)-3
        bet = None

        print('Balance: ' + balance.text)

        while True:
            betSlice = betStatus.text[len(betStatus.text)-7:len(betStatus.text)-3]
            if(betSlice == ' Red' or betSlice == 'Blue'):
                if(betSlice == bet):
                    print('Bet correctly')
                else:
                    print('Bet incorrectly')
                sleep(5)
            # if(betSlice == 'Blue'):
            #     print("Blue won")
            #     sleep(5)
            # if(wager.get_attribute("style") == "border-color: rgb(77, 176, 68); display: inline-block;"):
            if(betSlice == 'OPEN'):
                wager.send_keys(100)
                roulette = round(random.random())
                sleep(1)
                print('Balance: ' + balance.text)
                if(roulette == 0):
                    bet = ' Red'
                    self.player1()
                elif(roulette == 1):
                    bet = 'Blue'
                    self.player2()
            else:
                # print("couldn't bet")
                sleep(1)

        

bet = SaltyBetter()
bet.login()
sleep(2)
bet.autobet()