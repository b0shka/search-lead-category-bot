from aiogram import types
from aiogram.dispatcher import FSMContext
from Requests.functions import FunctionsBot
from Variables.config import PROGRAMMER_ID, dp, logger, bot
from Variables.error_messages import *
from Variables.text_messages import *
from Variables.form import Form


func = FunctionsBot()


@dp.message_handler(state=Form.username_tariff_category)
async def answer_q(message: types.Message, state: FSMContext):
    try:
        username, tariff, sale = message.text.lower().split("|")
        await func.add_tariff_user_panel(username, tariff, sale)
    except ValueError:
        await message.answer("Вы неправильно ввели данные")

    await state.finish()


@dp.message_handler(state=Form.spam)
async def answer_q(message: types.Message, state: FSMContext):
    try:
        username = message.text
        if "@" in username:
            username = username.replace("@", "")

        await func.add_spam(username, message)
        
    except Exception as error:
        logger.error(error)
        await message.answer(ERROR_SERVER_MESSAGE)
        await func.send_proggrammer_error(error)

    await state.finish()


@dp.message_handler(state=Form.mailing)
async def answer_q(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        message_text = message.text
        await func.mailing(message_text, data['whom'], message.from_user.id)
    except Exception as error:
        logger.error(error)
        await message.answer(ERROR_SERVER_MESSAGE)
        await func.send_proggrammer_error(error)

    await state.finish()


@dp.callback_query_handler(lambda call: True, state="*")
async def callback(call: types.CallbackQuery, state:FSMContext):
    try:
        if call.data == CATEGORY:
            await func.choosing_category(call.message, call.from_user.id)

        elif 'tariff' in call.data and "add" not in call.data:
            user_id = call.from_user.id

            if COMMAND_FREE_TARIFF in call.data:
                await func.free_tariff(call.message, user_id)

            if "sale" in call.data:
                if COMMAND_ONE_TARIFF in call.data:
                    await func.paid_tariff(COMMAND_ONE_TARIFF, call.message, user_id, 1)

                elif COMMAND_TWO_TARIFF in call.data:
                    await func.paid_tariff(COMMAND_TWO_TARIFF, call.message, user_id, 1)

                elif COMMAND_THREE_TARIFF in call.data:
                    await func.paid_tariff(COMMAND_THREE_TARIFF, call.message, user_id, 1)

            else:
                if COMMAND_ONE_TARIFF in call.data:
                    await func.paid_tariff(COMMAND_ONE_TARIFF, call.message, user_id, 0)

                elif COMMAND_TWO_TARIFF in call.data:
                    await func.paid_tariff(COMMAND_TWO_TARIFF, call.message, user_id, 0)

                elif COMMAND_THREE_TARIFF in call.data:
                    await func.paid_tariff(COMMAND_THREE_TARIFF, call.message, user_id, 0)

        elif "pause" in call.data:
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            
            if call.data == "start_pause":
                await func.start_pause(call.from_user.id, call.message)

            elif call.data == "stop_pause":
                await func.stop_pause(call.from_user.id, call.message)

        elif "get_contact" in call.data:
            contact = call.data.replace("get_contact_", "")
            await func.send_contact(call.from_user.id, contact)

        elif call.data == 'statistic':
            await func.statistic(call.message)
            
        elif call.data == 'indicators':
            await func.indicators(call.message)

        elif "mailing" in call.data:
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

            if call.data == "mailing":
                markup_inline = types.InlineKeyboardMarkup()

                without_tariff = types.InlineKeyboardButton(text='Без тарифа', callback_data = 'mailing_without')
                free_tariff = types.InlineKeyboardButton(text='Бесплатный тариф', callback_data = 'mailing_free')
                pay_tariff = types.InlineKeyboardButton(text='Платный тариф', callback_data = 'mailing_pay')
                all_users = types.InlineKeyboardButton(text='Всем пользователям', callback_data = 'mailing_all_users')

                markup_inline.add(without_tariff)
                markup_inline.add(free_tariff)
                markup_inline.add(pay_tariff)
                markup_inline.add(all_users)
                await call.message.answer('Выберите кому делать рассылку', reply_markup=markup_inline)

            else:
                await state.update_data(whom=call.data)
                await bot.send_message(call.from_user.id, "Введите сообщение для рассылки")
                await Form.mailing.set()

        elif call.data == 'logs':
            user_id = call.from_user.id

            if user_id == PROGRAMMER_ID:
                await func.send_logs()
            else:
                await bot.send_message(user_id, "Для вас эта функция ограничена")

        elif call.data == "add_tariff":
            await bot.send_message(call.from_user.id, "Введите команду типа: username|tariff|sale")
            await Form.username_tariff_category.set()

        elif "spam" in call.data:
            if call.data == "add_spam":
                await bot.send_message(call.from_user.id, "Введите username")
                await Form.spam.set()
            else:
                user_id = call.from_user.id
                data_callback = call.data.split("_")
                tariff = data_callback[0]
                contact = call.data.replace(f"{tariff}_spam_", "")

                if "https://t.me/" in contact:
                    contact = contact.replace("https://t.me/", "", 1)
                elif "t.me/" in contact:
                    contact = contact.replace("t.me/", "", 1)

                contact = contact.replace("@", "", 1)
                await func.contact_spam(user_id, contact, tariff)

    except Exception as error:
        await call.message.answer(ERROR_SERVER_MESSAGE)
        logger.error(error)
        await func.send_proggrammer_error(error)