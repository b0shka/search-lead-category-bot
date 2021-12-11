import asyncio
import time
from aiogram import executor, types
from Variables.config import *
from Variables.text_messages import *
from Databases.database_sql import DatabaseSQL
from Requests.monitoring_messages import MonitoringChats
from Requests.requests_bot import RequestsBot
from Requests.functions import FunctionsBot


db_sql = DatabaseSQL()
req_bot = RequestsBot()
func = FunctionsBot()
monitoring = MonitoringChats()


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
	try:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		support = types.KeyboardButton('💬 Поддержка')
		information = types.KeyboardButton('📚 Информация')
		about_tariffs = types.KeyboardButton('🗒 Тарифы')
		markup.add(information, support)
		markup.add(about_tariffs)

		await message.answer(start_message_1, reply_markup=markup)
		time.sleep(5)

		photo = open(PATH_TO_IMG, 'rb')
		await bot.send_photo(message.from_user.id, photo)
		time.sleep(5)

		markup_inline = types.InlineKeyboardMarkup()
		start_get = types.InlineKeyboardButton(text='Начать получать заказы ✅', callback_data=CATEGORY)
		markup_inline.add(start_get)
		await message.answer(start_message_2, reply_markup=markup_inline)

		user = get_data_user(message)
		if user != 0:
			result_add = await db_sql.add_user(user)
			if result_add != 1:
				await func.send_proggrammer_error(result_add)
			await asyncio.create_task(func.mailing_message_start(message.from_user.id))
	except Exception as error:
		logger.error(error)
		await func.send_proggrammer_error(error)


@dp.message_handler(commands=['tariff'])
async def category(message: types.Message):
	try:
		await func.choosing_category(message, message.from_user.id)

		user = get_data_user(message)
		if user != 0:
			result_add = await db_sql.add_user(user)
			if result_add != 1:
				await func.send_proggrammer_error(result_add)
	except Exception as error:
		logger.error(error)
		await func.send_proggrammer_error(error)


@dp.message_handler(commands=['support'])
async def support(message: types.Message):
	try:
		await func.support(message)

		user = get_data_user(message)
		if user != 0:
			result_add = await db_sql.add_user(user)
			if result_add != 1:
				await func.send_proggrammer_error(result_add)
	except Exception as error:
		logger.error(error)
		await func.send_proggrammer_error(error)


@dp.message_handler(commands=['information'])
async def information(message: types.Message):
	try:
		await func.information(message)

		user = get_data_user(message)
		if user != 0:
			result_add = await db_sql.add_user(user)
			if result_add != 1:
				await func.send_proggrammer_error(result_add)
	except Exception as error:
		logger.error(error)
		await func.send_proggrammer_error(error)


@dp.message_handler(commands=['panel'])
async def panel(message: types.Message):
	try:
		if message.from_user.id in admins:
			markup_inline = types.InlineKeyboardMarkup()
			statistic = types.InlineKeyboardButton(text = 'Статистика', callback_data = 'statistic')
			mailing = types.InlineKeyboardButton(text = 'Рассылка', callback_data = 'mailing')
			add_tariff = types.InlineKeyboardButton(text = 'Добавить тариф пользователю', callback_data = 'add_tariff')
			logs = types.InlineKeyboardButton(text = 'Скинуть logs', callback_data = 'logs')

			markup_inline.add(statistic)
			markup_inline.add(mailing)
			markup_inline.add(add_tariff)
			markup_inline.add(logs)
			await message.answer('Админ панель', reply_markup=markup_inline)
		else:
			await req_bot.result_message(message.text, message)

			user = get_data_user(message)
			if user != 0:
				result_add = await db_sql.add_user(user)
				if result_add != 1:
					await func.send_proggrammer_error(result_add)
	except Exception as error:
		logger.error(error)
		await func.send_proggrammer_error(error)


@dp.message_handler(content_types=["text"])
async def answer_message(message: types.Message):
	try:
		search = message.text.lower()
		await req_bot.result_message(search, message)
		
		user = get_data_user(message)
		if user != 0:
			result_add = await db_sql.add_user(user)
			if result_add != 1:
				await func.send_proggrammer_error(result_add)
	except Exception as error:
		logger.error(error)
		await func.send_proggrammer_error(error)
	
    
def get_data_user(message):
	try:
		user = {
			'user_id': message.from_user.id,
			'username': message.from_user.username,
			'first_name': message.from_user.first_name,
			'last_name': message.from_user.last_name
		}

		return user
	except Exception as error:
		logger.error(error)
		return 0



if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.create_task(monitoring.monitoring_channels())
	loop.create_task(func.check_time_tariff())
	executor.start_polling(dp, skip_updates=True, loop=loop)