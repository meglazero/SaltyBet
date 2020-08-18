from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import random
from pynput.keyboard import Key, Listener
import db


class SaltyBetter():
    wage = 100
    loop = True
    bet = None
    p1 = 0
    p1_name = ''
    p2 = 0
    p2_name = ''
    tourney = False
    exhib = False
    modeText = ''
    tourneyFlag = False
    exhibFlag = False

    # listener = Listener()

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        try:
            self.driver.get('https://www.saltybet.com/authenticate?signin=1')

            sleep(2)

            options = open(r".\options.txt", "r")
            user = options.readline()
            userpass = options.readline()
            options.close()
            user = str(user[10:len(user)])
            userpass = str(userpass[10:len(userpass)])

            email = self.driver.find_element_by_xpath('//*[@id="email"]')
            print("Entering username", flush=True)
            email.send_keys(user)
            sleep(1)

            password = self.driver.find_element_by_xpath('//*[@id="pword"]')
            print("Entering password", flush=True)
            password.send_keys(userpass)
            sleep(1)

            sign_in = self.driver.find_element_by_xpath('//*[@id="signinform"]/div[3]/div/span/input')
            print("Signing in", flush=True)
            sign_in.click()
        except:
            print('Already logged in I guess? or log in failed maybe idfk')

    def player1(self, wageBet):
        try:
            p1_button = self.driver.find_element_by_xpath('//*[@id="player1"]')
            p1_button.click()
            if(self.p1 != '0'):
                return 'Bet Team Red: ' + self.p1_name + '(' + self.p1 + ') $' + str(wageBet) + ' | '
            else:
                return 'Bet Team Red: ' + self.p1_name + ' $' + str(wageBet) + ' | '
        except:
            print("Failed to bet", flush=True)
            self.bet = None

    def player2(self, wageBet):
        try:
            p2_button = self.driver.find_element_by_xpath('//*[@id="player2"]')
            p2_button.click()
            if(self.p1 != '0'):
                return 'Bet Team Blue: ' + self.p2_name + '(' + self.p2 + ') $' + str(wageBet) + ' | '
            else:
                return 'Bet Team Blue: ' + self.p2_name + ' $' + str(wageBet) + ' | '
        except:
            print("Failed to bet", flush=True)
            self.bet = None

    def modeCheck(self):
        try:
            footer = self.driver.find_element_by_xpath('//*[@id="footer-alert"]').text
            # self.tourney = self.driver.find_element_by_xpath('//*[@id="tournament-note"]')
            if (footer[2:len(footer)] == 'characters are left in the bracket!' or
                footer[3:len(footer)] == 'characters are left in the bracket!'):
                self.exhib = False
                self.tourney = True
            elif (footer == 'FINAL ROUND! Stay tuned for exhibitions after the tournament!'):
                self.tourney = False
                self.exhib = True
                self.tourneyFlag = True
            elif (footer[2:len(footer)] == 'exhibition matches left!' or
                  footer[3:len(footer)] == 'exhibition matches left!' or
                  footer == 'Exhibition mode start!'):
                self.tourney = False
                self.exhib = True
            elif (footer == 'Matchmaking mode will be activated after the next exhibition match!'):
                self.tourney = False
                self.exhib = False
                self.exhibFlag = True
            elif (footer[2:len(footer)] == 'more matches until the next tournament!' or
                  footer[3:len(footer)] == 'more matches until the next tournament!' or
                  footer[4:len(footer)] == 'more matches until the next tournament!'):
                self.exhib = False
                self.tourney = False
            elif (footer != ' ' or footer != ''):
                self.exhibFlag = False
                self.exhib = False
                self.tourneyFlag = False
                self.tourney = False
            else:
                self.exhib = False
                self.tourney = False
        except:
            self.exhib = False
            self.tourney = False
        return footer

    def fightResult(self, betSlice):
        result = ''

        # no bet info
        if (self.bet == None):
            result += 'No bet info'
        # bet correctly
        elif (betSlice == self.bet):
            # if last battle of tournament or exhibition
            if(self.tourneyFlag or self.exhibFlag):
                result += 'Result of ' + self.p1_name + \
                      ' vs ' + self.p2_name + ': '
                # inform log of which mode is ending, update flag accordingly and add result to string
                if (self.tourneyFlag):
                    result += 'Last tourney bet correctly'
                    self.tourneyFlag = False
                elif (self.exhibFlag):
                    result += 'Last exhibition bet correctly'
                    self.exhibFlag = False
                try:
                    if(self.bet == ' Red'):
                        result += ' | ' + self.p1_name + ' won'
                    elif(self.bet == 'Blue'):
                        result += ' | ' + self.p2_name + ' won'
                except:
                    result += ' | Reporting fighters failed'
            elif(self.tourney or self.exhib):
                result += 'Result of ' + self.p1_name + \
                      ' vs ' + self.p2_name + ': '
                # add bet result to string and result of fight
                if (self.tourney):
                    result = 'Tourney bet correctly'
                elif (self.exhib):
                    result = 'Exhibition bet correctly'
                try:
                    if(self.bet == ' Red'):
                        result += ' | ' + self.p1_name + ' won'
                    elif(self.bet == 'Blue'):
                        result += ' | ' + self.p2_name + ' won'
                except:
                    result += ' | Reporting fighters failed'
            else:
                result += 'Result of ' + self.p1_name + '(' + str(self.p1) + ') vs ' + \
                      self.p2_name + '(' + str(self.p2) + ')' + ': '
                # add bet result to string and update future bet, alter database to reflect result
                result += 'Bet correctly'
                try:
                    if(self.bet == ' Red'):
                        db.fighterWin(self.p1)
                        db.fighterLose(self.p2)
                        result += ' | ' + self.p1_name + \
                            '(' + self.p1 + ') won'
                    elif(self.bet == 'Blue'):
                        db.fighterWin(self.p2)
                        db.fighterLose(self.p1)
                        result += ' | ' + self.p2_name + \
                            '(' + self.p2 + ') won'
                except:
                    result += ' | Updating fighters failed'

        # bet incorrectly
        elif (betSlice != self.bet):
            if(self.tourneyFlag or self.exhibFlag):
                result += 'Result of ' + self.p1_name + \
                      ' vs ' + self.p2_name + ': '
                # inform log of which mode is ending, update flag accordingly and add result to string
                if (self.tourneyFlag):
                    result += 'Last tourney bet incorrectly'
                    self.tourneyFlag = False
                elif (self.exhibFlag):
                    result += 'Last exhibition bet incorrectly'
                    self.exhibFlag = False
                try:
                    if(self.bet == ' Red'):
                        result += ' | ' + self.p2_name + ' won'
                    elif(self.bet == 'Blue'):
                        result += ' | ' + self.p1_name + ' won'
                except:
                    result += ' | Reporting fighters failed'
            elif(self.tourney or self.exhib):
                result += 'Result of ' + self.p1_name + \
                      ' vs ' + self.p2_name + ': '
                # add bet result to string and result of fight
                if (self.tourney):
                    result = 'Tourney bet incorrectly'
                elif (self.exhib):
                    result = 'Exhibition bet incorrectly'
                try:
                    if(self.bet == ' Red'):
                        result += ' | ' + self.p2_name + ' won'
                    elif(self.bet == 'Blue'):
                        result += ' | ' + self.p1_name + ' won'
                except:
                    result += ' | Reporting fighters failed'
            else:
                result += 'Result of ' + self.p1_name + '(' + str(self.p1) + ') vs ' + \
                      self.p2_name + '(' + str(self.p2) + ')' + ': '
                # add bet result to string and update future bet, alter database to reflect result
                result += 'Bet incorrectly'
                try:
                    if(self.bet == ' Red'):
                        db.fighterWin(self.p2)
                        db.fighterLose(self.p1)
                        result += ' | ' + self.p2_name + \
                            '(' + self.p2 + ') won'
                    elif(self.bet == 'Blue'):
                        db.fighterWin(self.p1)
                        db.fighterLose(self.p2)
                        result += ' | ' + self.p1_name + \
                            '(' + self.p1 + ') won'
                except:
                    result += ' | Updating fighters failed'

        # catch for errors
        else:
            result += 'Did not bet correctly, incorrectly, or None somehow'

        if (self.modeText != ''):
            result += ' | Footer: ' + self.modeText
        else:
            result += ' | No footer saved '
        print(result, flush=True)
        self.bet = None
        self.wage = 100
        sleep(5)

    def rouletteSpin(self, wager):
        try:
            roulette = round(random.random())
            if(roulette == 0):
                self.bet = ' Red'
                return self.player1(wager)
            elif(roulette == 1):
                self.bet = 'Blue'
                return self.player2(wager)
        except:
            return 'Roulette failed'

    def betFight(self, balance, wager):
        if (self.modeText == ''):
                self.modeText = self.modeCheck()
                if (self.modeText == ''):
                    return
        info = ''
        try:
            self.p1_name = self.driver.find_element_by_xpath(
                '//*[@id="player1"]').get_attribute("value")
            self.p2_name = self.driver.find_element_by_xpath(
                '//*[@id="player2"]').get_attribute("value")
        except:
            info += 'Couldn\'t find fighter names'
        b = balance.text.replace(',', '')
        if(self.tourney or self.exhib):
            info += self.p1_name + ' vs ' + self.p2_name
            try:
                if(self.p1 != '0' or self.p2 != '0'):
                    self.p1 = '0'
                    self.p2 = '0'
                sleep(5)
                if(self.tourney):
                    if(int(b) > 25000):
                        if(wager.get_attribute("disabled") != "disabled"):
                            wager.send_keys(self.wage)
                            info = self.rouletteSpin(self.wage) + info
                            info += ' | Tourney Balance(>25k): $' + balance.text
                        else:
                            info += 'Wager not visible'
                    else:
                        if(wager.get_attribute("disabled") != "disabled"):
                            wager.send_keys(b)
                            self.wage = b
                            info = self.rouletteSpin(self.wage) + info
                            info += ' | Tourney Balance: $' + balance.text
                        else:
                            info += 'Wager not visible'
                elif(self.exhib):
                    if(wager.get_attribute("disabled") != "disabled"):
                        wager.send_keys(self.wage)
                        info = self.rouletteSpin(self.wage) + info
                        info += ' | Balance: $' + balance.text
                    else:
                        info += 'Wager not visible'
                else:
                    info += 'Catch all, shouldn\'t appear'
            except:
                info += 'Exception in tourney or exhib bet'
        elif(self.tourney == False and self.exhib == False):
            try:
                self.p1 = db.queryId(self.p1_name)
                self.p2 = db.queryId(self.p2_name)
                if(self.p1 == '0' or self.p2 == '0'):
                    if (self.p1 == '0' and self.p2 == '0'):
                        self.p1 = db.insertFighter(self.p1_name)
                        self.p2 = db.insertFighter(self.p2_name)
                        info += self.p1_name + \
                            '(' + self.p1 + ') vs ' + \
                            self.p2_name + '(' + self.p2 + ')'
                        info += ' | added to db: ' + self.p1_name + ' & ' + self.p2_name
                    elif (self.p1 == '0'):
                        self.p1 = db.insertFighter(self.p1_name)
                        info += self.p1_name + \
                            '(' + self.p1 + ') vs ' + \
                            self.p2_name + '(' + self.p2 + ')'
                        info += ' | added to db: ' + self.p1_name
                    elif (self.p2 == '0'):
                        self.p2 = db.insertFighter(self.p2_name)
                        info += self.p1_name + \
                            '(' + self.p1 + ') vs ' + \
                            self.p2_name + '(' + self.p2 + ')'
                        info += ' | added to db: ' + self.p2_name
                else:
                    info += self.p1_name + \
                        '(' + self.p1 + ') vs ' + \
                        self.p2_name + '(' + self.p2 + ')'

                winRate = db.calcWinRate(self.p1, self.p2) * 100
                info += ' | Winrate: ' + str(winRate) + '%'
                if(int(b) < 2000):
                    self.wage = int(b)
                else:
                    if(abs(winRate) >= 50):
                        self.wage = 500
                    elif(abs(winRate) >= 40):
                        self.wage = 400
                    elif(abs(winRate) >= 30):
                        self.wage = 300
                    elif(abs(winRate) >= 15):
                        self.wage = 200
                    elif(abs(winRate) >= 0):
                        self.wage = 100
            except:
                info += ' | Something in first half of bet failed'

            try:
                if(wager.get_attribute("disabled") != "disabled"):
                    wager.send_keys(self.wage)
                    if(winRate == 0):
                        info = self.rouletteSpin(self.wage) + info
                    elif(winRate > 0):
                        self.bet = ' Red'
                        info = self.player1(self.wage) + info
                    elif(winRate < 0):
                        self.bet = 'Blue'
                        info = self.player2(self.wage) + info
                else:
                    info += 'Wager not visible'
            except:
                info += 'Failed winrate wager'
                info = self.rouletteSpin(self.wage) + info
            info += ' | Balance: $' + balance.text
        self.modeText = ''
        print(info, flush=True)
        sleep(15)

    def autobet(self):
        self.loop = True
        wager = self.driver.find_element_by_xpath('//*[@id="wager"]')
        balance = self.driver.find_element_by_xpath('//*[@id="balance"]')
        betStatus = self.driver.find_element_by_xpath('//*[@id="status"]')
        # i = 0
        # prevBal = 0

        if(self.modeText == ''):
            self.modeText = self.modeCheck()

        print('Balance: ' + balance.text, flush=True)

        while self.loop == True:

            betSlice = betStatus.text[len(betStatus.text)-7:len(betStatus.text)-3]

            if (self.modeText == ''):
                self.modeText = self.modeCheck()

            if(betSlice == ' Red' or betSlice == 'Blue'):
                self.fightResult(betSlice)
            elif(self.bet == None and betSlice == 'OPEN'):
                self.betFight(balance, wager)
            else:
                sleep(2)

    # def wagerAdjust(self):
    #     y = None
    #     try:
    #         y = int(input('Enter your adjusted wager: '))
    #     except:
    #         print("Not a number")
    #         y = None
    #         self.wagerAdjust()
    #     self.listenStart()
    #     return y

    # def autoAdjust(self):
    #     self.listenStop()
    #     print('Adjust autobet (pick a number):')
    #     print('1: Adjust wage (current: {0})'.format(self.wage))
    #     print('2: Adjust mode')
    #     print('3: Quit autobet')
    #     print('4: Cancel adjustment')
    #     userinput = input('Enter a menu item: ')
    #     try:
    #         userinput = int(userinput)
    #     except ValueError:
    #         print("Not a number")
    #         self.autoAdjust()
    #     print(userinput)
    #     if(userinput == 1):
    #         self.wage = self.wagerAdjust()
    #         print("Updated wager is: {0}".format(self.wage))
    #     elif(userinput == 2):
    #         print("Doesn't work yet")
    #         self.listenStart()
    #     elif(userinput == 3):
    #         print("Quitting autobet")
    #         self.loop = False
    #     elif(userinput == 4):
    #         print("Exited menu")
    #         self.listenStart()
    #     else:
    #         print("Not a valid entry on the list")
    #         self.autoAdjust()

    # def on_press(self, key):
    #     if key == Key.f8:
    #         self.autoAdjust()

    # def on_release(self, key):
    #     if key == Key.esc:
    #         return False

    # def listenStart(self):
    #     self.listener = Listener(
    #         on_press = self.on_press,
    #         on_release = self.on_release)
    #     self.listener.start()

    # def listenStop(self):
    #     self.listener.stop()


bet = SaltyBetter()
bet.login()
sleep(2)

# bet.listenStart()
bet.autobet()
