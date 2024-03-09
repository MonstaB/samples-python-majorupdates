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
    'soccer_korea_kleague1',
    'baseball_mlb',
    'baseball_mlb_preseason',
    'cricket_odi'
]
available_bookmakers = ["unibet", "ladbrokes_au", "pointsbetau", "playup", "tab", "neds", "bluebet", "betr_au",
                        "sportsbet", "betfair_ex_au"]

output_directory = 'found'
output_filename = '2-way-spread-arbitrage.txt'
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
                if market['key'] == 'spreads':
                    for outcome in market['outcomes']:
                        odds_str += f"{outcome['name']}: {outcome['price']} "

            print(odds_str)
            print('---------------------------------------------------------------------')

        print('=====================================================================')

        odds_dict = collections.defaultdict(list)

        for bookmaker_data in odds_json:
            bookmaker_title = bookmaker_data.get('key', '')  # Use 'key' instead of 'title' if available
            if not bookmaker_title:
                continue

            for market_data in bookmaker_data.get('markets', []):
                if market_data['key'] == 'spreads':
                    for outcome_data in market_data.get('outcomes', []):
                        team_name = outcome_data.get('name', '')
                        price = outcome_data.get('price', 0)
                        point = outcome_data.get('point', 0)

                        # Assuming underdog has positive point value and favorite has negative point value
                        if point > 0:
                            underdog_max_odd_entity = {'name': team_name, 'price': price, 'point': point}
                        else:
                            favorite_max_odd_entity = {'name': team_name, 'price': price, 'point': point}

            # Calculate arbitrage if both underdog and favorite are found
            if 'underdog_max_odd_entity' in locals() and 'favorite_max_odd_entity' in locals():
                underdog_max_odd = underdog_max_odd_entity['price']
                underdog_max_odd_bookmaker = bookmaker_title
                favorite_max_odd = favorite_max_odd_entity['price']
                favorite_max_odd_bookmaker = bookmaker_title

                # Check if one of the odds is above 2 and the other is below 2
                if (underdog_max_odd > 2 and favorite_max_odd < 2) or (underdog_max_odd < 2 and favorite_max_odd > 2):
                    # Calculate arbitrage percentage
                    arb_percentage = ((1 / (underdog_max_odd / 100)) + (1 / (favorite_max_odd / 100)))

                    # Check if arbitrage opportunity is profitable
                    if arb_percentage < 100:
                        # Calculate individual odds percentage
                        underdog_percentage = (1 / underdog_max_odd) * 100
                        favorite_percentage = (1 / favorite_max_odd) * 100

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
                        print('{} (underdog) vs {} (favorite) '.format(underdog_max_odd_entity['name'],
                                                                       favorite_max_odd_entity['name']))
                        print('Arbitrage Percentage: {:.2f}%'.format(arb_percentage))
                        print('Stake ${:.2f} on {} (underdog) from [{}] - Odds: ${:.2f} - point: {}'.format(
                            underdog_stake, underdog_max_odd_entity['name'], underdog_max_odd_bookmaker,
                            underdog_max_odd, underdog_max_odd_entity['point']))
                        print('Stake ${:.2f} on {} (favorite) from [{}] - Odds: ${:.2f}'.format(
                            favorite_stake, favorite_max_odd_entity['name'], favorite_max_odd_bookmaker,
                            favorite_max_odd))
                        print('Underdog Return: ${:.2f}, Profit: ${:.2f}'.format(underdog_return, underdog_profit))
                        print('Favorite Return: ${:.2f}, Profit: ${:.2f}'.format(favorite_return, favorite_profit))
                        print('---------------------------------------------------------------------')
                        # Append to the output file
                        with open(output_file_path, 'a') as output_file:
                            print('****{}*****'.format(event['sport_title']), file=output_file)
                            print('{} (underdog) vs {} (favorite) '.format(underdog_max_odd_entity['name'],
                                                                           favorite_max_odd_entity['name']),
                                  file=output_file)
                            print('Arbitrage Percentage: {:.2f}%'.format(arb_percentage), file=output_file)
                            print('Stake ${:.2f} on {} (underdog) from [{}] - Odds: ${:.2f}'.format(
                                underdog_stake, underdog_max_odd_entity['name'], underdog_max_odd_bookmaker,
                                underdog_max_odd), file=output_file)
                            print('Stake ${:.2f} on {} (favorite) from [{}] - Odds: ${:.2f}'.format(
                                favorite_stake, favorite_max_odd_entity['name'], favorite_max_odd_bookmaker,
                                favorite_max_odd), file=output_file)
                            print('Underdog Return: ${:.2f}, Profit: ${:.2f}'.format(underdog_return, underdog_profit),
                                  file=output_file)
                            print('Favorite Return: ${:.2f}, Profit: ${:.2f}'.format(favorite_return, favorite_profit),
                                  file=output_file)
                            print('---------------------------------------------------------------------',
                                  file=output_file)



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