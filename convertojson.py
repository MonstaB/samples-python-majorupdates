import json

# Read the content from the 'active_sports.txt' file
with open('active_sports.txt', 'r') as file:
    input_string = file.read()

# Parse the input string as a Python dictionary
data = json.loads(input_string)

# Convert the Python dictionary to a JSON string with indentation for better readability
json_string = json.dumps(data, indent=2)

# Save the JSON string to a file named 'active_sport.json'
with open('active_sport.json', 'w') as json_file:
    json_file.write(json_string)

print("Conversion successful. JSON file saved as 'active_sport.json'")

# Extract 'key' values from the data
keys = [item['key'] for item in data]

# Save the 'keys' list to a file named 'active_sports_keys.txt'
with open('active_sports_keys.txt', 'w') as keys_file:
    for key in keys:
        keys_file.write(f"{key}\n")

print("Keys extracted and saved to 'active_sports_keys.txt'")

#
#
#
with open('all_sports.txt', 'r') as file:
    input_string = file.read()

# Parse the input string as a Python dictionary
data = json.loads(input_string)

# Convert the Python dictionary to a JSON string with indentation for better readability
json_string = json.dumps(data, indent=2)

# Save the JSON string to a file named 'active_sport.json'
with open('all_sports.json', 'w') as json_file:
    json_file.write(json_string)

print("Conversion successful. JSON file saved as 'all_sport.json'")

# Extract 'key' values from the data
keys = [item['key'] for item in data]

# Save the 'keys' list to a file named 'active_sports_keys.txt'
with open('all_sports_keys.txt', 'w') as keys_file:
    for key in keys:
        keys_file.write(f"{key}\n")

print("Keys extracted and saved to 'all_sports_keys.txt'")