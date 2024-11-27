

# todo: move to SQLite
class Player:
    def __init__(self):
        self.db = TinyDB('./db.json')
        self.playerTable = self.db.table('player')
        self.username = None
        self.loggedIn = False

    def createPlayer(self):  # todo: post
        while True:
            username = input('Please enter your username: ')
            existingUserCheck = self.playerTable.search(Query().user == username)
            if existingUserCheck:
                print('That user already exists! Please try another username or log in if that\'s your username.')
                continue
            elif username:
                self.username = username
                password = input('Please enter your password: ')
                if password:
                    self.playerTable.insert(
                        {'user': username, 'password': password, 'currentLevel': 1, 'xpToNextLevel': 1000,
                         'currentXP': 0, 'highestScore': 0, 'gamesWon': 0, 'gamesPlayed': 0, 'winRate': 0})
                    self.loggedIn = True
                    self.loadPlayerData()
                    print('Thanks for joining! You are now logged in.')
                    break
                else:
                    print('Please input a password!')
            else:
                print('Please input a username!')

    def logPlayerIn(self):  # todo: post?
        if not self.playerTable:
            self.createPlayer()
        else:
            while True:
                username = input('Please enter your username: ')
                if not self.playerTable.search(Query().user == username):
                    print('That username doesn\'t exist. Please try again.')
                    continue
                password = input('Please enter your password: ')
                if password == self.playerTable.search(Query().user == username)[0]['password']:
                    self.username = username
                    self.loggedIn = True
                    self.loadPlayerData()
                    print('You have successfully logged in.')
                    break
                else:
                    print('Incorrect password. Please try again.')
                    continue

    def loadPlayerData(self):  # todo: get
        try:
            record = self.playerTable.get(Query().user == self.username)
        except Exception:
            logging.error('Error encountered getting player info.', exc_info=True)
            raise

        for key in ['highestScore', 'currentLevel', 'currentXP',
                    'xpToNextLevel', 'gamesWon', 'gamesPlayed', 'winRate']:
            setattr(self, key, record[key])

    def updatePlayerData(self):  # TODO: PUT
        record = {'highestScore': self.highestScore, 'currentLevel': self.currentLevel, 'currentXP': self.currentXP,
                  'xpToNextLevel': self.xpToNextLevel, 'gamesWon': self.gamesWon, 'gamesPlayed': self.gamesPlayed,
                  'gamesPlayed': self.gamesPlayed, 'winRate': self.winRate}
        self.playerTable.upsert(record, Query().user == self.username)

