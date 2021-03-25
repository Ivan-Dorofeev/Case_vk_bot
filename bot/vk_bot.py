import logging
import random

import Settings_dafault
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

try:
    import Settings
except ImportError:
    exit('DO COPY Settings.py and set token')


class Bot:

    def __init__(self, token, group_id):
        """
        :param token: секретный токен
        :param group_id: группа id из группы в vk.com
        """
        self.token = token
        self.group_id = group_id
        self.vk = vk_api.VkApi(token=self.token)
        self.long_poller = VkBotLongPoll(vk=self.vk, group_id=self.group_id)
        self.api = self.vk.get_api()
        self.user_states = dict()  # user_id -> UserState

    def run(self):
        """Запуск Бота"""
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                print('ошибка в обработке события', event.type)

    def on_event(self, event):
        """
        Обрабатывает собщение Бота.
        Отправляет сообщение назад, если сообщение текст
        """

        if event.type.value == 'message_new':
            print(event.message.from_id, 'Сообщение: ', event.message.text)
            user_id = event.message.peer_id
            self.api.message.send(
                message='Выбери с клавиататуры',
                random_id=random.randint(0, 2 ** 20),
                peer_id=user_id,
                keyboard={
                    "type": "message_new",
                    "object": {
                        "id": 41,
                        "date": 1526898082,
                        "out": 0,
                        "user_id": 163176673,
                        "read_state": 0,
                        "title": "",
                        "body": "Blue",
                        "payload": "{\"button\":\"4\"}"
                    },
                    "group_id": 194790108
                }
            )
        elif event.type.value == 'message_typing_state':
            print(event.object.from_id, 'печатает')
        else:
            print("Не умеем обрабатывать такое событие такого типа %s", event.type)


if __name__ == '__main__':
    bot = Bot(token=Settings_dafault.TOKEN, group_id=Settings_dafault.GROUP_ID)
    bot.run()
