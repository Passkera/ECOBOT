"""
    Bot for eco forum
        https://vk.com/rso_eco

           by Paskera
                        """

import vk_api
import pymysql
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from config import api

# Connect to DB
try:
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='Paskera',
        password='912t2414',
        database='eco',
        cursorclass=pymysql.cursors.DictCursor
    )

except Exception as error:
    print(f"DB error {error}")

# Auth in vk
try:
    vk_session = vk_api.VkApi(token=api)
    longpoll = VkLongPoll(vk_session)
except Exception as error:
    print(f"Error with the connection BOT\n {error}")

try:
    def send_msg(id, text, keyboard=None):
        if keyboard is None:
            vk_session.method('messages.send',
                              {'user_id': id, 'message': text, 'random_id': 0, })
        else:
            vk_session.method('messages.send',
                              {'user_id': id, 'message': text, 'random_id': 0, 'keyboard': keyboard.get_keyboard()})


    def get_name(user_id):
        return vk_session.method('users.get', {'user_id': user_id})[0]['first_name'] + ' ' + \
            vk_session.method('users.get', {'user_id': user_id})[0]['last_name']


    def send_attachment(id, url, text=None):
        vk_session.method('messages.send', {'user_id': id, 'message': text, 'attachment': url, 'random_id': 0})


    top_users = False
    test1 = False
    test2 = False
    test3 = False
    test4 = False
    test5 = False
    test6 = False
    test7 = False
    test8 = False
    test9 = False
    test10 = False
    test11 = False
    test12 = False
    test13 = False

    # Wait message from user
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                if event.from_user:
                    id = event.user_id
                    print(id)
                    msg = event.text.lower()
                    peer_id = event.peer_id

                    if msg == 'начать':
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute(f"INSERT INTO `users` (`id`,`score`) "
                                               f"VALUES ({id}, 0) ON DUPLICATE KEY UPDATE score = score;")
                                # cursor.execute("INSERT INTO `users` (`id`,`score`) "
                                #                "VALUES (%s, 0) ON DUPLICATE KEY UPDATE score = score;", id)
                                connection.commit()
                        except Exception as error:
                            print(f"Error add score\n {error}")

                        keyboard = VkKeyboard()
                        keyboard.add_button('Программа форума', VkKeyboardColor.POSITIVE)
                        keyboard.add_button('Прочитать летопись', VkKeyboardColor.POSITIVE)
                        keyboard.add_line()
                        keyboard.add_button('Контакты кураторов', VkKeyboardColor.POSITIVE)
                        keyboard.add_button('Карта местности', VkKeyboardColor.POSITIVE)

                        send_msg(id, 'Привет! На связи твой виртуальный помощник жителей Трёхгорья Амалия 🌸', keyboard)

                    elif msg == 'прочитать летопись':
                        send_attachment(id, 'photo-225244714_456239049', """С чего же все начиналось?\n
                        Именно эту летопись нашел Толя в сундуке Бабулиты 🤭""")

                    elif msg == 'программа форума':
                        send_attachment(id, 'doc-225244714_674207609', 'Держи программу форума'
                                                                       '')
                    elif msg == 'контакты кураторов':
                        send_msg(id, """Кураторы\n\n@id275168794 (Майборода Яна Алексеевна) +79785715803\n
                        @id491854216 (Чаюн Татьяна Дмитриевна) +79783457623""")

                    elif msg == 'карта местности':
                        send_attachment(id, 'photo-225244714_456239050',
                                        """Чтобы не заблудиться в нашем городке, пользуйтесь картой 🗺""")

                    # First code phrase
                    elif msg == 'приз1':
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute(f"INSERT INTO `users` (`id`,`score`) "
                                               f"VALUES ({id}, 0) ON DUPLICATE KEY UPDATE score = score + 1;")
                                connection.commit()
                                send_msg(id, f"@id{id} ({get_name(id)}) получает +1 экоин")

                        except Exception as error:
                            print(f"Error add score\n {error}")

                    # Show top rating
                    elif msg == '/eco top':
                        top_users = True
                        send_msg(id, f"Сколько призёров?")
                        continue

                    elif top_users:
                        top_users = False
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute(f"select * from users order by score desc limit {msg}")
                                for row in cursor.fetchall():
                                    count = 0
                                    for key, value in row.items():
                                        if count == 1:
                                            score = value
                                        else:
                                            user = value
                                        count += 1
                                    send_msg(id, f"@id{user} ({get_name(user)}) имеет {score} экоинов")
                                connection.commit()
                        except Exception as error:
                            print(f"Error show stats\n {error}")

                    # Show city
                    elif msg == '/eco info':
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, "Важное напоминание ❣\n"
                                                        "Проанализируйте состояние Трёхгорья, возможно, и в самом городе уже не так чисто🍃\n"
                                                        "Если вы заметили экологическую проблему на территории, то скорее ее решите. И пришлите фото ДО/ПОСЛЕ, чтобы получить дополнительные баллы в ваш рейтинг 🕊")
                        except Exception as error:
                            print(f"Error send all user message\n {error}")

                    # Test 1
                    elif msg == '/eco test1':
                        test1 = True
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value,
                                                 "По ходу вашего путешествия вы можети решать тесты и зарабатывать экоины!\n"
                                                 "+1 экоин получит лишь тот, кто ответит первый правильно\n\n"
                                                 "В какой стране находится самая масштабная свалка мусорных отходов?")
                        except Exception as error:
                            print(f"Error send all user message\n {error}")
                        continue

                    elif test1 is True and msg == 'сша':
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute(f"INSERT INTO `users` (`id`,`score`) "
                                               f"VALUES ({id}, 0) ON DUPLICATE KEY UPDATE score = score + 1;")
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, f"Вопрос 1\nПравильный ответ: США\n"
                                                        f"@id{id} ({get_name(id)}) ответил на вопрос первый и получает +1 экоин ❤‍🔥")
                                connection.commit()
                                test1 = False
                        except Exception as error:
                            print(f"Error add score\n {error}")

                    # Test 2
                    elif msg == '/eco test2':
                        test2 = True
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, "Вопрос 2!\n"
                                                        "+1 экоин получит лишь тот, кто ответит первый правильно\n\n"
                                                        "Полиэтиленовый пакет, брошенный в лесу, пролежит без изменения больше ... лет")
                        except Exception as error:
                            print(f"Error send all user message\n {error}")
                        continue

                    elif test2 is True and (msg == '100' or msg == 'ста' or msg == 'сто'):
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute(f"INSERT INTO `users` (`id`,`score`) "
                                               f"VALUES ({id}, 0) ON DUPLICATE KEY UPDATE score = score + 1;")
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, f"Вопрос 2\nПравильный ответ: 100\n" 
                                        f"@id{id} ({get_name(id)}) ответил на вопрос первый и получает +1 экоин ❤‍🔥")
                                connection.commit()
                                test2 = False
                        except Exception as error:
                            print(f"Error add score\n {error}")

                    # Test 3
                    elif msg == '/eco test3':
                        test3 = True
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, "Вопрос 3!\n"
                                                        "+1 экоин получит лишь тот, кто ответит первый правильно\n\n"
                                                        "Наука о взаимодействии организмов между собой и с окружающей их средой называется ...")
                        except Exception as error:
                            print(f"Error send all user message\n {error}")
                        continue

                    elif test3 is True and msg == 'экология':
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute(f"INSERT INTO `users` (`id`,`score`) "
                                               f"VALUES ({id}, 0) ON DUPLICATE KEY UPDATE score = score + 1;")
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, f"Вопрос 3\nПравильный ответ: экология\n"
                                        f"@id{id} ({get_name(id)}) ответил на вопрос первый и получает +1 экоин ❤‍🔥")
                                connection.commit()
                                test3 = False
                        except Exception as error:
                            print(f"Error add score\n {error}")

                    # Test 4
                    elif msg == '/eco test4':
                        test4 = True
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, "Вопрос 4!\n"
                                                        "+1 экоин получит лишь тот, кто ответит первый правильно\n\n"
                                                        "Раздел экологии, который изучает основные принципы строения и функционирования различных надорганизменных систем называется ... ...")
                        except Exception as error:
                            print(f"Error send all user message\n {error}")
                        continue

                    elif test4 is True and msg == 'общая экология':
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute(f"INSERT INTO `users` (`id`,`score`) "
                                               f"VALUES ({id}, 0) ON DUPLICATE KEY UPDATE score = score + 1;")
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, f"Вопрос 4\nПравильный ответ: общая экология\n"
                                        f"@id{id} ({get_name(id)}) ответил на вопрос первый и получает +1 экоин ❤‍🔥")
                                connection.commit()
                                test4 = False
                        except Exception as error:
                            print(f"Error add score\n {error}")

                    # Test 5
                    elif msg == '/eco test5':
                        test5 = True
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, "Вопрос 5!\n"
                                                        "+1 экоин получит лишь тот, кто ответит первый правильно\n\n"
                                                        "Живая и неживая природа, окружающая растения, животных и человека называется ... ...")
                        except Exception as error:
                            print(f"Error send all user message\n {error}")
                        continue

                    elif test5 is True and msg == 'среда обитания':
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute(f"INSERT INTO `users` (`id`,`score`) "
                                               f"VALUES ({id}, 0) ON DUPLICATE KEY UPDATE score = score + 1;")
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, f"Вопрос 5\nПравильный ответ: среда обитания\n"
                                        f"@id{id} ({get_name(id)}) ответил на вопрос первый и получает +1 экоин ❤‍🔥")
                                connection.commit()
                                test5 = False
                        except Exception as error:
                            print(f"Error add score\n {error}")

                    # Test 6
                    elif msg == '/eco test6':
                        test6 = True
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, "Вопрос 6!\n"
                                                        "+1 экоин получит лишь тот, кто ответит первый правильно\n\n"
                                                        "Совокупность живых организмов (животных, растений, грибов и микроорганизмов), населяющих определенную территорию называют ...")
                        except Exception as error:
                            print(f"Error send all user message\n {error}")
                        continue

                    elif test6 is True and msg == 'биоценоз':
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute(f"INSERT INTO `users` (`id`,`score`) "
                                               f"VALUES ({id}, 0) ON DUPLICATE KEY UPDATE score = score + 1;")
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, f"Вопрос 6\nПравильный ответ: биоценоз\n"
                                        f"@id{id} ({get_name(id)}) ответил на вопрос первый и получает +1 экоин ❤‍🔥")
                                connection.commit()
                                test6 = False
                        except Exception as error:
                            print(f"Error add score\n {error}")

                    # Test 7
                    elif msg == '/eco test7':
                        test7 = True
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, "Вопрос 7!\n"
                                                        "+1 экоин получит лишь тот, кто ответит первый правильно\n\n"
                                                        "... ... - это регулярное наблюдение и контроль над состоянием окружающей среды; определение изменений, вызванных антропогенным воздействием")
                        except Exception as error:
                            print(f"Error send all user message\n {error}")
                        continue

                    elif test7 is True and msg == 'экологический мониторинг':
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute(f"INSERT INTO `users` (`id`,`score`) "
                                               f"VALUES ({id}, 0) ON DUPLICATE KEY UPDATE score = score + 1;")
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, f"Вопрос 7\nПравильный ответ: экологический мониторинг\n"
                                        f"@id{id} ({get_name(id)}) ответил на вопрос первый и получает +1 экоин ❤‍🔥")
                                connection.commit()
                                test7 = False
                        except Exception as error:
                            print(f"Error add score\n {error}")

                    # Test 8
                    elif msg == '/eco test8':
                        test8 = True
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, "Вопрос 8!\n"
                                                        "+1 экоин получит лишь тот, кто ответит первый правильно\n\n"
                                                        "Какой цвет имеет контейнер для макулатуры?")
                        except Exception as error:
                            print(f"Error send all user message\n {error}")
                        continue

                    elif test8 is True and msg == 'синий':
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute(f"INSERT INTO `users` (`id`,`score`) "
                                               f"VALUES ({id}, 0) ON DUPLICATE KEY UPDATE score = score + 1;")
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, f"Вопрос 8\nПравильный ответ: синий\n"
                                        f"@id{id} ({get_name(id)}) ответил на вопрос первый и получает +1 экоин ❤‍🔥")
                                connection.commit()
                                test8 = False
                        except Exception as error:
                            print(f"Error add score\n {error}")

                    # Test 9
                    elif msg == '/eco test9':
                        test9 = True
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, "Вопрос 9!\n"
                                                        "+1 экоин получит лишь тот, кто ответит первый правильно\n\n"
                                                        "Батарейки, градусники, лекарственные препараты это ... отходы")
                        except Exception as error:
                            print(f"Error send all user message\n {error}")
                        continue

                    elif test9 is True and msg == 'опасные':
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute(f"INSERT INTO `users` (`id`,`score`) "
                                               f"VALUES ({id}, 0) ON DUPLICATE KEY UPDATE score = score + 1;")
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, f"Вопрос 9\nПравильный ответ: опасные\n"
                                        f"@id{id} ({get_name(id)}) ответил на вопрос первый и получает +1 экоин ❤‍🔥")
                                connection.commit()
                                test9 = False
                        except Exception as error:
                            print(f"Error add score\n {error}")

                    # Test 10
                    elif msg == '/eco test10':
                        test10 = True
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, "Вопрос 10!\n"
                                                        "+1 экоин получит лишь тот, кто ответит первый правильно\n\n"
                                                        "Бытовой мусор делят на 4 категории: стекло, пластик, макулатура, ...")
                        except Exception as error:
                            print(f"Error send all user message\n {error}")
                        continue

                    elif test10 is True and msg == 'металл':
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute(f"INSERT INTO `users` (`id`,`score`) "
                                               f"VALUES ({id}, 0) ON DUPLICATE KEY UPDATE score = score + 1;")
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, f"Вопрос 10\nПравильный ответ: металл\n"
                                        f"@id{id} ({get_name(id)}) ответил на вопрос первый и получает +1 экоин ❤‍🔥")
                                connection.commit()
                                test10 = False
                        except Exception as error:
                            print(f"Error add score\n {error}")

                    # Test 11
                    elif msg == '/eco test11':
                        test11 = True
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, "Вопрос 11!\n"
                                                        "+1 экоин получит лишь тот, кто ответит первый правильно\n\n"
                                                        "... составляет большую часть мусора, загрязняющего Землю")
                        except Exception as error:
                            print(f"Error send all user message\n {error}")
                        continue

                    elif test11 is True and msg == 'бумага':
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute(f"INSERT INTO `users` (`id`,`score`) "
                                               f"VALUES ({id}, 0) ON DUPLICATE KEY UPDATE score = score + 1;")
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, f"Вопрос 11\nПравильный ответ: бумага\n"
                                        f"@id{id} ({get_name(id)}) ответил на вопрос первый и получает +1 экоин ❤‍🔥")
                                connection.commit()
                                test11 = False
                        except Exception as error:
                            print(f"Error add score\n {error}")

                    # Test 12
                    elif msg == '/eco test12':
                        test12 = True
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, "Вопрос 12!\n"
                                                        "+1 экоин получит лишь тот, кто ответит первый правильно\n\n"
                                                        "... - это наука, которая занимается мусором")
                        except Exception as error:
                            print(f"Error send all user message\n {error}")
                        continue

                    elif test12 is True and msg == 'гарбология':
                        try:
                            with connection.cursor() as cursor:
                                cursor.execute(f"INSERT INTO `users` (`id`,`score`) "
                                               f"VALUES ({id}, 0) ON DUPLICATE KEY UPDATE score = score + 1;")
                                cursor.execute("select id from users")
                                for row in cursor.fetchall():
                                    for value in row.values():
                                        send_msg(value, f"Вопрос 12\nПравильный ответ: гарбология\n"
                                        f"@id{id} ({get_name(id)}) ответил на вопрос первый и получает +1 экоин ❤‍🔥")
                                connection.commit()
                                test12 = False
                        except Exception as error:
                            print(f"Error add score\n {error}")

except Exception as error:
    print(f"Global error\n {error}")
