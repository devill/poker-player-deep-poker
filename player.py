

import random
import sys
import math

class Player:
    VERSION = "Fuck pogacsa 1.4"

    def chen_calculator(self,game_state):
        current_val = 0
        team =  game_state['players'][game_state['in_action']]
        suite_value = { 'A' : 10, 'K' : 8 , 'Q' : 7 , 'J' : 6 , '10': 5 , '9' : 4.5 , '8' : 4, '7' : 3.5, '6': 3 , '5' : 2.5 , '4' :2 , '3' :1.5 , '2' : 1 }
        suite_order = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        hole_cards_rank_0 = team['hole_cards'][0]["rank"]
        hole_cards_rank_1 = team['hole_cards'][1]["rank"]
        card_0_value = suite_value[hole_cards_rank_0]
        #print(card_0_value)
        card_1_value = suite_value[hole_cards_rank_1]
        #print(card_1_value)
        if card_0_value > card_1_value:
            #print('first is bigger')
            current_val += card_0_value
        elif card_0_value < card_1_value:
            #print('second is bigger')
            current_val += card_1_value
        else:
            current_val += card_0_value * 2
            if current_val < 5:
                current_val += 5
        #print("chen value is now" + str(current_val))
        hole_cards_suit_0 = team['hole_cards'][0]["suit"]
        hole_cards_suit_1 = team['hole_cards'][1]["suit"]
        if hole_cards_suit_0 == hole_cards_suit_1:
            current_val += 2
        
        card_gap = abs(suite_order.index(hole_cards_rank_0) -  suite_order.index(hole_cards_rank_1))-1
        #print(suite_order.index(hole_cards_rank_0))
        #print(card_gap)
        cards_lower_than_Q = False
        if suite_order.index(hole_cards_rank_0) < 10 and suite_order.index(hole_cards_rank_1) < 10:
            cards_lower_than_Q = True
        if card_gap  < 1:
            current_val += 0
            if cards_lower_than_Q == True:
                current_val += 1
        elif card_gap < 2 :
            current_val += -1
            if cards_lower_than_Q == True:
                current_val += 1
        elif card_gap < 3:
            current_val += -2
        elif card_gap < 4:
            current_val += -3
        elif card_gap > 4:
            current_val += -4
        print(card_gap)
        print("chen value is now" + str(current_val))
        current_val = math.ceil(current_val)
        return current_val
        
        
    def chen_evaluator(self,game_state):
        chen_val = self.chen_calculator(game_state)
        team =  game_state['players'][game_state['in_action']]
        
        to_call = game_state['current_buy_in'] - team['bet']
        to_raise = to_call + game_state['minimum_raise'] + 100
        
        if chen_val > 10:
            return to_raise
        if chen_val > 15:
            return to_raise + 50
        else:
            return 0
        
        
            
            
    def get_cards_back(self,game_state):
        # if random.randint(0,10) > 2:
        #     return 150

        useful_ranks = ['8','9','10','J','Q','K','A']
        team =  game_state['players'][game_state['in_action']]
        hole_cards_rank_0 = team['hole_cards'][0]["rank"]
        hole_cards_rank_1 = team['hole_cards'][1]["rank"]

        hole_cards_suit_0 = team['hole_cards'][0]["suit"]
        hole_cards_suit_1 = team['hole_cards'][1]["suit"]

        to_call = game_state['current_buy_in'] - team['bet']
        if hole_cards_rank_0 == hole_cards_rank_1 and hole_cards_rank_0 in useful_ranks:
            current_bet = 10000
        elif hole_cards_rank_0 in ['J','Q','K','A'] and hole_cards_rank_1 in ['J','Q','K','A'] and hole_cards_suit_0 == hole_cards_suit_1:
            current_bet = to_call
        elif team['bet'] > 0 and team['bet'] > to_call:
            current_bet = to_call
        else:
            current_bet = 0
        return  current_bet

    def get_number_of_active_players(self, game_state):
        active_players = 0
        for player in game_state['players']:
            if player['active'] != 'out':
                active_players += 1

        return active_players

    def betRequest(self, game_state):
        
            current_bet_in_betReq = 1
            comm_cards = game_state['community_cards']
            if not comm_cards:
                current_bet_in_betReq =  self.chen_evaluator(game_state)
            else:
                current_bet_in_betReq = self.get_cards_back(game_state)
                current_bet_in_betReq = int(current_bet_in_betReq)
            
            if current_bet_in_betReq < 0:
                current_bet_in_betReq = 2
            
            return current_bet_in_betReq
        
            
            current_bet_in_betReq = 3
            return current_bet_in_betReq
            

    def showdown(self, game_state):
        pass

