from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import random
from pynput.keyboard import Key, Listener


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
        sleep(1)

        password = self.driver.find_element_by_xpath('//*[@id="pword"]')
        password.send_keys(userpass)
        sleep(1)

        sign_in = self.driver.find_element_by_xpath(
            '//*[@id="signinform"]/div[3]/div/span/input')
        sign_in.click()

    def player1(self, wageBet):
        try:
            p1_button = self.driver.find_element_by_xpath('//*[@id="player1"]')
            print("Bet Team Red: " + self.p1_name +
                  '(' + self.p1 + ') $' + str(wageBet))
            p1_button.click()
            sleep(60)
        except:
            print('Failed to bet: P1')
            self.bet = None

    def player2(self, wageBet):
        try:
            p2_button = self.driver.find_element_by_xpath('//*[@id="player2"]')
            print("Bet Team Blue: " + self.p2_name +
                  '(' + self.p2 + ') $' + str(wageBet))
            p2_button.click()
            sleep(60)
        except:
            print("Failed to bet: P2")
            self.bet = None

    def modeCheck(self):
        try:
            footer = self.driver.find_element_by_xpath(
                '//*[@id="footer-alert"]').text
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
            else:
                self.exhib = False
                self.tourney = False
        except:
            self.exhib = False
            self.tourney = False
        return footer

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

    def autobet(self):
        self.loop = True
        wager = self.driver.find_element_by_xpath('//*[@id="wager"]')
        balance = self.driver.find_element_by_xpath('//*[@id="balance"]')
        betStatus = self.driver.find_element_by_xpath('//*[@id="status"]')
        # i = 0
        prevBal = 0

        if (self.modeText == ''):
            self.modeText = self.modeCheck()

        print('Balance: ' + balance.text)

        # main while loop of whole bot
        while self.loop == True:

            # pulls betting info from under video to make all decisions on when to bet/update bets
            betSlice = betStatus.text[len(
                betStatus.text)-7:len(betStatus.text)-3]

            # if modeText is cleared, check for new modeText
            if (self.modeText == ''):
                self.modeText = self.modeCheck()

            # when fight is over and decision is made, run checks and update information as needed
            if(betSlice == ' Red' or betSlice == 'Blue'):
                # provide log info of fight that just ended
                print('Result: ' + self.p1_name + '(' + str(self.p1) + ') vs ' + self.p2_name + '(' + str(self.p2) + ')' +
                      ' | Tournament: ' + str(self.tourney == True) + ' | Mode Text: ' + str(self.modeText), flush=True)

                # bet correctly and end of tournament or exhibition
                if(betSlice == self.bet and (self.tourneyFlag or self.exhibFlag)):
                    # inform log of which mode is ending, update flag accordingly and add result to string
                    if (self.tourneyFlag):
                        result = 'Last tourney bet correctly'
                        self.tourneyFlag = False
                    elif (self.exhibFlag):
                        result = 'Last exhibition bet correctly'
                        self.exhibFlag = False
                    try:
                        if(self.bet == ' Red'):
                            result += ' | ' + self.p1_name + ' won'
                        elif(self.bet == 'Blue'):
                            result += ' | ' + self.p2_name + ' won'
                    except:
                        result += ' | Updating fighters failed'
                    # resets betting amount and bet status
                    self.wage = 100
                    self.bet = None

                # bet incorrectly and end of tournament or exhibition
                elif(betSlice != self.bet and (self.tourneyFlag or self.exhibFlag)):
                    # inform log of which mode is ending, update flag accordingly and add result to string
                    if (self.tourneyFlag):
                        result = 'Last tourney bet incorrectly'
                        self.tourneyFlag = False
                    elif (self.exhibFlag):
                        result = 'Last exhibition bet incorrectly'
                        self.exhibFlag = False
                    try:
                        if(self.bet == ' Red'):
                            result += ' | ' + self.p2_name + ' won'
                        elif(self.bet == 'Blue'):
                            result += ' | ' + self.p1_name + ' won'
                    except:
                        result += ' | Updating fighters failed'
                    # resets betting amount and bet status
                    self.wage = 100
                    self.bet = None

                # bet correctly and not in tourney or exhibition
                elif(betSlice == self.bet and (self.tourney == False or self.exhib == False)):
                    # add bet result to string and update future bet, alter database to reflect result
                    result = 'Bet correctly'
                    self.wage = 100
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
                        # print('Updating fighters failed', flush=True)
                        result += ' | Updating fighters failed'
                    # reset betting status to no bet
                    self.bet = None

                # bet correctly and in tournament or exhibition
                elif(betSlice == self.bet and (self.tourney == True or self.exhib == True)):
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
                        result += ' | Updating fighters failed'
                    # reset wage for next fight and update betting status
                    self.wage = 100
                    self.bet = None

                # bet incorrectly and in tournament or exhibition
                elif(betSlice != self.bet and (self.tourney == True or self.exhib == True)):
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
                        result += ' | Updating fighters failed'
                    # reset wage for next fight and update betting status
                    self.wage = 100
                    self.bet = None

                # no bet info, generally because script just loaded but sometimes just missing bet info
                elif(self.bet == None):
                    # resets wage and bet status, updates info for log
                    result = 'No bet info'
                    self.wage = 100
                    self.bet = None

                # catch all that catches way too much currently, attempting to fix
                else:
                    # apparently assumption is I bet incorrectly
                    result = 'Bet incorrectly'
                    sleep(1)
                    # compares current balance versus stored previous balance, in case there's a discrepancy can know mostly
                    curBal = int(balance.text.replace(',', ''))
                    # not really sure why I'm checking for this
                    if prevBal > 0 and curBal > 0:
                        # if balances and wagers make sense or I'm all inning
                        if prevBal - self.wage == curBal or prevBal == curBal:
                            # reset wage to 100 for next fight
                            self.wage = 100
                            # if not in tournament
                            if(self.tourney == False):
                                # update for incorrect bet
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
                        # balances don't make sense somewhere
                        else:
                            # if I'm in the mines
                            if curBal <= 1000:
                                # all in every bet
                                self.wage = curBal
                            else:
                                # catch all statements mostly
                                if(self.tourney == True or self.exhib == True):
                                    # print('Tourney bet')
                                    result += " | Shouldn't appear anymore, old tourney/exhib bet result??"
                                else:
                                    # print('Missed a bet somewhere probably')
                                    result += ' | Missed a bet somewhere probably catchall'
                    # resets bet again probably for some reason??
                    self.bet = None
                # print results and move on
                print(result, flush=True)
                sleep(5)

            # if I'm in tourney or exhib and there's no bet made yet
            if((self.tourney == True or self.exhib == True) and self.bet == None):
                # reset fighter ids to 0 because I don't want to track them in database
                if(self.p1 != '0' or self.p2 != '0'):
                    self.p1 = '0'
                    self.p2 = '0'
                try:
                    # when bets are open, pull fighter info and add to log
                    if(betSlice == 'OPEN'):
                        info = ''
                        try:
                            self.p1_name = self.driver.find_element_by_xpath(
                                '//*[@id="player1"]').get_attribute("value")
                            self.p2_name = self.driver.find_element_by_xpath(
                                '//*[@id="player2"]').get_attribute("value")
                            info += self.p1_name + ' vs ' + self.p2_name
                        except:
                            info += 'Couldn\'t find fighter names'
                        # pull balance info and random number
                        b = balance.text.replace(',', '')
                        roulette = round(random.random())
                        sleep(5)
                        # if it's tourney, all in and bet on whichever based on coin flip
                        if (self.tourney):
                            wager.send_keys(b)
                            info += ' | Tourney Balance: ' + balance.text
                            print(info, flush=True)
                            if(roulette == 0):
                                self.bet = ' Red'
                                self.player1(b)
                            elif(roulette == 1):
                                self.bet = 'Blue'
                                self.player2(b)
                        # if it's exhibition send 100$ wager and bet on whichever based on coin flip
                        elif (self.exhib):
                            wager.send_keys(self.wage)
                            info += ' | (Exhib) Balance: ' + balance.text
                            print(info, flush=True)
                            if(roulette == 0):
                                self.bet = ' Red'
                                self.player1(self.wage)
                            elif(roulette == 1):
                                self.bet = 'Blue'
                                self.player2(self.wage)
                        # after bets are made reset modeText to blank to be updated during fight
                        self.modeText = ''
                    else:
                        sleep(1)
                except:
                    print('Tourney bet failed')

            # no open bet and not in tournament or exhibition
            elif(self.bet == None):
                if(betSlice == 'OPEN'):
                    info = ''
                    # pull fighter names and ids and store into variables
                    try:
                        self.p1_name = self.driver.find_element_by_xpath(
                            '//*[@id="player1"]').get_attribute("value")
                        self.p2_name = self.driver.find_element_by_xpath(
                            '//*[@id="player2"]').get_attribute("value")
                        self.p1 = db.queryId(self.p1_name)
                        self.p2 = db.queryId(self.p2_name)
                        # if queryId returns 0, means no fighter with name, so add fighter to database with basic values and update string
                        if (self.p1 == '0' or self.p2 == '0'):
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
                        # found both fighters, update string with names and ids
                        else:
                            info += self.p1_name + \
                                '(' + self.p1 + ') vs ' + \
                                self.p2_name + '(' + self.p2 + ')'
                        # perform winrate calculation based on database if possible, update string and perform bet calculation based on result
                        winRate = db.calcWinRate(self.p1, self.p2) * 100
                        info += ' | Winrate: ' + str(winRate) + '%'
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
                        print(
                            "Something inside of pulling fighter names and adding to db failed", flush=True)
                    try:
                        # send bet text to box and store balance for calculations in results, send string to log
                        wager.send_keys(self.wage)
                        sleep(5)
                        info += ' | Balance: ' + balance.text
                        prevBal = int(balance.text.replace(',', ''))
                        info += ' | Tournament: ' + str(self.tourney == True)
                        print(info, flush=True)
                    except:
                        print('Sending keys to wager failed', flush=True)
                    try:
                        # if no winrate to make judgement, coin flip, else choose favorite
                        if(winRate == 0):
                            roulette = round(random.random())
                            if(roulette == 0):
                                self.bet = ' Red'
                                self.player1(self.wage)
                            elif(roulette == 1):
                                self.bet = 'Blue'
                                self.player2(self.wage)
                        elif(winRate > 0):
                            self.bet = ' Red'
                            self.player1(self.wage)
                        elif(winRate < 0):
                            self.bet = 'Blue'
                            self.player2(self.wage)
                    except:
                        # catch for some error that shouldn't really appear, but just in case
                        print('Failed winrate wager', flush=True)
                        roulette = round(random.random())
                        if(roulette == 0):
                            self.bet = ' Red'
                            self.player1(self.wage)
                        elif(roulette == 1):
                            self.bet = 'Blue'
                            self.player2(self.wage)
                    # reset modeText on bet to allow it to be updated for future result
                    self.modeText = ''
                else:
                    sleep(2)
            else:
                sleep(2)


bet = SaltyBetter()
bet.login()
sleep(2)

# bet.listenStart()
bet.autobet()
