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

# Read the original file and structure the sports
my_sports_path = os.path.join(parent_directory, config.get('SPORTS', 'MY_SPORTS_LIST_FILE'))
original_file_path = os.path.join(parent_directory, config.get('SPORTS', 'SPORTS_LIST_FILE'))



sports_sections = {}
current_section = None


with open(original_file_path, 'r') as file:
    for line in file:
        stripped_line = line.strip()
        if not stripped_line.isspace():
            current_section = stripped_line
            if current_section not in sports_sections:
                sports_sections[current_section] = [stripped_line]
            elif current_section is not None:
                sports_sections[current_section].append(stripped_line)


with open(my_sports_path, 'w') as new_file:
    new_file.write(', '.join(sports_sections))

print(f"Sorted sports structure written to {my_sports_path}")
