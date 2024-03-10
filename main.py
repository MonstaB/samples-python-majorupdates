import argparse
import glob
import configparser
import requests
import json
import os.path

config = configparser.ConfigParser()
config.read('config.cfg')
output_directory = 'Json_files'

os.makedirs(output_directory, exist_ok=True)
# Delete existing JSON files in the directory
existing_json_files = glob.glob(os.path.join(output_directory, '*.json'))
for file in existing_json_files:
    os.remove(file)

api_key_in_env = os.getenv("api_key")

# Obtain the api key that was passed in from the command line
parser = argparse.ArgumentParser(description='Sample V4')
parser.add_argument('--api-key', type=str, default='')
args = parser.parse_args()

# An api key is emailed to you when you sign up to a plan
# Get a free API key at https://api.the-odds-api.com/
API_KEY = args.api_key or config.get('DEFAULT', 'API_KEY')

# Sport key
# Find sport keys from the /sports endpoint below, or from https://the-odds-api.com/sports-odds-data/sports-apis.html
# Alternatively use 'upcoming' to see the next 8 games across all sports
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
# Bookmaker regions
# uk | us | us2 | eu | au. Multiple can be specified if comma delimited.
# More info at https://the-odds-api.com/sports-odds-data/bookmaker-apis.html
REGIONS = 'au'

# Odds markets
# h2h | spreads | totals. Multiple can be specified if comma delimited
# More info at https://the-odds-api.com/sports-odds-data/betting-markets.html
# Note only featured markets (h2h, spreads, totals) are available with the o's endpoint.
MARKETS = 'h2h'
# Odds format
# decimal | american
ODDS_FORMAT = 'decimal'

# Date format
# iso | unix
DATE_FORMAT = 'iso'

available_bookmakers = config.get('BOOKMAKERS', 'BOOKMAKERS_LIST').split(', ')

for SPORT in SPORTS:
    odds_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds', params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    })

    if odds_response.status_code != 200:
        print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')
        exit()

    else:
        odds_json = odds_response.json()
        output_filename = f'output_{SPORT}.json'
        output_file_path = os.path.join(output_directory, output_filename)

        with open(output_file_path, 'w') as json_file:
            json.dump(odds_json, json_file, indent=2)

        print('Number of events:', len(odds_json))

        # Check the usage quota
        print('Remaining requests', odds_response.headers['x-requests-remaining'])
        print('Used requests', odds_response.headers['x-requests-used'])

        print('---------------------------------------------------------------------')
