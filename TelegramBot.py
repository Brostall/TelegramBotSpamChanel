from pyrogram import Client  # телеграм клиент
import shelve  # запись информации в файл
import random  # для выбора случайного элемента из списка
import time  # для задержки

api_id = 12345678 # WRITE UR API ID
api_hash = "YOR API HASH"
phone_number = 'PHONE NUMBER (BOT)'
PUBLIC = ['NAME OF PUBLIC', 'NAME OF PUBLIC']  # паблики
# Варианты текстов сообщений RANDOM MEESEGES UR BOT SAYS IN CHAT
TEXTS = [
    'Неплохо👌',
    'Может быть😅',
    'Ничего особенного🤷‍♀️',
    'Понимаю)',
    'Не плохо👍',
    'Ого',
    'Нормально😉',
    'Класс👍',
    'Супер💖',
]
COMMENT_EVERY_N = 1  # комментируем каждое N сообщение

# список обработанных сообщений
processed_messages = shelve.open('processed_messages.db', writeback=True)

# создаем клиент телеграма
app = Client(name="WRITE UR BOT NAME", api_id=api_id, api_hash=api_hash, phone_number=phone_number)

with app:
    for p in PUBLIC:
        public = app.get_chat(p)  # ищем паблик по нику
        chat = public.linked_chat  # связанный чат обсуждений паблика
        
        for msg in app.get_chat_history(chat.id, limit=100):
            # фильтруем только авторепосты из паблика
            if msg.from_user is None:  # если сообщение не имеет автора
                if msg.forward_from_chat is not None and msg.forward_from_chat.id == public.id:
                    if msg.forward_from_message_id % COMMENT_EVERY_N != 0:
                        print(f'Пропускаем message_id={msg.forward_from_message_id},'
                              f' так как комментируем каждое {COMMENT_EVERY_N}')
                        continue
                    # проверяем, есть ли в списке обработанных сообщений этот айди
                    # чтобы не комментировать по несколько раз один пост
                    if str(msg.forward_from_message_id) in processed_messages:
                        print(f'Пропускаем уже обработанное message_id={msg.forward_from_message_id}')
                        continue
                    # пишем в список обработанных айди этого сообщения
                    processed_messages[str(msg.forward_from_message_id)] = True

                    print(f'Обработка message_id={msg.forward_from_message_id}')

                    text = random.choice(TEXTS)  # выбираем случайный текст из списка
                    app.send_message(chat.id, text,  # отправляем текст в чат
                                     reply_to_message_id=msg.forward_from_message_id)  # как ответ на сообщение с постом

                    # для того, чтоб не оставлять больше одного коммента за 5 минут
                    break  # выходим из перебора сообщений, если оставили коммент

        print('Ставим на паузу')
        time.sleep(5000)
