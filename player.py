import  json

class Player:
    VERSION = "Default Python folding player"


    def get_cards_back(self,game_state):
        
        current_bet = 0
        useful_ranks = ['10','J','Q','K','A']
        team =  game_state['players'][game_state['in_action']]
        hole_cards_0 = team['hole_cards'][0]["rank"]
        hole_cards_1 = team['hole_cards'][1]["rank"]
        if hole_cards_0 == hole_cards_1 and hole_cards_0 in useful_ranks:
            current_bet = 10000
        else:
            current_bet = 0
        return  current_bet
        


    def betRequest(self, game_state):
        try:
            current_bet_in_betReq = 0
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

