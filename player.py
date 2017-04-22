

import numpy as np
import random
import sys
import math

import keras
from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.core import Flatten, Dense, Dropout, Activation
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import Nadam
from keras.preprocessing import image

MODEL = Sequential([
    ZeroPadding2D(padding=(2, 0), input_shape=(13, 4, 1)),
    Convolution2D(10,5,4, border_mode='valid', activation='relu'),
    Flatten(),
    Dense(20, activation='relu'),
    Dense(1),
    Activation('sigmoid')
])

opt = Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08, schedule_decay=0.006)
MODEL.compile(optimizer=opt,loss='binary_crossentropy', metrics=['accuracy'])
MODEL.load_weights('lean_poker_hand_quality_v1.h5')

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

    def get_rank(self, rank):
        return ['2','3','4','5','6','7','8','9','10','J','Q','K','A'].index(rank)

    def get_suit(self, suit):
        return ['diamonds','spades','hearts','clubs'].index(suit)

    def get_card_id(self, hand, i):
        return (self.get_rank(hand[2 * i]), self.get_suit(hand[2 * i + 1]))

    def get_cards(self, hand):
        cards = np.zeros((13, 4))
        for i in range(len(hand) - 1):
            cards[self.get_card_id(hand, i)] = 1
        return cards

    def get_cards_for_prediciton(self, game_state):
        community_cards = game_state['community_cards']

        active_player_idx = int(game_state['in_action'])
        hole_cards = game_state['players'][active_player_idx]['hole_cards']

        data = []

        for community_card in community_cards:
            data.append(community_card['rank'])
            data.append(community_card['suit'])

        for card in hole_cards:
            data.append(card['rank'])
            data.append(card['suit'])

        return self.get_cards(data)

    def betRequest(self, game_state):
        
            current_bet_in_betReq = 1
            comm_cards = game_state['community_cards']
            if not comm_cards:
                current_bet_in_betReq = self.chen_evaluator(game_state)
            else:
                cards = self.get_cards_for_prediciton(game_state)
                prediction = MODEL.predict([cards])
                print(cards)
                print('Prediction: %s' % prediction)
                if prediction[0] > 0.8:
                    team =  game_state['players'][game_state['in_action']]
                    current_bet_in_betReq = int(game_state['current_buy_in']) - int(team['bet']) + int(game_state['minimum_raise'])
                else:
                    current_bet_in_betReq = 0
            
            if current_bet_in_betReq < 0:
                current_bet_in_betReq = 2
            
            return current_bet_in_betReq
            

    def showdown(self, game_state):
        pass

