
import random

class Player:
    VERSION = "Fuck pogacsa"


    def get_cards_back(self,game_state):
        if random.randint(0,10) > 7:
            return 150

        useful_ranks = ['8','9','10','J','Q','K','A']
        team =  game_state['players'][game_state['in_action']]
        hole_cards_rank_0 = team['hole_cards'][0]["rank"]
        hole_cards_rank_1 = team['hole_cards'][1]["rank"]

        hole_cards_suit_0 = team['hole_cards'][0]["suit"]
        hole_cards_suit_1 = team['hole_cards'][1]["suit"]

        active_players = 0
        for player in game_state['players']:
            if player['active'] != 'out':
                active_players += 1

        if active_players > 2:
            useful_ranks = ['J','Q','K','A']

        if hole_cards_rank_0 == hole_cards_rank_1 and hole_cards_rank_0 in useful_ranks:
            current_bet = 10000
        elif active_players == 2 and hole_cards_rank_0 in ['K','A'] and hole_cards_rank_1 in ['K','A'] and hole_cards_suit_0 == hole_cards_suit_1:
            current_bet = team['stack'] / 2
        else:
            current_bet = 0
        return  current_bet
        


    def betRequest(self, game_state):
        try:
            current_bet_in_betReq = self.get_cards_back(game_state)
            current_bet_in_betReq = int(current_bet_in_betReq)
            if current_bet_in_betReq < 0:
                current_bet_in_betReq = 0
            
            return current_bet_in_betReq
        except:
            current_bet_in_betReq = 0
            return current_bet_in_betReq
            

    def showdown(self, game_state):
        pass

