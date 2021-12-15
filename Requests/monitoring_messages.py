import asyncio
import pymorphy2
from aiogram import types
from telethon.sync import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
from Variables.config import bot, logger
from Variables.text_messages import *
from Variables.monitoring import *
from Databases.database_sql import DatabaseSQL
from Requests.functions import FunctionsBot


class MonitoringChats:

    def __init__(self):
        try:
            self.db_sql = DatabaseSQL()
            self.func = FunctionsBot()
        except Exception as error:
            logger.error(error)


    async def get_messages_channel(self, message_text, channel):
        try:
            if channel == 'rueventjob' and "(#удаленка)" in message_text.lower():
                list_messages = message_text.split('\n\n')[1:]
                return list_messages

            if channel == 'reklamodromo' and "ВАКАНСИИ" in message_text:
                list_messages = message_text.split("ВАКАНСИИ")[1]
                list_messages = list_messages.split('➖➖➖➖➖➖➖')[:-1]
                return list_messages

            if channel == "workzavr":
                list_messages = message_text.split("\n\n")[:-1]
                return list_messages

            if channel in ["fr_works", "recruit_jobs", "workers_job"]:
                list_messages = message_text.split("➖➖➖➖➖➖➖")[:-1]
                return list_messages

            if channel == "workspaced" and "➖➖➖➖➖➖" in message_text:
                list_messages = message_text.split("➖➖➖➖➖➖")
                return list_messages

            if channel in ["remote_ru"] and "откликнуться:" in message_text.lower():
                return [message_text]

            if channel in ["distantsiya", "lead_get_target", "goodpeople_pro", "traficmaker_channel", "rabota_go", "vacanciesrus", "workfromhomeforfun", "digitalworkr", "seejobplus", "dnative_job", "testgroupinvite", "testgroupinvite1"]:
                return [message_text]

            if channel == "jobosphere":
                if "#резюме" in message_text:
                    list_messages = message_text.split("\n—")[:-1]
                    return list_messages
                else:
                    return [message_text]

            if channel in ["ispolnytel"] and "#помогу" not in message_text:
                if "➖➖➖➖➖➖" in message_text:
                    list_messages = message_text.split("➖➖➖➖➖➖")
                    return list_messages
                else:
                    return [message_text]

            if (channel in LIST_GROUP or channel in ["freelance_vip"]) and "#ищу" in message_text.lower() and "#помогу" not in message_text.lower() and "#ищуработу" not in message_text.lower():
                return [message_text]

            return []

        except Exception as error:
            logger.error(error)
            await self.func.send_proggrammer_error(error)
            return []


    async def determinate_catorory(self, message_text):
        try:
            categories = []
            morph = pymorphy2.MorphAnalyzer()

            symbols_replace_space = ['?', '!', '.', '-', '/', "#"]
            symbols_replace_nothing = [',', '(', ')']

            for i in symbols_replace_space:
                message_text = message_text.replace(i, ' ')

            for i in symbols_replace_nothing:
                message_text = message_text.replace(i, '')

            words = message_text.lower().split()[:10]

            for phrases in advertisement:
                if phrases in message_text.lower():
                    return []

            for i in words:
                p = morph.parse(i.replace("\u200b", ""))[0]
                
                if p.normal_form in no:
                    return []

                elif p.normal_form in globals()[CATEGORY]:
                    categories.append(CATEGORY)

                for word in globals()[f'{CATEGORY}_phrases']:
                    if word in message_text.lower():
                        categories.append(CATEGORY)

            return categories

        except Exception as error:
            logger.error(error)
            await self.func.send_proggrammer_error(error)
            return []


    async def get_contact_group(self, client, channel, message_text: dict):
        try:
            contact = ""

            if channel in LIST_GROUP:
                if message_text['reply_markup'] != None:
                    try:
                        contact = message_text['reply_markup']['rows'][0]['buttons'][0]['url']
                    except:
                        contact = ""

                elif message_text['reply_markup'] == None:
                    try:
                        #user_id = message_text['fwd_from']['from_id']['user_id']
                        user_id = message_text['from_id']['user_id']
                  
                        contact = await client.get_entity(user_id)
                        contact = contact.to_dict()['username']
                        if contact != None:
                            try:
                                contact = contact.replace(" ", "")
                            except:
                                pass
                        else:
                            contact = ""
                    except:
                        contact = ""

            return contact
        except Exception as error:
            logger.error(error)
            await self.func.send_proggrammer_error(error)
            return ""


    async def get_contact_channel(self, message_text: str):       
        try:
            contact = ""
            list_contacts = []

            for i in message_text.split():
                if "@" in i or "https://" in i or "http://" in i or 't.me/' in i:
                    i = i.replace(",", "")
                    if "@" in i and i[0] == "@":
                        i = i.replace(".", "")
                    list_contacts.append(i)

            if len(list_contacts) != 0:
                for i in list_contacts:
                    if i[0] == "@" or 't.me/' in i:
                        contact = i.replace("@", "")
                        break

                if contact == "":
                    for i in list_contacts:
                        if "@" in i:
                            contact = i

                    if contact == "":
                        contact = list_contacts[-1]

            return contact, list_contacts
        except Exception as error:
            logger.error(error)
            await self.func.send_proggrammer_error(error)
            return ""
            

    async def check_username(self, client, username):
        try:
            if "http" in username or "@" in username:
                return 1
            try:
                await client(GetFullUserRequest(username))
                return 1
            except:
                return 0
        except Exception as error:
            logger.error(error)
            await self.func.send_proggrammer_error(error)
            return 0


    async def check_contact_black_list_user(self, user_id, contact):
        try:
            if "https://t.me/" in contact:
                contact = contact.replace("https://t.me/", "", 1)
            elif "t.me/" in contact:
                contact = contact.replace("t.me/", "", 1)

            contact = contact.replace("@", "", 1)
            black_list = await self.db_sql.get_black_list_user(user_id)

            if ";" in black_list:
                if contact in black_list.split(";"):
                    return 1
            else:
                return 0
        except Exception as error:
            logger.error(error)
            await self.func.send_proggrammer_error(error)
            return 0


    async def send_application(self, users_tariff, msg, contact, list_contacts, channel_id):
        try:
            for user in users_tariff.keys():
                result_ckeck_contact_block = await self.check_contact_black_list_user(user, contact)
                count_replay = await self.db_sql.check_contact_replay(contact, user, msg)

                if count_replay == 0 and not result_ckeck_contact_block:
                    result_add = await self.db_sql.add_application(user, channel_id, contact, msg)
                    if result_add != 1:
                        logger.error(result_add)
                        await self.func.send_proggrammer_error(result_add)

                    answer_message = APPLICATION.replace(REPLACE_SYMBOLS_2, CATEGODIES[CATEGORY], 1)
                    count_app = await self.db_sql.get_count_application(user)

                    if type(count_app) == int:
                        markup_inline = types.InlineKeyboardMarkup()
                        result_update_count_app = await self.db_sql.update_count_application(user, count_app)

                        if result_update_count_app != 1:
                            logger.error(result_update_count_app)
                            await self.func.send_proggrammer_error(result_update_count_app)

                        answer_message = answer_message.replace(REPLACE_SYMBOLS_1, str(count_app), 1)
                        answer_message = answer_message.rstrip()

                        if users_tariff[user] in [i for i in TARIFFS.keys()]:
                            if "http://" not in contact and "@" not in contact:
                                if ("https://" in contact and "t.me/" in contact) or ("https://" not in contact):
                                    answer_message = answer_message.replace(REPLACE_SYMBOLS, msg, 1)

                                    if "https://" not in contact:
                                        if "t.me/" in contact:
                                            contact = f"https://{contact}"
                                        elif "http://" in contact:
                                            pass
                                        else:
                                            contact = f"https://t.me/{contact}"

                                    contact_btn = types.InlineKeyboardButton(text="Написать заказчику", url=contact)
                                    spam = types.InlineKeyboardButton(text="Отправить в спам ❌", callback_data=f'pay_spam_{contact}')

                                    markup_inline.add(contact_btn)
                                    markup_inline.add(spam)
                                    try:
                                        await bot.send_message(user, answer_message, reply_markup=markup_inline, disable_web_page_preview=True, parse_mode='html')
                                    except Exception as error:
                                        logger.error(f"{error} {user}")

                        else:
                            if contact not in msg:
                                answer_message += HIDE_CONTACT
                            else:
                                msg = msg.replace(contact, "*****")

                            for contact_message in list_contacts:
                                try:
                                    msg = msg.replace(contact_message, "")
                                except:
                                    pass
                            answer_message = answer_message.replace(REPLACE_SYMBOLS, msg, 1)
                            answer_message += APPLICATION_FREE

                            spam = types.InlineKeyboardButton(text="Отправить в спам ❌", callback_data=f'free_spam_{contact}')
                            markup_inline.add(spam)

                            try:
                                await bot.send_message(user, answer_message, disable_web_page_preview=True, parse_mode='html', reply_markup=markup_inline)
                            except Exception as error:
                                logger.error(f"{error} {user}")

                        logger.info(f"Отправилось {user} {users_tariff[user]}")
                    else:
                        logger.error(count_app)
                        await self.func.send_proggrammer_error(count_app)

                elif result_ckeck_contact_block == 1:
                    logger.info(f"Конакт {contact} в черном списке у пользователя {user}")

                elif count_replay != 0:
                    logger.info(f"Пойман повтор {contact} {user}")
        except Exception as error:
            logger.error(error)
            await self.func.send_proggrammer_error(error)


    async def monitoring_channels(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            client = TelegramClient(NAME_SESSION, API_ID, API_HASH)
            
            @client.on(events.NewMessage(chats=CHANNELS))
            async def handler(event):
                try:
                    await asyncio.sleep(TIME_SLEEP_CHECK_CHANNELS)
                    message_text = event.message.to_dict()
                    channel_id = 0

                    try:
                        channel_id = message_text['peer_id']['channel_id']
                        #channel_id = message_text['fwd_from']['from_id']['channel_id']
                    except Exception as error:
                        logger.error(error)

                    if channel_id in [i for i in CHANNELS_ID.keys()]:
                        channel = CHANNELS_ID[channel_id]
                        list_messages = await self.get_messages_channel(message_text['message'], channel)
                        
                        for message in list_messages:
                            if channel in 'rueventjob':
                                try:
                                    message = message.replace("  ", " ")
                                    message = message.replace(". #", "")[1:]
                                except:
                                    pass

                            if channel in ["reklamodromo", "fr_works", "workspaced", "recruit_jobs", "workers_job", "ispolnytel"]:
                                try:
                                    message = message.replace("➖", "")
                                    message = message.replace("\n\n", "\n", 1)
                                except:
                                    pass

                            categories = await self.determinate_catorory(message)

                            if categories != []:                                
                                if channel in LIST_GROUP:
                                    contact = await self.get_contact_group(client, channel, message_text)
                                    _, list_contacts = await self.get_contact_channel(message)

                                elif channel in LIST_CHANNELS:
                                    contact, list_contacts = await self.get_contact_channel(message)

                                if contact != "":
                                    result_check_contact = await self.check_username(client, contact)
                                    result_ckeck_contact_block = await self.db_sql.check_contact_in_black_list(contact)

                                    if result_check_contact and not result_ckeck_contact_block:
                                        users_tariff = {}

                                        tariff = await self.db_sql.get_users_tariff()

                                        if tariff != [] and type(tariff) == list:
                                            for j in tariff:
                                                users_tariff[j[0]] = j[1]

                                        await self.send_application(users_tariff, message, contact, list_contacts, channel_id)

                                    elif result_ckeck_contact_block == 1:
                                        logger.info(f"Конакт @{contact} в черном списке")

                except Exception as error:
                    logger.error(error)
                    await self.func.send_proggrammer_error(error)
            
            await client.start()
            await client.run_until_disconnected()

        except Exception as error:
            logger.error(error)
            await self.func.send_proggrammer_error(error)