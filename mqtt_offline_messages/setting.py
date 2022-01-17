from environs import Env

env = Env()
env.read_env()


class Config:
    telegram_token = env.str("TELEGRAM_TOKEN")
    telegram_api = env.str("TELEGRAM_API")
    telegram_chat_id = env.int("TELEGRAM_CHAT_ID")
    mqtt_api = env.str("MQTT_API")
    headers = env.json("HEADERS")
    offline_messages = env.int("OFFLINE_MESSAGES")