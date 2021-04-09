import random

from pony.orm import db_session, select

import Settings_dafault
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from bot.models import Products
from keyboard import steps


class Bot:

    def __init__(self, token, group_id):
        self.token = token
        self.group_id = group_id
        self.vk = vk_api.VkApi(token=self.token)
        self.long_poller = VkBotLongPoll(vk=self.vk, group_id=self.group_id)
        self.api = self.vk.get_api()
        self.keyboard = VkKeyboard()
        self.message = str
        self.step = 0
        self.event = None

    def run(self):
        """Запуск Бота"""
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                print('Ошибка в обработке события', event.type)

    def scenario(self, key_input):
        if str(key_input).capitalize() in steps[self.step]['buttons']:
            if str(key_input).capitalize() == "Назад":
                self.step -= 1
            else:
                self.step += 1
            self.prepare_keyboard_message(key_input)
        else:
            self.prepare_keyboard_message(key_input)
            self.api.messages.send(
                message='Нажмите на кнопку',
                random_id=random.randint(0, 2 ** 20),
                peer_id=self.event.message.peer_id,
                keyboard=self.keyboard.get_keyboard(),
            )

    def prepare_keyboard_message(self, key_input):
        """Подготавливаем клавиатуру и сообщение"""
        self.keyboard = VkKeyboard()
        for main_buttons in steps[self.step]['buttons']:
            self.keyboard.add_button(label=main_buttons, color=VkKeyboardColor.PRIMARY)
        self.message = steps[self.step]['message']
        self.api.messages.send(
            message=self.message,
            random_id=random.randint(0, 2 ** 20),
            peer_id=self.event.message.peer_id,
            keyboard=self.keyboard.get_keyboard(),
        )

    @db_session
    def database(self):
        """записываем и берём информацию из базы"""
        products_5 = select(p for p in Products.name if Products.id < 6)
        return products_5

    def on_event(self, event):
        """Обрабатываем событие"""
        if event.type.value == 'message_new':
            self.event = event
            print(event.message.from_id, 'Сообщение: ', event.message.text)
            self.scenario(key_input=event.message.text)


if __name__ == '__main__':
    bot = Bot(token=Settings_dafault.TOKEN, group_id=Settings_dafault.GROUP_ID)
    bot.run()
