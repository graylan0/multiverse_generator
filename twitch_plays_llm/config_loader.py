import json
import openai

# Load the configuration file
with open('C:\\Users\\gray00\\gpt\\gamejam_twitch\\config.json') as config_file:
    config = json.load(config_file)

# Now you can access your keys
client_id = config['twitch']['clientkey']
channel_name = config['twitch']['hostchannel']
openai_api_key = config['openai']['api_key']
openai.api_key = openai_api_key
