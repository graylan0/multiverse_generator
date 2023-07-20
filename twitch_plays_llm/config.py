from pydantic import BaseModel
import json

class Settings(BaseModel):
    twitch_bot_username: str
    twitch_bot_client_id: str
    twitch_channel_name: str
    openai_api_key: str

    vote_delay: int = 20
    backend_port: int = 9511

    @classmethod
    def load_config(cls):
        with open('config.json') as config_file:
            config = json.load(config_file)
        return cls(
            twitch_bot_username=config['twitch']['clientkey'],
            twitch_bot_client_id=config['twitch']['clientkey'],
            twitch_channel_name=config['twitch']['hostchannel'],
            openai_api_key=config['openai']['api_key'],
        )

config = Settings.load_config()
