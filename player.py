
class Player:
    VERSION = "Default Python folding player"


    def get_cards_back(self,game_state):
        useful_ranks = ['8','9','10','J','Q','K','A']
        team =  game_state['players'][game_state['in_action']]
        hole_cards_rank_0 = team['hole_cards'][0]["rank"]
        hole_cards_rank_1 = team['hole_cards'][1]["rank"]

        hole_cards_suit_0 = team['hole_cards'][0]["suit"]
        hole_cards_suit_1 = team['hole_cards'][1]["suit"]
        if hole_cards_rank_0 == hole_cards_rank_1 and hole_cards_rank_0 in useful_ranks:
            current_bet = 10000
        elif hole_cards_rank_0 in ['Q','K','A'] and hole_cards_rank_1 in ['Q','K','A'] and hole_cards_suit_0 == hole_cards_suit_1:
            current_bet = team['stack'] / 2
        else:
            to_call = team['current_buy_in'] - team['bet']
            current_bet = min(to_call, team['stack']/20)
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

