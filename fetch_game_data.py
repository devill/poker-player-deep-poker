import re
import requests

TOURNAMENT_URL = 'http://live.leanpoker.org/api/tournament/58430f4e7e7a0f000403a6d5/game'
GAME_URL = 'http://live.leanpoker.org/api/tournament/58430f4e7e7a0f000403a6d5/game/%s/log'

# Get games ids in torunament
r = requests.get(TOURNAMENT_URL)
games = r.json()
game_ids = [game['id'] for game in games]

# Fetch and save game data
print('h0_rank,h0_suite,h1_rank,h1_suite,c0_rank,c0_suit,c1_rank,c1_suit,c2_rank,c2_suit,c3_rank,c3_suit,c4_rank,c4_suit')

for game_id in game_ids:
    r = requests.get(GAME_URL % game_id)
    game_data = r.json()

    winner_announcements = [wa for wa in game_data if 'type' in wa and wa['type'] == 'winner_announcement']

    for wa in winner_announcements:
        game_state = wa['game_state']

        community_cards = game_state['community_cards']

        winner_name = re.search('(.*) won \d+', wa['message']).group(1)

        winner = [player for player in game_state['players'] if player['name'] == winner_name][0]
        cards = winner['hole_cards']

        data = []

        for card in cards:
            data.append(card['rank'])
            data.append(card['suit'])

        for community_card in community_cards:
            data.append(community_card['rank'])
            data.append(community_card['suit'])

        print(','.join(data))

