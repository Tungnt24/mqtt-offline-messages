import requests
import time
from typing import List

from setting import Config
from logger import logger

import schedule


def get_client_offline(url: str, headers: dict) -> List:
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    result = []
    for client in data['table']:
        if not client.get("is_online"):
            result.append({"client_id": client.get("client_id"),
                          "offline_messages": client.get("offline_messages")})
    return result


def send_message(content: str) -> None:
    logger.info("sending message....")
    res = requests.post(Config.telegram_api.format(
        Config.telegram_token, Config.telegram_chat_id, content))
    logger.info("response code: %s, reason: %s", res.status_code, res.content)


def create_message(clients: List[dict]) -> str:
    client_info = []
    total_offline_message = 0
    message = ""
    for client in clients:
        offline_messages = client.get("offline_messages")
        total_offline_message += offline_messages
        if offline_messages > 0:
            client_info.append(str(client))
    if total_offline_message >= Config.offline_messages:
        message = "```{}\ntotal: {}```".format("\n".join(client_info), total_offline_message)
    print(message)
    return message


def main():
    clients = get_client_offline(Config.mqtt_api, Config.headers)
    message = create_message(clients)
    if message:
        send_message(message)


if __name__ == "__main__":
    schedule.every(5).seconds.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
