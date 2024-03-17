import glob
import json
import collections
import os.path
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

input_directory = 'Json_files'
total_bet_amount = 100  # Change this to the desired total bet amount in dollars
sports_list_file = config.get('SPORTS', 'MY_SPORTS_LIST_FILE')
with open(sports_list_file, 'r') as file:
    SPORTS = file.read().split(', ')

SPORTS = [SPORT.strip() for SPORT in SPORTS]
available_bookmakers = config.get('BOOKMAKERS', 'BOOKMAKERS_LIST').split(', ')

output_directory = 'found'
output_filename = '3-way-arbitrage.txt'
output_file_path = os.path.join(output_directory, output_filename)
os.makedirs(output_directory, exist_ok=True)
# Delete existing txt files in the directory
existing_arb_files = glob.glob(os.path.join(output_directory, output_filename))
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
                if len(outcomes) != 3:
                    pass
                if len(outcomes) == 3:
                    if outcomes[0]['price'] < 3 and outcomes[1]['price'] < 3 and outcomes[2]['price'] < 3:
                        # all odds negative. ignore this bet.
                        pass
                    if outcomes[0]['price'] > 3 and outcomes[1]['price'] > 3 and outcomes[2]['price'] > 3:
                        # all odds positive. i wish.
                        pass
                    elif outcomes[0]['price'] > outcomes[1]['price']:
                        # first team has positive odd (first team = underdog, second team = favorite)
                        odds_dict[outcomes[0]['name']].append(
                            {'bookmaker': bookmaker_name, 'underdog': outcomes[0], 'favorite': outcomes[1],
                             'draw': outcomes[2]})
                    else:
                        # second team has positive odd (first team = favorite, second team = underdog)
                        odds_dict[outcomes[1]['name']].append(
                            {'bookmaker': bookmaker_name, 'underdog': outcomes[1], 'favorite': outcomes[0],
                             'draw': outcomes[2]})

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
            draw_max_odd_entity = max(odds_list, key=lambda x: x['draw']['price'])
            draw_max_odd = draw_max_odd_entity['draw']['price']
            draw_max_odd_bookmaker = draw_max_odd_entity['bookmaker']

            # Check if one of the odds is above 2 and the other is below 2

            arb_percentage = (
                    (1 / (underdog_max_odd / 100)) + (1 / (favorite_max_odd / 100)) + (1 / (draw_max_odd / 100)))

            # Check if arbitrage opportunity is profitable
            if arb_percentage < 100:
                # Calculate individual odds percentage
                underdog_percentage = (1 / (underdog_max_odd)) * 100
                favorite_percentage = (1 / (favorite_max_odd)) * 100
                draw_percentage = (1 / (draw_max_odd)) * 100

                # Calculate stakes
                underdog_stake = (total_bet_amount * underdog_percentage) / arb_percentage
                favorite_stake = (total_bet_amount * favorite_percentage) / arb_percentage
                draw_stake = (total_bet_amount * draw_percentage) / arb_percentage

                # Calculate potential returns
                underdog_return = underdog_stake * underdog_max_odd
                favorite_return = favorite_stake * favorite_max_odd
                draw_return = draw_stake * draw_max_odd

                # Calculate profits
                underdog_profit = underdog_return - total_bet_amount
                favorite_profit = favorite_return - total_bet_amount
                draw_profit = draw_return - total_bet_amount

                arbitrage_found = True

                # Append to email content

                # Print to console
                # Print to console
                print(
                    f'{underdog_max_odd_entity["underdog"]["name"]} (underdog) vs {favorite_max_odd_entity["favorite"]["name"]} (favorite)')
                print(f'Arbitrage Percentage: {arb_percentage:.2f}%')
                print(
                    f'Stake ${underdog_stake:.2f} on {underdog_max_odd_entity["underdog"]["name"]} (underdog) from [{underdog_max_odd_bookmaker}] - Odds: {underdog_max_odd:.2f}')
                print(
                    f'Stake ${favorite_stake:.2f} on {favorite_max_odd_entity["favorite"]["name"]} (favorite) from [{favorite_max_odd_bookmaker}] - Odds: {favorite_max_odd:.2f}')
                print(f'Stake ${draw_stake:.2f} on Draw from [{draw_max_odd_bookmaker}] - Odds: {draw_max_odd:.2f}')
                print(f'Underdog Return: ${underdog_return:.2f}, Profit: ${underdog_profit:.2f}')
                print(f'Favorite Return: ${favorite_return:.2f}, Profit: ${favorite_profit:.2f}')
                print(f'Draw Return: ${draw_return:.2f}, Profit: ${draw_profit:.2f}')
                print('---------------------------------------------------------------------')

                # Append to the output file
                with open(output_file_path, 'a', encoding='utf-8') as output_file:
                    print(f'****{event["sport_title"]}****', file=output_file)
                    print(
                        f'{underdog_max_odd_entity["underdog"]["name"]} (underdog) vs '
                        f'{favorite_max_odd_entity["favorite"]["name"]} (favorite)',
                        file=output_file)
                    print(f'Arbitrage Percentage: {arb_percentage:.2f}%', file=output_file)
                    print(
                        f'Stake ${underdog_stake:.2f} on {underdog_max_odd_entity["underdog"]["name"]} (underdog) '
                        f'from [{underdog_max_odd_bookmaker}] - Odds: {underdog_max_odd:.2f}',
                        file=output_file)
                    print(
                        f'Stake ${favorite_stake:.2f} on {favorite_max_odd_entity["favorite"]["name"]} (favorite) '
                        f'from [{favorite_max_odd_bookmaker}] - Odds: {favorite_max_odd:.2f}',
                        file=output_file)
                    print(
                        f'Stake ${draw_stake:.2f} on Draw from [{draw_max_odd_bookmaker}] - Odds: {draw_max_odd:.2f}',
                        file=output_file)
                    print(f'Underdog Return: ${underdog_return:.2f}, Profit: ${underdog_profit:.2f}',
                          file=output_file)
                    print(f'Favorite Return: ${favorite_return:.2f}, Profit: ${favorite_profit:.2f}',
                          file=output_file)
                    print(f'Draw Return: ${draw_return:.2f}, Profit: ${draw_profit:.2f}', file=output_file)
                    print('---------------------------------------------------------------------', file=output_file)


for SPORT in SPORTS:
    input_filename = f'output_{SPORT}.json'
    input_file_path = os.path.join(input_directory, input_filename)

    with open(input_file_path, 'r') as json_file:
        # Load the JSON content
        odds_json = json.load(json_file)
        find_arbitrage_opportunities(odds_json, total_bet_amount, available_bookmakers, output_file_path)

# Now odds_json contains the data read from the file
# You can use it as needed in the rest of your scrip
