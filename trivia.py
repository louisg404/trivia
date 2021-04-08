#!/usr/bin/env python3

class Game:
    def __init__(self):
        self.players = []
        self.places = [0] * 100
        self.purses = [0] * 6
        self.in_penalty_box = [0] * 100
        self.techno = False
        self.goldNeeded = 0
        self.joker = []
        self.isJokerInUse = False

        self.pop_questions = []
        self.science_questions = []
        self.sports_questions = []
        self.rock_questions = []
        self.techno_questions = []

        self.current_player = 0
        self.is_getting_out_of_penalty_box = False

        for i in range(50):
            self.pop_questions.append("Pop Question %s" % i)
            self.science_questions.append("Science Question %s" % i)
            self.sports_questions.append("Sports Question %s" % i)
            self.rock_questions.append("Rock Question %s" % i)
            self.techno_questions.append("Techno Question %s" % i)

    def is_playable(self):
        return self.how_many_players >= 2 and self.how_many_players <= 6

    def add(self, player_name):
        self.players.append(player_name)
        self.joker.append(True)
        self.places[self.how_many_players] = 0
        self.purses[self.how_many_players] = 0
        self.in_penalty_box[self.how_many_players] = False

        print(player_name + " was added")

        return True

    @property
    def how_many_players(self):
        return len(self.players)

    def roll(self, roll):
        print("%s is the current player" % self.players[self.current_player])

        stopGame = input("Do you want to stop ? (yes/no)")
        if stopGame == 'yes':
            self.players.pop(self.current_player)
            play()
        else:
            print("They have rolled a %s" % roll)
            if self.in_penalty_box[self.current_player]:
                if roll % 2 != 0:
                    self.is_getting_out_of_penalty_box = True

                    print("%s is getting out of the penalty box" % self.players[self.current_player])
                    self.places[self.current_player] = self.places[self.current_player] + roll
                    if self.places[self.current_player] > 11:
                        self.places[self.current_player] = self.places[self.current_player] - 12
                    self._question_process()
                   
                else:
                    print("%s is not getting out of the penalty box" % self.players[self.current_player])
                    self.is_getting_out_of_penalty_box = False
            else:
                self.places[self.current_player] = self.places[self.current_player] + roll
                if self.places[self.current_player] > 11:
                    self.places[self.current_player] = self.places[self.current_player] - 12
                self._question_process()
        

    def _question_process(self):
        print(self.players[self.current_player] + \
            '\'s new location is ' + \
            str(self.places[self.current_player]))
        print("The category is %s" % self._current_category)
        self._ask_question()
        if self.joker[self.current_player] :
            useJoker = input("Do you want to use your joker ? (yes/no)")
            if(useJoker == 'yes') : 
                self.joker[self.current_player] = False
                self.isJokerInUse = True
                print("you have used your joker")



    def _ask_question(self):
        if self._current_category == 'Pop': print(self.pop_questions.pop(0))
        if self._current_category == 'Science': print(self.science_questions.pop(0))
        if self._current_category == 'Sports': print(self.sports_questions.pop(0))
        if self._current_category == 'Rock': print(self.rock_questions.pop(0))
        if self._current_category == 'Techno': print(self.techno_questions.pop(0))

    @property
    def _current_category(self):
        if self.places[self.current_player] == 0: return 'Pop'
        if self.places[self.current_player] == 4: return 'Pop'
        if self.places[self.current_player] == 8: return 'Pop'
        if self.places[self.current_player] == 1: return 'Science'
        if self.places[self.current_player] == 5: return 'Science'
        if self.places[self.current_player] == 9: return 'Science'
        if self.places[self.current_player] == 2: return 'Sports'
        if self.places[self.current_player] == 6: return 'Sports'
        if self.places[self.current_player] == 10: return 'Sports'
        else:
            if self.techno:
                return 'Techno'
            else:
                return 'Rock'

    def was_correctly_answered(self):
        if self.in_penalty_box[self.current_player]:
            if self.is_getting_out_of_penalty_box:
                print('Answer was correct!!!!')
                self.purses[self.current_player] += 1
                print(self.players[self.current_player] + \
                    ' now has ' + \
                    str(self.purses[self.current_player]) + \
                    ' Gold Coins.')

                winner = self._did_player_win()
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0

                return winner
            else:
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0
                return True
        else:
            print("Answer was correct!!!!")
            self.purses[self.current_player] += 1
            print(self.players[self.current_player] + \
                ' now has ' + \
                str(self.purses[self.current_player]) + \
                ' Gold Coins.')

            winner = self._did_player_win()
            self.current_player += 1
            if self.current_player == len(self.players): self.current_player = 0

            return winner

    def joker_used(self):
        self.isJokerInUse = False
        self.current_player += 1
        if self.current_player == len(self.players): self.current_player = 0
        return True         


    def wrong_answer(self):
        print('Question was incorrectly answered')
        print(self.players[self.current_player] + " was sent to the penalty box")
        self.in_penalty_box[self.current_player] = True

        self.current_player += 1
        if self.current_player == len(self.players): self.current_player = 0
        return True

    def _did_player_win(self):
        return not (self.purses[self.current_player] == int(self.goldNeeded))

from random import randrange

if __name__ == '__main__':
    not_a_winner = False

    def play():
        while True:
            if game.how_many_players > 1:
                game.roll(randrange(5) + 1)
                if game.how_many_players > 1:
                    if game.isJokerInUse : 
                        not_a_winner = game.joker_used()   
                    elif randrange(9) == 7:
                        not_a_winner = game.wrong_answer()
                    else:
                        not_a_winner = game.was_correctly_answered()
                    if not not_a_winner: break
            else:
                break
                exit

    game = Game()
    game.add('Louis')
    game.add('Steeve')

    if game.is_playable():
        gold = False
        while (not gold):
            goldn = input("How much gold you want to win ? (6 minimum)")
            if(int(goldn) >= 6):
                gold = True
                game.goldNeeded = goldn
        
        techno = input("Do you want to play with Techno category instead of Rock category ? (yes/no)")
        if techno == 'yes':
            print("You will play with Techno category")
            game.techno = True
            play()
        else:
            print("You will play with Rock category")
            game.techno = False
            play()
    else:
        print('Too many/less players')
