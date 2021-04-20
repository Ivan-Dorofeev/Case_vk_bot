import random

import requests
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from keyboard import steps
import Settings_dafault
from models import *


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
        self.user_id = None

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

    def prepare_keyboard_message(self, key_input):
        """Подготавливаем клавиатуру и сообщение"""
        self.keyboard = VkKeyboard()
        for main_buttons in steps[self.step]['buttons']:
            self.keyboard.add_button(label=main_buttons, color=VkKeyboardColor.PRIMARY)
        if self.step > 1:
            product_list = get_products_by_type(shoes_type=str(key_input).capitalize())
            for product_name in product_list:
                p_id = product_name[0]
                p_name = product_name[1]
                p_description = product_name[2]
                p_counts = product_name[3]
                p_price = product_name[4]
                p_pictures = product_name[5]
                self.message = f'#{p_id} /n ,{p_name}, Описание: {p_description}, Цена: {p_price}, В наличии: {p_counts}'
                self.send_message()
                self.send_image(p_pictures, user_id=self.user_id, product_name=p_name)
            self.keyboard = VkKeyboard()
            for p_button in product_list:
                self.keyboard.add_button(label=p_button[1], color=VkKeyboardColor.PRIMARY)
            self.message = "Выберите название товара, чтобы положить в корзину"
        else:
            self.message = steps[self.step]['message']
        self.send_message()

    def send_message(self):
        self.api.message.send(
            message=self.message,
            random_id=random.randint(0, 3 ** 20),
            peer_id=self.event.message.peer_id,
            keyboard=self.keyboard.get_keyboard(),
        )

    def send_image(self, image, user_id, product_name):
        upload_url = self.api.photos.getMessagesUploadServer()['upload_url']
        upload_data = requests.post(url=upload_url, files={'photo': ('image.png', image, 'image/png')}).json()
        image_data = self.api.photos.saveMessagesPhoto(**upload_data)
        owner_id = image_data[0]['owner_id']
        media_id = image_data[0]['id']
        attachment = f'photo{owner_id}_{media_id}'
        self.api.messages.send(
            message=product_name,
            attachment=attachment,
            random_id=random.randint(0, 2 ** 20),
            peer_id=user_id
        )

    @db_session
    def on_event(self, event):
        """Обрабатываем событие"""
        if event.type.value == 'message_new':
            self.event = event
            print(event.message.from_id, 'Сообщение: ', event.message.text)
            self.scenario(key_input=event.message.text)


if __name__ == '__main__':
    bot = Bot(token=Settings_dafault.TOKEN, group_id=Settings_dafault.GROUP_ID)
    bot.run()
