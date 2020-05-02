from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import random
from pynput.keyboard import Key, Listener

class SaltyBetter():
    wage = 100

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

    def player2(self, wageBet):
        p2_button = self.driver.find_element_by_xpath('//*[@id="player2"]')
        p2_button.click()
        print("Bet Team Blue: " + str(wageBet))

    def wagerAdjust(self):
        x = None
        x = input('Enter your adjusted wager: ')
        if(isinstance(int(x), int) == False):
            print("Not a proper number")
            wagerAdjust()
        x = int(x)
        return x

    def autoAdjust(self):
        x = None
        print('Adjust autobet (pick a number):')
        print('1: Adjust wage')
        print('2: Adjust mode')
        print('3: Quit autobet')
        print('4: Cancel adjustment')
        x = input()
        try:
            x = int(x)
        except:
            print("Not a valid entry on the list")
            self.autoAdjust()
        if(x == 1):
            self.wage = self.wagerAdjust()
            print("Updated wager is: {0}".format(self.wage))
        elif(x == 2):
            print("Doesn't work yet")
        elif(x == 3):
            quit()
        elif(x == 4):
            return
        else:
            print("Not a valid entry on the list")
            self.autoAdjust()

    def on_press(self, key):
        pass
        # print('{0} pressed'.format(key))

    def on_release(self, key):
        # print('{0} release'.format(key))
        if key == Key.f8:
            self.autoAdjust()
        if key == Key.esc:
            return False

    def autobet(self):
        wager = self.driver.find_element_by_xpath('//*[@id="wager"]')
        balance = self.driver.find_element_by_xpath('//*[@id="balance"]')
        betStatus = self.driver.find_element_by_xpath('//*[@id="status"]')
        betOpen = len(betStatus.text)-7
        betClose = len(betStatus.text)-3
        bet = None
        i = 0

        listener = Listener(
            on_press = self.on_press,
            on_release = self.on_release)
        listener.start()

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
                    bet = None
                elif(bet == None):
                    print('No bet info')
                    bet = None
                else:
                    print('Bet incorrectly')
                    bet = None
                sleep(5)
            if(tourney != None and bet == None):
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
            elif(bet == None):
                if(betSlice == 'OPEN'):
                    wager.send_keys(self.wage)
                    roulette = round(random.random())
                    sleep(1)
                    print('Balance: ' + balance.text)
                    if(roulette == 0):
                        bet = ' Red'
                        self.player1(self.wage)
                    elif(roulette == 1):
                        bet = 'Blue'
                        self.player2(self.wage)
                    i = 0
                else:
                    sleep(1)
                    i+=1

bet = SaltyBetter()
bet.login()
sleep(2)
bet.autobet()