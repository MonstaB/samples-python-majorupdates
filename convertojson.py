import json

# Read the content from the 'active_sport.json' file
with open('sports/active_sport.json', 'r') as file:
    input_string = file.read()

# Parse the input string as a Python dictionary
data = json.loads(input_string)

# Extract 'key' values from the data
keys = [item['key'] for item in data]

# Save the 'keys' list to a file named 'active_sports_keys.txt'
with open('sports/active_sports_keys.txt', 'w') as keys_file:
    for key in keys:
        keys_file.write(f"'{key}',\n")

print("Keys extracted and saved to 'active_sports_keys.txt'")

#
#
#
with open('sports/all_sports.json', 'r') as file:
    input_string = file.read()

# Parse the input string as a Python dictionary
data = json.loads(input_string)


# Extract 'key' values from the data
keys = [item['key'] for item in data]

# Save the 'keys' list to a file named 'active_sports_keys.txt'
with open('sports/all_sports_keys.txt', 'w') as keys_file:
    for key in keys:
        keys_file.write(f"{key}\n")

print("Keys extracted and saved to 'all_sports_keys.txt'")