import argparse
import requests
import configparser
import json
import configparser
import os

# Get the current directory
current_directory = os.path.dirname(__file__)

# Move one directory up
parent_directory = os.path.dirname(current_directory)

# Combine with the filename to get the path of config.cfg
config_file_path = os.path.join(parent_directory, 'config.cfg')

# Create a ConfigParser object and read the config file
config = configparser.ConfigParser()
config.read(config_file_path)



# Obtain the api key that was passed in from the command line
parser = argparse.ArgumentParser(description='Sample V4')
parser.add_argument('--api-key', type=str, default='')
args = parser.parse_args()


# An api key is emailed to you when you sign up to a plan
# Get a free API key at https://api.the-odds-api.com/
API_KEY = args.api_key or config.get('DEFAULT', 'API_KEY')
sports_response = requests.get('https://api.the-odds-api.com/v4/sports', params={
    'api_key': API_KEY
})
output_file_path = os.path.join(parent_directory, config.get('SPORTS', 'ACTIVE_SPORTS_JSON'))
keys_output = os.path.join(parent_directory, config.get('SPORTS', 'SPORTS_LIST_FILE'))

if sports_response.status_code != 200:
    print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')
    exit(1)

else:
    print('List of in season sports:', sports_response.json())
    odds_json = sports_response.json()
    with open(output_file_path, 'w') as json_file:
        json.dump(odds_json, json_file, indent=2)


with open(output_file_path, 'r') as file:
    input_string = file.read()

    # Parse the input string as a Python dictionary
data = json.loads(input_string)

    # Extract 'key' values from the data
keys = [item['key'] for item in data]

    # Save the 'keys' list to a file named 'active_sports_keys.txt'
with open(keys_output, 'w') as keys_file:
    for key in keys:
        keys_file.write(f"{key}\n ")
print("Keys extracted and saved to 'active_sports_keys.txt'")

    # Save the 'keys' list to a file named 'active_sports_keys_backup.txt'
with open('../sports/active_sports_keys_backup.txt', 'w') as keys_file:
    for key in keys:
        keys_file.write(f"{key}\n ")
print("Keys extracted and saved to 'active_sports_keys_backup.txt'")
