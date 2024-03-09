import glob
import json
import collections
import os.path

input_directory = 'Json_files'
total_bet_amount = 200  # Change this to the desired total bet amount in dollars
SPORTS = [
    'rugbyleague_nrl',
    'mma_mixed_martial_arts',
    'icehockey_nhl',
    'basketball_nba',
    'boxing_boxing',
    'cricket_big_bash',
    'soccer_australia_aleague',
    'soccer_austria_bundesliga',
    'soccer_belgium_first_div',
    'soccer_brazil_campeonato',
    'soccer_chile_campeonato',
    'soccer_china_superleague',
    'soccer_conmebol_copa_libertadores',
    'soccer_denmark_superliga',
    'soccer_efl_champ',
    'soccer_england_league1',
    'soccer_england_league2',
    'soccer_epl',
    'soccer_fa_cup',
    'soccer_france_ligue_one',
    'soccer_france_ligue_two',
    'soccer_germany_bundesliga',
    'soccer_germany_bundesliga2',
    'soccer_germany_liga3',
    'soccer_greece_super_league',
    'soccer_italy_serie_a',
    'soccer_italy_serie_b',
    'soccer_japan_j_league',
    'soccer_korea_kleague1',
    'soccer_league_of_ireland',
    'soccer_mexico_ligamx',
    'soccer_netherlands_eredivisie',
    'soccer_poland_ekstraklasa',
    'soccer_portugal_primeira_liga',
    'soccer_spain_la_liga',
    'soccer_spain_segunda_division',
    'soccer_spl',
    'soccer_sweden_allsvenskan',
    'soccer_switzerland_superleague',
    'soccer_turkey_super_league',
    'soccer_uefa_champs_league',
    'soccer_uefa_euro_qualification',
    'soccer_uefa_europa_conference_league',
    'soccer_uefa_europa_league',
    'soccer_usa_mls',
    'baseball_mlb',
    'baseball_mlb_preseason',
    'cricket_odi'
]
available_bookmakers = ["unibet", "ladbrokes_au", "pointsbetau", "playup", "tab", "neds", "bluebet", "betr_au",
                        "sportsbet", "betfair_ex_au"]

output_directory = 'found'
output_filename = '2-way-arbitrage.txt'
output_file_path = os.path.join(output_directory, output_filename)
# Delete existing txt files in the directory
existing_arb_files = glob.glob(os.path.join(output_directory, output_filename))
os.makedirs(output_directory, exist_ok=True)
for file in existing_arb_files:
    os.remove(file)




# Open the file for reading


def find_arbitrage_opportunities(odds_json, total_bet_amount, available_bookmakers, output_file_path):
    for event in odds_json:
        print('** {} - {} vs {} **'.format(event['sport_title'], event['home_team'], event['away_team']))
        print('=====================================================================')
        for bookmaker in event['bookmakers']:
            print(f"Bookmaker: {bookmaker['key']}")

            odds_str = ""
            for market in bookmaker['markets']:
                if market['key'] == 'h2h':
                    for outcome in market['outcomes']:
                        odds_str += f"{outcome['name']}: {outcome['price']} "

            print(odds_str)
            print('---------------------------------------------------------------------')

        print('=====================================================================')

        odds_dict = collections.defaultdict(list)

        # fill odds_dict
        for bookmaker in event['bookmakers']:
            bookmaker_name = bookmaker['key']
            if bookmaker_name not in available_bookmakers:
                continue
            for market in bookmaker['markets']:
                if market['key'] != 'h2h':
                    continue
                outcomes = market['outcomes']

                if outcomes[0]['price'] < 2 and outcomes[1]['price'] < 2:
                    # both odds negative. ignore this bet.
                    pass
                if outcomes[0]['price'] > 2 and outcomes[1]['price'] > 2:
                    # both odds positive. ignore this bet.
                    # TODO: is this a possible scenario?
                    pass
                elif outcomes[0]['price'] > 2:
                    # first team has positive odd (first team = underdog, second team = favorite)
                    odds_dict[outcomes[0]['name']].append(
                        {'bookmaker': bookmaker_name, 'underdog': outcomes[0], 'favorite': outcomes[1]})
                else:
                    # second team has positive odd (first team = favorite, second team = underdog)
                    odds_dict[outcomes[1]['name']].append(
                        {'bookmaker': bookmaker_name, 'underdog': outcomes[1], 'favorite': outcomes[0]})


        # ...

        # ...
        # Set the total bet amount (adjust this value based on your requirements)

        # Calculate max underdog odd and max favorite odd (max = most positive)
        for team_name in [event['home_team'], event['away_team']]:
            odds_list = odds_dict[team_name]
            if not odds_list:
                continue
            underdog_max_odd_entity = max(odds_list, key=lambda x: x['underdog']['price'])
            underdog_max_odd = underdog_max_odd_entity['underdog']['price']
            underdog_max_odd_bookmaker = underdog_max_odd_entity['bookmaker']
            favorite_max_odd_entity = max(odds_list, key=lambda x: x['favorite']['price'])
            favorite_max_odd = favorite_max_odd_entity['favorite']['price']
            favorite_max_odd_bookmaker = favorite_max_odd_entity['bookmaker']

            # Check if one of the odds is above 2 and the other is below 2
            if (underdog_max_odd > 2 and favorite_max_odd < 2) or (underdog_max_odd < 2 and favorite_max_odd > 2):
                # Calculate arbitrage percentage
                arb_percentage = ((1 / (underdog_max_odd / 100)) + (1 / (favorite_max_odd / 100)))

                # Check if arbitrage opportunity is profitable
                if arb_percentage < 100:
                    # Calculate individual odds percentage
                    underdog_percentage = (1 / (underdog_max_odd)) * 100
                    favorite_percentage = (1 / (favorite_max_odd)) * 100

                    # Calculate stakes
                    underdog_stake = (total_bet_amount * underdog_percentage) / arb_percentage
                    favorite_stake = (total_bet_amount * favorite_percentage) / arb_percentage

                    # Calculate potential returns
                    underdog_return = underdog_stake * underdog_max_odd
                    favorite_return = favorite_stake * favorite_max_odd

                    # Calculate profits
                    underdog_profit = underdog_return - total_bet_amount
                    favorite_profit = favorite_return - total_bet_amount

                    arbitrage_found = True

                    # Append to email content

                    # Print to console
                    print('{} (underdog) vs {} (favorite) '.format(underdog_max_odd_entity['underdog']['name'],
                                                                   favorite_max_odd_entity['favorite']['name']))
                    print('Arbitrage Percentage: {:.2f}%'.format(arb_percentage))
                    print('Stake ${:.2f} on {} (underdog) from [{}] - Odds: ${:.2f}'.format(
                        underdog_stake, underdog_max_odd_entity['underdog']['name'], underdog_max_odd_bookmaker,
                        underdog_max_odd))
                    print('Stake ${:.2f} on {} (favorite) from [{}] - Odds: ${:.2f}'.format(
                        favorite_stake, favorite_max_odd_entity['favorite']['name'], favorite_max_odd_bookmaker,
                        favorite_max_odd))
                    print('Underdog Return: ${:.2f}, Profit: ${:.2f}'.format(underdog_return, underdog_profit))
                    print('Favorite Return: ${:.2f}, Profit: ${:.2f}'.format(favorite_return, favorite_profit))
                    print('---------------------------------------------------------------------')
                    # Append to the output file
                    with open(output_file_path, 'a', encoding='utf-8') as output_file:
                        print('****{}*****'.format(event['sport_title']), file=output_file)
                        print('{} (underdog) vs {} (favorite) '.format(
                            underdog_max_odd_entity['underdog']['name'],
                            favorite_max_odd_entity['favorite']['name']),
                            file=output_file)
                        print('Arbitrage Percentage: {:.2f}%'.format(arb_percentage), file=output_file)
                        print('Stake ${:.2f} on {} (underdog) from [{}] - Odds: ${:.2f}'.format(
                            underdog_stake, underdog_max_odd_entity['underdog']['name'], underdog_max_odd_bookmaker,
                            underdog_max_odd), file=output_file)
                        print('Stake ${:.2f} on {} (favorite) from [{}] - Odds: ${:.2f}'.format(
                            favorite_stake, favorite_max_odd_entity['favorite']['name'], favorite_max_odd_bookmaker,
                            favorite_max_odd), file=output_file)
                        print('Underdog Return: ${:.2f}, Profit: ${:.2f}'.format(underdog_return, underdog_profit),
                              file=output_file)
                        print('Favorite Return: ${:.2f}, Profit: ${:.2f}'.format(favorite_return, favorite_profit),
                              file=output_file)
                        print('---------------------------------------------------------------------', file=output_file)



for SPORT in SPORTS:
    input_filename = f'output_{SPORT}.json'
    input_file_path = os.path.join(input_directory, input_filename)


    with open(input_file_path, 'r') as json_file:
        # Load the JSON content
        odds_json = json.load(json_file)
        find_arbitrage_opportunities(odds_json, total_bet_amount, available_bookmakers, output_file_path)
with open(output_file_path, 'a') as output_file:
    print('---------------------next----set-------------------------------------', file=output_file)
    print('---------------------next----set-------------------------------------', file=output_file)
available_bookmakers = ["unibet", "ladbrokes_au", "pointsbetau", "playup", "tab", "neds", "bluebet", "betr_au",
                        "sportsbet"]
for SPORT in SPORTS:
    input_filename = f'output_{SPORT}.json'
    input_file_path = os.path.join(input_directory, input_filename)


    with open(input_file_path, 'r') as json_file:
        # Load the JSON content
        odds_json = json.load(json_file)
        find_arbitrage_opportunities(odds_json, total_bet_amount, available_bookmakers, output_file_path)
