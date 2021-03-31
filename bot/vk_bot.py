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
        self.event = None

    def run(self):
        """Запуск Бота"""
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                print('Ошибка в обработке события', event.type)

    def scenario(self, input_word):
        print(self.event.object)
        if input_word == 'Разделы':
            print(self.keyboard)
            # self.send_empty_message()
            self.keyboard.add_button(label='Назад', color=VkKeyboardColor.PRIMARY)
            self.keyboard.add_line()
            self.keyboard.add_button(label='Спортивная', color=VkKeyboardColor.PRIMARY)
            self.keyboard.add_button(label='Повседневная', color=VkKeyboardColor.PRIMARY)
            self.keyboard.add_button(label='Хардкор', color=VkKeyboardColor.PRIMARY)
            print(self.keyboard.get_keyboard())
        elif input_word == 'Товары':
            # self.keyboard.add_line()
            # self.keyboard.add_button(label='Назад', color=VkKeyboardColor.PRIMARY)
            # self.keyboard.add_button(label='Положить в корзину', color=VkKeyboardColor.PRIMARY)
            self.send_empty_message()
        elif input_word == 'Корзина':
            # self.send_empty_message()
            # self.keyboard.get_empty_keyboard()
            self.keyboard.add_line()
            self.keyboard.add_button(label='Назад', color=VkKeyboardColor.PRIMARY)
            self.keyboard.add_button(label='Купить всё, что в корзине', color=VkKeyboardColor.NEGATIVE)
            print(self.keyboard.get_keyboard())

    def send_empty_message(self):
        self.api.messages.send(
            message='Тут я ещё не придумал, как быть',
            random_id=random.randint(0, 2 ** 20),
            peer_id=self.event.message.peer_id,
            keyboard=self.keyboard.get_empty_keyboard(),
        )

    def send_message(self):
        self.api.messages.send(
            message='Выберите что-нибудь из разделов ниже',
            random_id=random.randint(0, 2 ** 20),
            peer_id=self.event.message.peer_id,
            keyboard=self.keyboard.get_keyboard(),
        )
        print(self.api.messages)

    def prepare_keyboard(self, key_input):
        """Подготавливаем клавиатуру и отправляем ответ"""
        if str(key_input).capitalize() in ['Разделы', 'Товары', 'Корзина']:
            self.scenario(input_word=str(key_input).capitalize())
            self.send_message()
        else:
            self.keyboard.add_button(label='Разделы', color=VkKeyboardColor.POSITIVE)
            self.keyboard.add_button(label='Товары', color=VkKeyboardColor.POSITIVE)
            self.keyboard.add_button(label='Корзина', color=VkKeyboardColor.POSITIVE)
            self.api.messages.send(
                message='Выберите что-нибудь из разделов ниже',
                random_id=random.randint(0, 2 ** 20),
                peer_id=self.event.message.peer_id,
                keyboard=self.keyboard.get_keyboard(),
            )

    def on_event(self, event):
        """Обрабатываем событие"""
        if event.type.value == 'message_new':
            self.event = event
            print(event.message.from_id, 'Сообщение: ', event.message.text)
            self.prepare_keyboard(key_input=event.message.text)


if __name__ == '__main__':
    bot = Bot(token=Settings_dafault.TOKEN, group_id=Settings_dafault.GROUP_ID)
    bot.run()
