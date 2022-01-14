import asyncio
import requests
from aiogram import types
from random import choice, randint
from bs4 import BeautifulSoup as BS
from datetime import datetime
from Variables.config import *
from Variables.error_messages import *
from Variables.text_messages import *
from Databases.database_sql import DatabaseSQL


class FunctionsBot:

    def __init__(self):
        try:
            self.db_sql = DatabaseSQL()
        except Exception as error:
            logger.error(error)


    async def mailing_message_start(self, user_id):
        try:
            await asyncio.sleep(5)
            photo = open(PATH_TO_IMG, 'rb')
            await bot.send_photo(user_id, photo)
            
            await asyncio.sleep(5)
            markup_inline = types.InlineKeyboardMarkup()
            start_get = types.InlineKeyboardButton(text='Начать получать заказы ✅', callback_data=CATEGORY)
            markup_inline.add(start_get)
            await bot.send_message(user_id, start_message_2, reply_markup=markup_inline)
            
            wait = 10

            while True:
                await asyncio.sleep(10)
                tariffs = self.db_sql.get_tariff(user_id)
                if tariffs == None:
                    tariffs = self.db_sql.get_tariff(user_id)

                if COMMAND_FREE_TARIFF in tariffs or COMMAND_ONE_TARIFF in tariffs or COMMAND_TWO_TARIFF in tariffs or COMMAND_THREE_TARIFF in tariffs:
                    break

                wait += 10
                if wait == TIME_SLEEP_MAILING_START_1:
                    markup_inline = types.InlineKeyboardMarkup()
                    item_1 = types.InlineKeyboardButton(text="Активировать подписку 🎁", callback_data = CATEGORY)
                    markup_inline.add(item_1)

                    try:
                        await bot.send_message(user_id, MAILING_MESSAGE_START_1, reply_markup=markup_inline)
                    except:
                        logger.info(f"Пользователь {user_id} заблокировал бота")
                        break

                elif wait == TIME_SLEEP_MAILING_START_2:
                    markup_inline = types.InlineKeyboardMarkup()
                    item_1 = types.InlineKeyboardButton(text="Забрать подарок 🎁", callback_data = CATEGORY)
                    markup_inline.add(item_1)

                    try:
                        await bot.send_message(user_id, MAILING_MESSAGE_START_2, reply_markup=markup_inline)
                    except:
                        logger.info(f"Пользователь {user_id} заблокировал бота")
                    break

        except Exception as error:
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def mailing_message_connect_free(self, user_id):
        try:
            await asyncio.sleep(10)
            try:
                await bot.send_message(user_id, FREE_TARIFF_MAILING)
            except:
                logger.info(f"Пользователь {user_id} заблокировал бота")

        except Exception as error:
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def mailing_message_after_free(self, user_id):
        try:
            wait = 0

            while True:
                await asyncio.sleep(216)
                tariff = self.db_sql.get_tariff(user_id)

                if tariff in [COMMAND_ONE_TARIFF, COMMAND_TWO_TARIFF, COMMAND_THREE_TARIFF]:
                    break

                wait += 216
                if wait == TIME_SLEEP_MAILING_FREE:
                    markup_inline = types.InlineKeyboardMarkup()
                    item_1 = types.InlineKeyboardButton(text="SALE 🔥", url=LINK_MANAGER)
                    markup_inline.add(item_1)

                    try:
                        await bot.send_message(user_id, MAILING_MESSAGE_AFTER_FREE, reply_markup=markup_inline)
                        logger.info(f"Скинулать рассылка после бесплатного тарифа {user_id}")
                    except:
                        logger.info(f"Пользователь {user_id} заблокировал бота")
                    break

        except Exception as error:
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def mailing_message_after_payment(self, user_id):
        try:
            wait = 0

            while True:
                await asyncio.sleep(432)
                tariff = self.db_sql.get_tariff(user_id)

                if tariff in [COMMAND_ONE_TARIFF, COMMAND_TWO_TARIFF, COMMAND_THREE_TARIFF]:
                    break

                wait += 432
                if wait == TIME_SLEEP_MAILING_PAYMENT:
                    markup_inline = types.InlineKeyboardMarkup()
                    item_1 = types.InlineKeyboardButton(text="Продлить 🔥", url=LINK_MANAGER)
                    markup_inline.add(item_1)

                    try:
                        await bot.send_message(user_id, MAILING_MESSAGE_AFTER_PAYMENT, reply_markup=markup_inline)
                        logger.info(f"Скинулать рассылка после платного тарифа {user_id}")
                    except:
                        logger.info(f"Пользователь {user_id} заблокировал бота")
                    break

        except Exception as error:
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def else_answer(self, message):
        try:
            choice_text = ('Меня еще этому не научили', 'Я не знаю про что вы', 'У меня нет ответа', 'Я еще этого не умею', 'Беспонятия про что вы')
            await message.answer(choice(choice_text))
        except Exception as error:
            await message.answer(ERROR_SERVER_MESSAGE)
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def choosing_category(self, message, user_id: int):
        try:
            markup_inline = types.InlineKeyboardMarkup()
            tariff = self.db_sql.get_tariff(user_id)
            if tariff == None:
                tariff = self.db_sql.get_tariff(user_id)

            if tariff == "0" or tariff == COMMAND_FREE_TARIFF:
                status_sale = await self.db_sql.get_status_sale(user_id)
                is_free = await self.db_sql.get_is_free(user_id)

                if status_sale == 0 and is_free == 1:
                    one_tariff = types.InlineKeyboardButton(text = SALE_BUTTON_TARIF_TWO, callback_data=f'sale_tariff_{COMMAND_ONE_TARIFF}')
                    two_tariff = types.InlineKeyboardButton(text = SALE_BUTTON_TARIF_THREE, callback_data=f'sale_tariff_{COMMAND_TWO_TARIFF}')
                    three_tariff = types.InlineKeyboardButton(text = SALE_BUTTON_TARIF_FOUR, callback_data=f'sale_tariff_{COMMAND_THREE_TARIFF}')

                elif is_free == 1:
                    one_tariff = types.InlineKeyboardButton(text = BUTTON_TARIF_TWO, callback_data=f'tariff_{COMMAND_ONE_TARIFF}')
                    two_tariff = types.InlineKeyboardButton(text = BUTTON_TARIF_THREE, callback_data=f'tariff_{COMMAND_TWO_TARIFF}')
                    three_tariff = types.InlineKeyboardButton(text = BUTTON_TARIF_FOUR, callback_data=f'tariff_{COMMAND_THREE_TARIFF}')

                else:
                    free = types.InlineKeyboardButton(text=BUTTON_TARIF_ONE, callback_data=f'tariff_{COMMAND_FREE_TARIFF}')
                    one_tariff = types.InlineKeyboardButton(text = BUTTON_TARIF_TWO, callback_data=f'tariff_{COMMAND_ONE_TARIFF}')
                    two_tariff = types.InlineKeyboardButton(text = BUTTON_TARIF_THREE, callback_data=f'tariff_{COMMAND_TWO_TARIFF}')
                    three_tariff = types.InlineKeyboardButton(text = BUTTON_TARIF_FOUR, callback_data=f'tariff_{COMMAND_THREE_TARIFF}')
                    markup_inline.add(free)

                markup_inline.add(one_tariff)
                markup_inline.add(two_tariff)
                markup_inline.add(three_tariff)

                answer_message = CHOOSING_CATEGORY.replace(REPLACE_SYMBOLS, CATEGODIES[CATEGORY])
                await message.answer(answer_message, reply_markup=markup_inline)

            elif tariff in [i for i in TARIFFS.keys()]:
                answer_message = ALREADY_PURCHASED_TARIFF.replace(REPLACE_SYMBOLS, TARIFFS[tariff], 1)
                remainig_time = await self.db_sql.get_remaining_time_tariff(user_id)

                if remainig_time != -1:
                    hours = (remainig_time.seconds / 3600) + remainig_time.days * 24
                    days = hours / 24
                    remainig = int(DEADLINES_TARIFFS[tariff] - days)
                    
                    if remainig > 0:
                        if remainig in [1, 21]:
                            answer_message = answer_message.replace(REPLACE_SYMBOLS, str(remainig) + " день", 1)
                        elif remainig in [2, 3, 4, 22, 23, 24]:
                            answer_message = answer_message.replace(REPLACE_SYMBOLS, str(remainig) + " дня", 1)
                        else:
                            answer_message = answer_message.replace(REPLACE_SYMBOLS, str(remainig) + " дней", 1)
                    else:
                        remainig = int((DEADLINES_TARIFFS[tariff] * 24) - hours)
                        
                        if remainig > 0:
                            if remainig in [1, 21]:
                                answer_message = answer_message.replace(REPLACE_SYMBOLS, str(remainig) + " час", 1)
                            elif remainig in [2, 3, 4, 22, 23, 24]:
                                answer_message = answer_message.replace(REPLACE_SYMBOLS, str(remainig) + " часа", 1)
                            else:
                                answer_message = answer_message.replace(REPLACE_SYMBOLS, str(remainig) + " часов", 1)
                        else:
                            minutes = hours * 60
                            remainig = int((DEADLINES_TARIFFS[tariff] * 24 * 60) - minutes)
                            answer_message = answer_message.replace(REPLACE_SYMBOLS, str(remainig) + " минут", 1)
                else:
                    await self.send_proggrammer_error("Сколько осталось времени в тарифе")

                count_app = await self.db_sql.get_count_application(user_id)
                if type(count_app) == int:
                    answer_message = answer_message.replace(REPLACE_SYMBOLS, str(count_app-1), 1)
                else:
                    logger.error(count_app)
                    await self.func.send_proggrammer_error(count_app)

                status_pause = await self.db_sql.get_status_pause(user_id)

                if status_pause == PAUSE_SUSPEND:
                    pause_tariff = types.InlineKeyboardButton(text="Приостановить тариф", callback_data=f'start_pause')
                    markup_inline.add(pause_tariff)
                    await message.answer(answer_message + PAUSE_DESC, reply_markup=markup_inline)

                elif status_pause == PAUSE_LAUNCH:
                    pause_tariff = types.InlineKeyboardButton(text="Возобновить тариф", callback_data=f'stop_pause')
                    markup_inline.add(pause_tariff)
                    await message.answer(answer_message + PAUSE_USING, reply_markup=markup_inline)

                else:
                    await message.answer(answer_message)

            else:
                await message.answer(ERROR_SERVER_MESSAGE)
                logger.error(tariff)
                await self.send_proggrammer_error(tariff)

        except Exception as error:
            await message.answer(ERROR_SERVER_MESSAGE)
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def start_pause(self, user_id, message):
        try:
            result_cahnge = await self.db_sql.change_status_pause(user_id, PAUSE_LAUNCH)

            if result_cahnge != 1:
                await message.answer(ERROR_SERVER_MESSAGE)
                logger.error(result_cahnge)
                await self.send_proggrammer_error(result_cahnge)
            else:
                await message.answer(START_PAUSE)
                logger.info(f"Поставил тариф на паузу {user_id}")
        except Exception as error:
            await bot.send_message(user_id, ERROR_SERVER_MESSAGE)
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def stop_pause(self, user_id, message):
        try:
            result_cahnge = await self.db_sql.change_status_pause(user_id, PAUSE_USED)

            if result_cahnge != 1:
                await message.answer(ERROR_SERVER_MESSAGE)
                logger.error(result_cahnge)
                await self.send_proggrammer_error(result_cahnge)
            else:
                await message.answer(STOP_PAUSE)
                logger.info(f"Снял тариф с паузы {user_id}")
        except Exception as error:
            await bot.send_message(user_id, ERROR_SERVER_MESSAGE)
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def send_contact(self, user_id, contact):
        try:
            show_contact = await self.db_sql.get_show_contact(user_id)

            if show_contact != None and type(show_contact) == int:
                if show_contact < COUNT_SHOW_CONTACT:
                    if "http" not in contact:
                        await bot.send_message(user_id, f"Контакт - @{contact}")
                    else:
                        await bot.send_message(user_id, f"Контакт - {contact}")

                    await self.db_sql.update_show_contact(user_id)
                    await bot.send_message(user_id, f"Осталось попыток: {COUNT_SHOW_CONTACT - show_contact}")
                    
                    logger.info(f"Узнал контакт {user_id} {contact}")
                else:
                    await bot.send_message(user_id, "Вы уже использовали все попытки")
            else:
                await bot.send_message(user_id, ERROR_SERVER_MESSAGE)
                logger.error(show_contact)
                await self.send_proggrammer_error(show_contact)
                
        except Exception as error:
            await bot.send_message(user_id, ERROR_SERVER_MESSAGE)
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def support(self, message):
        try:
            markup_inline = types.InlineKeyboardMarkup()
            item_1 = types.InlineKeyboardButton(text='💬 Менеджер | Тех.поддержка', url=LINK_MANAGER)

            markup_inline.add(item_1)

            await message.answer(SUPPORT, reply_markup=markup_inline)
        except Exception as error:
            await message.answer(ERROR_SERVER_MESSAGE)
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def information(self, message):
        try:
            await message.answer(INFORMATION, parse_mode='html')
        except Exception as error:
            await message.answer(ERROR_SERVER_MESSAGE)
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def study(self, message):
        try:
            await message.answer(STUDY)
        except Exception as error:
            await message.answer(ERROR_SERVER_MESSAGE)
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def free_tariff(self, message, user_id: int):
        try:
            tariff = self.db_sql.get_tariff(user_id)
            if tariff == None:
                tariff = self.db_sql.get_tariff(user_id)

            if tariff == "0":
                is_free = await self.db_sql.get_is_free(user_id)

                if is_free == 0:
                    result_add = await self.db_sql.add_tariff(user_id, COMMAND_FREE_TARIFF)

                    if result_add == 1:
                        await message.answer(FREE_TARIFF)

                        result_update_indicator = await self.db_sql.update_indicators('free')
                        if result_update_indicator != 1:
                            logger.error(result_update_indicator)
                            await self.send_proggrammer_error(result_update_indicator)

                        logger.info(f"Подключил тариф {COMMAND_FREE_TARIFF} {user_id}")
                        try:
                            username = await self.db_sql.get_username_by_id(user_id)
                            if username != 0 and username != "None":
                                for i in admins:
                                    await bot.send_message(i, f"Подключил тариф {COMMAND_FREE_TARIFF} @{username}")
                            else:
                                for i in admins:
                                    await bot.send_message(i, f"Подключил тариф {COMMAND_FREE_TARIFF} {user_id}")
                        except:
                            pass

                        await asyncio.create_task(self.mailing_message_connect_free(user_id))
                    else:
                        await message.answer(ERROR_SERVER_MESSAGE)
                        await self.send_proggrammer_error(result_add)
                            

                elif is_free == 1:
                    await message.answer(ALREADY_USED_FREE)

                else:
                    await message.answer(ERROR_SERVER_MESSAGE)
                    logger.error(is_free)
                    await self.send_proggrammer_error(is_free)  

            elif tariff == COMMAND_FREE_TARIFF:
                remainig_time = await self.db_sql.get_remaining_time_tariff(user_id)
                answer_message = ALREADY_USING_FREE

                if remainig_time != -1:
                    hours = remainig_time.seconds / 3600
                    remainig = int(FREE_TERM - hours)
                    
                    if remainig > 0:
                        if remainig == 1:
                            answer_message = answer_message.replace(REPLACE_SYMBOLS, str(remainig) + " час", 1)
                        elif remainig in [2, 3, 4]:
                            answer_message = answer_message.replace(REPLACE_SYMBOLS, str(remainig) + " часа", 1)
                        else:
                            answer_message = answer_message.replace(REPLACE_SYMBOLS, str(remainig) + " часов", 1)
                    else:
                        minutes = remainig_time.seconds / 60
                        remainig = int((FREE_TERM * 60) - minutes)
                        answer_message = answer_message.replace(REPLACE_SYMBOLS, str(remainig) + " минут", 1)
                else:
                    logger.error(remainig_time)
                    await self.send_proggrammer_error(remainig_time)

                await message.answer(answer_message)

            else:
                await message.answer(ERROR_SERVER_MESSAGE)
                logger.error(tariff)
                await self.send_proggrammer_error(tariff)

        except Exception as error:
            await message.answer(ERROR_SERVER_MESSAGE)
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def paid_tariff(self, choice_tariff: str, message, user_id: int, status_sale: int):
        try:
            comment = str(user_id) + "_" + str(randint(1000, 9999))
            markup_inline = types.InlineKeyboardMarkup()

            if status_sale == 0:
                bill = p2p.bill(amount=PRICES[choice_tariff], lifetime=10, comment=comment)
                pay_in_bot = types.InlineKeyboardButton(text=BUTTON_PAYMENT_ONE, url=bill.pay_url)
                pay_manager = types.InlineKeyboardButton(text=BUTTON_PAYMENT_TWO, url=LINK_MANAGER)
                markup_inline.add(pay_in_bot)
                markup_inline.add(pay_manager)
                
            elif status_sale == 1:
                bill = p2p.bill(amount=SALE_PRICES[choice_tariff], lifetime=10, comment=comment)
                pay_in_bot = types.InlineKeyboardButton(text=BUTTON_PAYMENT_ONE, url=bill.pay_url)
                markup_inline.add(pay_in_bot)                

            await message.answer(PAID_TARIFF, reply_markup=markup_inline)
            await asyncio.create_task(self.check_payment(user_id, bill.bill_id, choice_tariff, status_sale))

        except Exception as error:
            logger.error(error)
            await message.answer(ERROR_SERVER_MESSAGE)


    async def check_payment(self, user_id, bill_id, tariff, status_sale):
        try:
            wait = 0
            while True:
                await asyncio.sleep(2)
                status = p2p.check(bill_id=bill_id).status
                
                if status == "PAID":
                    await self.enabling_tariff(user_id, tariff, status_sale)

                    if status_sale == 1:
                        await self.db_sql.change_status_sale(user_id)
                        
                    break

                wait += 1
                if wait == 300:
                    break
        except Exception as error:
            logger.error(error)


    async def enabling_tariff(self, user_id: int, tariff: str, sale: int):
        try:
            await bot.send_message(user_id, ENABLING_TARIFF)
            if sale == 0:
                money = PRICES[tariff]
                indicator = TARIFFS_INDICATORS[tariff]
            else:
                money = SALE_PRICES[tariff]
                indicator = f"{TARIFFS_INDICATORS[tariff]}_sale"

            # Добавление тарифа в БД и изменение статуса бесплатного тарифа
            result_change = await self.db_sql.change_is_free(user_id)
            result_add = await self.db_sql.add_tariff(user_id, tariff)
            if result_add != 1 or result_change != 1:
                await bot.send_message(user_id, ERROR_SERVER_MESSAGE)
                await self.send_proggrammer_error(result_add)
                logger.error(f'[{user_id} {tariff}]: {result_add} {result_change}')

            # Обновление индикатора тарифа
            result_update_indicator = await self.db_sql.update_indicators(indicator)
            if result_update_indicator != 1:
                logger.error(result_update_indicator)
                await self.send_proggrammer_error(result_update_indicator)

            # Обновление индикатора прибыли
            result_update_income = await self.db_sql.update_income_indicator(money)
            if result_update_income != 1:
                logger.error(result_update_income)
                await self.send_proggrammer_error(result_update_income)

            # Получение статуса покупки тарифа ранее
            status_pay = await self.db_sql.get_status_pay(user_id)
            if status_pay == None:
                status_pay = await self.db_sql.get_status_pay(user_id)

            if status_pay == 0:
                # Обновление статуса покупки
                result_update_status_pay = await self.db_sql.update_status_pay(user_id)
                if result_update_status_pay != 1:
                    logger.error(result_update_status_pay)
                    await self.send_proggrammer_error(result_update_status_pay)
            elif status_pay == 1:
                # Обновление индикатора повторной покупки тарифа
                result_update_indicator = await self.db_sql.update_indicators('again_pay')
                if result_update_indicator != 1:
                    logger.error(result_update_indicator)
                    await self.send_proggrammer_error(result_update_indicator)
            else:
                logger.error(status_pay)
                await self.send_proggrammer_error(status_pay)

            try:
                username = await self.db_sql.get_username_by_id(user_id)
                if username != 0 and username != "None":
                    for i in admins:
                        await bot.send_message(i, f"Куплен тариф {TARIFFS[tariff]} @{username}")
                else:
                    for i in admins:
                        await bot.send_message(i, f"Куплен тариф {TARIFFS[tariff]} {user_id}")

                logger.info(f"Куплен тариф {tariff} {user_id}")
            except:
                pass
        except Exception as error:
            await bot.send_message(user_id, ERROR_SERVER_MESSAGE)
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def check_size_log(self):
        try:
            size_log = os.path.getsize(PATH_TO_LOGS) / 1024

            if size_log >= 1000:
                await self.send_logs()
        except Exception as error:
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def check_time_tariff(self):
        try:
            loop_ = asyncio.get_event_loop()

            while True:
                await asyncio.sleep(TIME_SLEEP_CHECK_TARIFFS)
                await self.check_size_log()
                datetime_now = datetime.now()

                users_time = await self.db_sql.get_time_tariff_users()

                if type(users_time) == list:
                    for user in users_time:
                        time_delta = datetime_now - user[2]
                        days = time_delta.days
                        hours = time_delta.seconds / 3600

                        if user[1] == COMMAND_FREE_TARIFF:
                            hours = hours + days*24

                            if hours >= FREE_TERM:
                                await self.db_sql.stop_tariff(user[0])
                                await self.db_sql.change_is_free(user[0])

                                count_app = await self.db_sql.get_count_application(user[0])

                                if type(count_app) == int:
                                    message_answer = ENDED_FREE_TARIFF.replace(REPLACE_SYMBOLS, str(count_app-1), 1)
                                else:
                                    logger.error(count_app)
                                    await self.func.send_proggrammer_error(count_app)

                                try:
                                    markup_inline = types.InlineKeyboardMarkup()
                                    item_1 = types.InlineKeyboardButton(text="Воспользоваться ✅ ", callback_data=CATEGORY)
                                    markup_inline.add(item_1)

                                    await bot.send_message(user[0], message_answer, reply_markup=markup_inline)
                                    
                                    username = await self.db_sql.get_username_by_id(user[0])
                                    if username != 0 and username != "None":
                                        logger.info(f"Закончился бесплатный тариф @{user[0]}")
                                        for admin in admins:
                                            await bot.send_message(admin, f"<b>Закончился бесплатный тариф у @{username}</b>", parse_mode="html")
                                    else:
                                        logger.info(f"Закончился бесплатный тариф @{user[0]}")
                                        for admin in admins:
                                            await bot.send_message(admin, f"<b>Закончился бесплатный тариф у {user[0]}</b>", parse_mode="html")

                                    loop_.create_task(self.mailing_message_after_free(user[0]))
                                except:
                                    pass

                        else:
                            if days == (DEADLINES_TARIFFS[user[1]] - 1) and int(hours) == 0:
                                await bot.send_message(user[0], END_WARNING_PAYMENT_TARIFF)

                            if days >= DEADLINES_TARIFFS[user[1]]:
                                await self.db_sql.stop_tariff(user[0])

                                try:
                                    count_app = await self.db_sql.get_count_application(user[0])

                                    if type(count_app) == int:
                                        answer_message = STOP_TARIFF.replace(REPLACE_SYMBOLS, str(count_app-1), 1)
                                    else:
                                        logger.error(count_app)
                                        await self.func.send_proggrammer_error(count_app)

                                    await bot.send_message(user[0], answer_message)

                                    username = await self.db_sql.get_username_by_id(user[0])
                                    if username != 0 and username != "None":
                                        logger.info(f"Закончился тариф {user[1]} @{username}")
                                        for admin in admins:
                                            await bot.send_message(admin, f"<b>Закончился тариф {TARIFFS[user[1]]} у @{username}</b>", parse_mode="html")
                                    else:
                                        logger.info(f"Закончился тариф {user[1]} {user[0]}")
                                        for admin in admins:
                                            await bot.send_message(admin, f"<b>Закончился тариф {TARIFFS[user[1]]} у {user[0]}</b>", parse_mode="html")

                                    loop_.create_task(self.mailing_message_after_payment(user[0]))
                                except:
                                    pass

                else:
                    logger.error(users_time)
                    await self.send_proggrammer_error(users_time)

        except Exception as error:
            logger.error(error)
            await self.send_proggrammer_error(error)

    
    async def contact_spam(self, user_id, contact, tariff):
        try:
            result_add = await self.db_sql.add_spam_contact(user_id, contact)

            if result_add == -1:
                await bot.send_message(user_id, f"Контакт @{contact} уже был добавлен в спам")
            else:
                if result_add != 1:
                    await self.send_proggrammer_error(result_add)

                if tariff == "pay":
                    await bot.send_message(user_id, f"Контакт @{contact} отправлен в спам")
                elif tariff == "free":
                    await bot.send_message(user_id, "Контакт @***** отправлен в спам")

                logger.info(f"@{contact} отправлен в спам {user_id}")
        except Exception as error:
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def add_tariff_user_panel(self, username: str, tariff: str, sale: str):
        try:
            if "@" in username:
                username = username.replace("@", "")

            user_id = await self.db_sql.get_user_id_username(username)
            await self.enabling_tariff(user_id, tariff, int(sale))
        except Exception as error:
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def statistic(self, message):
        try:
            count_users = await self.db_sql.get_count_users()
            if count_users == None:
                count_users = await self.db_sql.get_count_users()

            count_users_subscribes_free = await self.db_sql.get_count_subscribe_free_users()
            if count_users_subscribes_free == None:
                count_users_subscribes_free = await self.db_sql.get_count_subscribe_free_users()

            count_users_payment = await self.db_sql.get_count_payment_users()
            if count_users_payment == None:
                count_users_payment = await self.db_sql.get_count_payment_users()

            count_unused_users = None
            if count_users != None and count_users_subscribes_free != None and count_users_payment != None:
                count_unused_users = count_users - count_users_subscribes_free - count_users_payment

            sattistic_message = STATISTIC

            if type(count_users) == int:
                sattistic_message = sattistic_message.replace(REPLACE_SYMBOLS, str(count_users), 1)
            else:
                logger.error(count_users)
                await self.send_proggrammer_error(count_users)

            if type(count_users_subscribes_free) == int:
                sattistic_message = sattistic_message.replace(REPLACE_SYMBOLS_1, str(count_users_subscribes_free), 1)
            else:
                logger.error(count_users_subscribes_free)
                await self.send_proggrammer_error(count_users)

            if type(count_users_payment) == int:
                sattistic_message = sattistic_message.replace(REPLACE_SYMBOLS_2, str(count_users_payment), 1)
            else:
                logger.error(count_users_payment)
                await self.send_proggrammer_error(count_users)

            if count_unused_users != None:
                sattistic_message = sattistic_message.replace(REPLACE_SYMBOLS_3, str(count_unused_users), 1)
            else:
                logger.error(count_unused_users)
                await self.send_proggrammer_error(count_users)
            
            await message.answer(sattistic_message, parse_mode='html')
        except Exception as error:
            await message.answer(ERROR_SERVER_MESSAGE)
            await message.answer(TRY_AGAIN)
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def get_count_memers_channel(self, channel: str) -> int:
        try:
            url = f"https://t.me/{channel}"

            response = requests.get(url)
            html = BS(response.content, 'html.parser')

            for el in html.select('.tgme_page'):
                count_ = el.select('.tgme_page_extra')[0].text

            return int(count_.split()[0])
        except Exception as error:
            logger.error(error)
            await self.send_proggrammer_error(error)
            return -1


    async def indicators(self, message):
        try:
            answer_message = INDICATORS
            main_count = 0

            # Получение общего числа людей в каналах
            for channel in CHANNELS_INVITING:
                count_users = await self.get_count_memers_channel(channel)
                if count_users != -1:
                    main_count += count_users

            list_indicators = await self.db_sql.get_indecators()
            if list_indicators != None and len(list_indicators) != 0:
                list_indicators = list_indicators[0]

                # Определение конверсии в бесплатную подписку
                count_users_free = list_indicators[0]
                conversion_free = (count_users_free / main_count) * 100
                conversion_free = float(f"{conversion_free:.2f}")
                answer_message = answer_message.replace(REPLACE_SYMBOLS, f"{str(conversion_free)}%", 1)

                # Определение конверсии в платную подписку
                count_users_pay = 0
                for i in list_indicators[2:-2]:
                    count_users_pay += i
                
                if count_users_free != 0:
                    conversion_pay = (count_users_pay / count_users_free) * 100
                    conversion_pay = float(f"{conversion_pay:.2f}")
                else:
                    conversion_pay = float(count_users_pay * 100)
                answer_message = answer_message.replace(REPLACE_SYMBOLS, f"{str(conversion_pay)}%", 1)

                # Определение конверсии в повторную покупку
                count_users_again_pay = list_indicators[1]
                if count_users_pay != 0:
                    conversion_again_pay = (count_users_again_pay / count_users_pay) * 100
                    conversion_again_pay = float(f"{conversion_again_pay:.2f}")
                else:
                    conversion_again_pay = float(count_users_again_pay * 100)
                answer_message = answer_message.replace(REPLACE_SYMBOLS, f"{str(conversion_again_pay)}%", 1)

                # Определение ЕПЦ
                income = list_indicators[8]
                epc = income / main_count
                epc = float(f"{epc:.2f}")
                answer_message = answer_message.replace(REPLACE_SYMBOLS, f"{str(epc)}₽", 1)

                # Добавление данных по приобретенным тарифам
                answer_message = answer_message.replace(REPLACE_SYMBOLS_1, str(count_users_free), 1)
                answer_message = answer_message.replace(REPLACE_SYMBOLS_1, str(list_indicators[2]), 1)
                answer_message = answer_message.replace(REPLACE_SYMBOLS_1, str(list_indicators[3]), 1)
                answer_message = answer_message.replace(REPLACE_SYMBOLS_2, str(list_indicators[4]), 1)
                answer_message = answer_message.replace(REPLACE_SYMBOLS_2, str(list_indicators[5]), 1)
                answer_message = answer_message.replace(REPLACE_SYMBOLS_3, str(list_indicators[6]), 1)
                answer_message = answer_message.replace(REPLACE_SYMBOLS_3, str(list_indicators[7]), 1)
                
                answer_message = answer_message.replace(REPLACE_SYMBOLS, str(income), 1)

                target_income = list_indicators[9]
                if target_income != 0:
                    percent = (income / target_income) * 100
                    percent = float(f"{percent:.2f}")
                    message_target_income = TARGET_INCOME.replace(REPLACE_SYMBOLS, str(percent), 1)

                    answer_message += message_target_income

            markup_inline = types.InlineKeyboardMarkup()
            add_target = types.InlineKeyboardButton(text='Добавить/изменить цель', callback_data="add_target")

            markup_inline.add(add_target)
            await message.answer(answer_message, reply_markup=markup_inline, parse_mode='html')

        except Exception as error:
            await message.answer(ERROR_SERVER_MESSAGE)
            await message.answer(TRY_AGAIN)
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def add_new_target(self, message, new_target):
        try:
            result_update = await self.db_sql.update_tager_income(new_target)
            
            if result_update != 1:
                await message.answer(ERROR_SERVER_MESSAGE)
                logger.error(result_update)
                await self.send_proggrammer_error(result_update)
            else:
                await message.answer("Цель успешно установлена")
        except Exception as error:
            await message.answer(ERROR_SERVER_MESSAGE)
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def mailing(self, message_text, whom, user_id):
        try:
            users = await self.db_sql.get_id_users(whom)
            
            for user in users:
                try:
                    await bot.send_message(user[0], message_text)
                    logger.info(f"Рассылка {user_id[0]}")
                except:
                    pass

            await bot.send_message(user_id, f"Рассылка {len(users)} пользователям прошла успешно")
            logger.info(f"Рассылка {len(users)} пользователям прошла успешно")
        except Exception as error:
            await bot.send_message(user_id, ERROR_SERVER_MESSAGE)
            logger.error(error)
            await self.send_proggrammer_error(error)


    async def add_spam(self, username, message):
        try:
            result_add = await self.db_sql.add_spam(username)

            if result_add != 1:
                await message.answer(ERROR_SERVER_MESSAGE)
                logger.error(result_add)
                await bot.send_message(PROGRAMMER_ID, result_add)
            else:
                await message.answer(f"Пользователь @{username} добавлен в спам")
                logger.info(f"Пользователь @{username} добавлен в спам")
        except Exception as error:
            await message.answer(ERROR_SERVER_MESSAGE)
            logger.error(error)
            await bot.send_message(PROGRAMMER_ID, error)


    async def send_logs(self):
        try:
            await bot.send_document(PROGRAMMER_ID, open(PATH_TO_LOGS, 'rb'))

            with open(PATH_TO_LOGS, 'w') as log:
                log.write("[INFO] Logs was send and clean\n")
        except Exception as error:
            logger.error(error)
            await bot.send_message(PROGRAMMER_ID, error)


    async def send_proggrammer_error(self, error):
        try:
            message_error = f"[ERROR] {error}"
            await bot.send_message(PROGRAMMER_ID, message_error)
            await bot.send_document(PROGRAMMER_ID, open(PATH_TO_LOGS, 'rb'))
        except Exception as error:
            logger.error(error)