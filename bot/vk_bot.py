import logging
import random

import Settings_dafault
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
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
        self.keyboard = VkKeyboard()

    def run(self):
        """Запуск Бота"""
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                print('Ошибка в обработке события', event.type)

    def on_event(self, event):
        """
        Обрабатывает собщение Бота.
        Отправляет сообщение назад, если сообщение текст
        """

        if event.type.value == 'message_new':
            print(event.message.from_id, 'Сообщение: ', event.message.text)
            user_id = event.message.peer_id
            text_to_send = 'Выбери с клавиатуры'
            self.keyboard.add_button(label='Разделы', color=VkKeyboardColor.POSITIVE)
            self.api.messages.send(
                message=text_to_send,
                random_id=random.randint(0, 2 ** 20),
                peer_id=user_id,
                keyboard=self.keyboard.get_keyboard(),
            )
        elif event.type.value in ['message_typing_state', 'message_reply']:
            print(event.object.from_id, 'печатает/отвечает')
        else:
            print("Не умеем обрабатывать такое событие такого типа %s", event.type)


if __name__ == '__main__':
    bot = Bot(token=Settings_dafault.TOKEN, group_id=Settings_dafault.GROUP_ID)
    bot.run()
