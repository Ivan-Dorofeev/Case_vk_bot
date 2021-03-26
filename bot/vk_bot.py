import random

import Settings_dafault
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class Bot:

    def __init__(self, token, group_id):
        self.token = token
        self.group_id = group_id
        self.vk = vk_api.VkApi(token=self.token)
        self.long_poller = VkBotLongPoll(vk=self.vk, group_id=self.group_id)
        self.api = self.vk.get_api()
        self.keyboard = VkKeyboard()
        self.buttons = ['Разделы', 'Товары', 'Корзина']

    def run(self):
        """Запуск Бота"""
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                print('Ошибка в обработке события', event.type)

    def prepare_keyboard(self):
        """Подготавливаем клавиатуру"""
        print('get_keyboard1 =',self.keyboard.get_keyboard())
        self.keyboard.add_button(label='Разделы', color=VkKeyboardColor.POSITIVE)
        self.keyboard.add_button(label='Товары', color=VkKeyboardColor.POSITIVE)
        self.keyboard.add_button(label='Корзина', color=VkKeyboardColor.POSITIVE)
        print('get_keyboard2 =', self.keyboard.get_keyboard())
        return self.keyboard

    def on_event(self, event):
        """Обрабатываем событие"""
        if event.type.value == 'message_new':
            print(event.message.from_id, 'Сообщение: ', event.message.text)
            self.prepare_keyboard()
            self.api.messages.send(
                message='',
                random_id=random.randint(0, 2 ** 20),
                peer_id=event.message.peer_id,
                keyboard=self.keyboard.get_keyboard(),
            )


if __name__ == '__main__':
    bot = Bot(token=Settings_dafault.TOKEN, group_id=Settings_dafault.GROUP_ID)
    bot.run()
