import mysql.connector
from datetime import datetime
from Variables.databases import *
from Variables.config import logger, bot, admins
from Variables.error_messages import *
from Variables.text_messages import *


class DatabaseSQL:

	def __init__(self):
		'''Подключение в базе данных'''

		try:
			self.db = mysql.connector.connect(host=IP_DB,
											user=USER_DB,
											password=PASSWORD_DB,
											database=DATABASE)
			self.sql = self.db.cursor()

			print("[INFO] Success connect to MySQL")
			logger.info("Success connect to MySQL")
		except Exception as error:
			print("[ERROR] Connection to MySQL")
			logger.error(f"Connection to MySQL: {error}")


	def connect_db(self):
		'''Подключение в базе данных'''

		try:
			self.db = mysql.connector.connect(host=IP_DB,
											user=USER_DB,
											password=PASSWORD_DB,
											database=DATABASE)
			self.sql = self.db.cursor()

			return 1
		except Exception as error:
			logger.error(error)
			return error


	def create_tables(self):
		'''Создание таблицы в базе данных users'''

		try:
			self.sql.execute(f"""CREATE TABLE IF NOT EXISTS `{TABLE_DATA}` (
							id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
							admins TEXT,
							black_list TEXT);""")
			self.db.commit()
			logger.info(f'Создана таблица {TABLE_DATA} в БД')

			self.sql.execute(f"""CREATE TABLE IF NOT EXISTS `{TABLE_USERS}` (
							id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
							user_id INTEGER NOT NULL,
							username VARCHAR(255),
							first_name VARCHAR(50) NOT NULL,
							last_name VARCHAR(100),
							time DATETIME DEFAULT CURRENT_TIMESTAMP,
							black_list TEXT,
							show_contact INTEGER DEFAULT 0);""")
			self.db.commit()
			logger.info(f'Создана таблица {TABLE_USERS} в БД')

			self.sql.execute(f"""CREATE TABLE IF NOT EXISTS `{TABLE_USERS_TARIFF_CATEGORY}` (
							id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
							user_id INTEGER NOT NULL,
							tariff VARCHAR(255) DEFAULT 0,
							time_subscribe DATETIME,
							is_free INTEGER DEFAULT 0,
							count INTEGER DEFAULT 1,
							sale INTEGER DEFAULT 0,
							pause INTEGER DEFAULT 0,
							time_pause DATETIME);""")
			self.db.commit()
			logger.info(f'Создана таблица {TABLE_USERS_TARIFF_CATEGORY} в БД')

			self.sql.execute(f"""CREATE TABLE IF NOT EXISTS `{TABLE_APPLICATIONS}` (
							id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
							user_id INTEGER NOT NULL,
							channel_id INTEGER NOT NULL,
							time DATETIME DEFAULT CURRENT_TIMESTAMP,
							contact TEXT,
							category VARCHAR(255),
							text_application TEXT);""")
			self.db.commit()
			logger.info(f'Создана таблица {TABLE_APPLICATIONS} в БД')

			return 1
		except Exception as error:
			logger.error(error)
			return error


	async def add_user(self, user: dict):
		"""Добавление пользователя в БД"""

		try:
			self.sql.execute(f"SELECT COUNT(*) FROM {TABLE_USERS} WHERE user_id={user['user_id']};")
			count_ = self.sql.fetchone()
			if count_ != None:
				count_ = count_[0]

			if count_ == 0:
				self.sql.execute(f"INSERT INTO {TABLE_USERS} (user_id, username, first_name, last_name) VALUES ({user['user_id']}, '{user['username']}', '{user['first_name']}', '{user['last_name']}');")
				self.db.commit()
				
				logger.info(f"[@{user['username']} {user['user_id']}] Создан новый пользователь")
				try:
					for i in admins:
						await bot.send_message(i, f"Новый пользователь @{user['username']} {user['user_id']}")
				except:
					pass

			await self.add_category_user(user['user_id'])
			return 1

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					await self.add_user(user)
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.add_user(user)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def add_category_user(self, user_id: int):
		"""Добавление записи в таблицу с тарифами и категориями"""

		try:
			self.sql.execute(f"SELECT COUNT(*) FROM {TABLE_USERS_TARIFF_CATEGORY} WHERE user_id={user_id};")

			if self.sql.fetchone()[0] == 0:
				self.sql.execute(f"INSERT INTO {TABLE_USERS_TARIFF_CATEGORY} (user_id) VALUES ({user_id});")
				self.db.commit()

			return 1

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					await self.add_category_user(user_id)
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.add_category_user(user_id)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def add_tariff(self, user_id: int, tariff: str):
		"""Добавление тарифа в таблицу с тарифами и категориями"""

		try:
			self.sql.execute(f"SELECT COUNT(*) FROM {TABLE_USERS_TARIFF_CATEGORY} WHERE user_id={user_id};")

			if self.sql.fetchone()[0] == 0:
				await self.add_category_user(user_id)

			self.sql.execute(f"UPDATE {TABLE_USERS_TARIFF_CATEGORY} SET tariff='{tariff}', time_subscribe='{datetime.now()}' WHERE user_id={user_id};")
			self.db.commit()

			return 1

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					result_add = await self.add_category_user(user_id)
					if result_add == 1:
						await self.add_tariff(user_id, tariff)
					else:
						return result_add
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.add_tariff(user_id, tariff)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	def get_tariff(self, user_id: int):
		"""Получения тарифа пользователя"""

		try:
			self.sql.execute(f"SELECT tariff FROM {TABLE_USERS_TARIFF_CATEGORY} WHERE user_id={user_id};")
			tariff = self.sql.fetchone()

			if tariff != None:
				return tariff[0]
			return tariff

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					return "0"
				return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				self.get_tariff(user_id)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def get_time_tariff_users(self):
		"""Получение время подписки на тариф у всех пользователей в определенной категории для 'таймера'"""
		
		try:
			self.sql.execute(f"SELECT user_id, tariff, time_subscribe FROM {TABLE_USERS_TARIFF_CATEGORY} WHERE tariff!='0';")
			users_time = self.sql.fetchall()

			return users_time

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					await self.get_time_tariff_users()
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.get_time_tariff_users()

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def stop_tariff(self, user_id: int):
		"""Удаление тарифа из таблицы с тарифами и категориями у пользователя"""

		try:
			self.sql.execute(f"UPDATE {TABLE_USERS_TARIFF_CATEGORY} SET tariff='0' WHERE user_id={user_id};")
			self.db.commit()

			return 1

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					result_add = await self.add_category_user(user_id)
					if result_add == 1:
						await self.stop_tariff(user_id)
					else:
						return result_add
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.stop_tariff(user_id)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def get_is_free(self, user_id: int):
		"""Получение статуса использования бесплатной подписки у пользователя в определенной категории"""

		try:
			self.sql.execute(f"SELECT is_free FROM {TABLE_USERS_TARIFF_CATEGORY} WHERE user_id={user_id};")
			is_free = self.sql.fetchone()[0]

			return is_free

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					result_add = await self.add_category_user(user_id)
					if result_add == 1:
						return 0
					return result_add
				return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.get_is_free(user_id)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def change_is_free(self, user_id: int):
		"""Изменение статуса использования бесплатной подписки в определенной категории"""

		try:
			self.sql.execute(f"UPDATE {TABLE_USERS_TARIFF_CATEGORY} SET is_free=1 WHERE user_id={user_id};")
			self.db.commit()

			return 1

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					result_add = await self.add_category_user(user_id)
					if result_add == 1:
						await self.change_is_free(user_id)
					else:
						return result_add
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.change_is_free(user_id)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def get_users_tariff(self):
		"""Получение пользователей и их тарифа"""

		try:
			self.sql.execute(f"SELECT user_id, tariff FROM {TABLE_USERS_TARIFF_CATEGORY} WHERE tariff!='0' AND pause!=1;")
			tariff = self.sql.fetchall()

			return tariff

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					return []
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.get_users_tariff()

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def get_remaining_time_tariff(self, user_id: int):
		"""Получение оставшегося времени тарифа у пользователя в определенной категории"""

		try:
			self.sql.execute(f"SELECT time_subscribe FROM {TABLE_USERS_TARIFF_CATEGORY} WHERE user_id={user_id};")
			time_tariff = self.sql.fetchone()[0]
			datetime_now = datetime.now()
			time_delta = datetime_now - time_tariff
			
			return time_delta

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					return -1
				return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.get_remaining_time_tariff(user_id)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def get_count_application(self, user_id: int):
		"""Получение номера заявки у пользователя в определенной категории"""

		try:
			self.sql.execute(f"SELECT count FROM {TABLE_USERS_TARIFF_CATEGORY} WHERE user_id={user_id};")
			count_app = self.sql.fetchone()[0]
			
			return count_app

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					result_add = await self.add_category_user(user_id)
					if result_add == 1:
						return 1
					return result_add
				return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.get_count_application(user_id)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def update_count_application(self, user_id: int, count_app: int):
		"""Обновление номера заявки у пользователя в определенной категории"""

		try:
			self.sql.execute(f"UPDATE {TABLE_USERS_TARIFF_CATEGORY} SET count={count_app+1} WHERE user_id={user_id};")
			self.db.commit()
			
			return 1

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					result_add = await self.add_category_user(user_id)
					if result_add == 1:
						await self.update_count_application(user_id, count_app)
					else:
						return result_add
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.update_count_application(user_id, count_app)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def get_status_sale(self, user_id: int):
		"""Получение статуса скидки у пользователя в определенной категории"""
		
		try:
			self.sql.execute(f"SELECT sale FROM {TABLE_USERS_TARIFF_CATEGORY} WHERE user_id={user_id};")
			status_sale = self.sql.fetchone()[0]

			return status_sale

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					result_add = await self.add_category_user(user_id)
					if result_add == 1:
						await self.get_status_sale(user_id)
					else:
						return result_add
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.get_status_sale(user_id)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def change_status_sale(self, user_id: int):
		"""Изменение статуса скидки у пользователя в определенной категории"""

		try:
			self.sql.execute(f"UPDATE {TABLE_USERS_TARIFF_CATEGORY} SET sale=1 WHERE user_id={user_id};")
			self.db.commit()

			return 1

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					result_add = await self.add_category_user(user_id)
					if result_add == 1:
						await self.change_status_sale(user_id)
					else:
						return result_add
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.change_status_sale(user_id)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def get_user_id_username(self, username: str):
		"""Получение id пользователя по его username"""

		try:
			self.sql.execute(f"SELECT user_id FROM {TABLE_USERS} WHERE username='{username}';")
			user_id = self.sql.fetchone()

			if user_id != None:
				return user_id[0]
			return user_id

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					return 0
				return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.get_user_id_username(username)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def get_username_by_id(self, user_id: int):
		"""Получение username пользователя по его id"""

		try:
			self.sql.execute(f"SELECT username FROM {TABLE_USERS} WHERE user_id={user_id};")
			username = self.sql.fetchone()[0]

			return username

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					return 0
				return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.get_username_by_id(user_id)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def get_count_users(self):
		"""Получение количества пользователей для статистики"""

		try:
			self.sql.execute(f"SELECT COUNT(*) FROM {TABLE_USERS};")
			count_users = self.sql.fetchone()[0]

			return count_users

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					await self.get_count_users()
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.get_count_users()

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def get_count_subscribe_free_users(self):
		"""Получение количества подписанных на бесплатный тариф пользователей для статистики"""

		try:
			self.sql.execute(f"SELECT COUNT(*) FROM {TABLE_USERS_TARIFF_CATEGORY} WHERE tariff='free';")
			count_users = self.sql.fetchone()[0]

			return count_users

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					await self.get_count_subscribe_free_users()
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.get_count_subscribe_free_users()

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def get_count_payment_users(self):
		"""Получение количества пользователей купивших подписку для статистики"""

		try:
			self.sql.execute(f"SELECT COUNT(*) FROM {TABLE_USERS_TARIFF_CATEGORY} WHERE tariff IN ('{COMMAND_ONE_TARIFF}', '{COMMAND_TWO_TARIFF}', '{COMMAND_THREE_TARIFF}');")
			count_users = self.sql.fetchone()[0]

			return count_users

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					await self.get_count_payment_users()
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.get_count_payment_users()

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def add_application(self, user_id, channel_id, contact, message):
		"""ДОбавление данных отправленной заявки пользователю в БД"""

		try:
			if "https://t.me/" in contact:
				contact = contact.replace("https://t.me/", "", 1)

			self.sql.execute(f"INSERT INTO {TABLE_APPLICATIONS} (user_id, channel_id, contact, category, text_application) VALUES ({user_id}, {channel_id}, '{contact}', '{CATEGORY}', '{message}');")
			self.db.commit()

			count_application = await self.get_count_applications()
			if count_application > 1000:
				result_delete = await self.delete_old_applications()
				if result_delete == 0:
					logger.error(result_delete)

			return 1
		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					await self.add_application(user_id, channel_id, contact, message)
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.add_application(user_id, channel_id, contact, message)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def get_count_applications(self):
		try:
			self.sql.execute(f"SELECT COUNT(*) FROM {TABLE_APPLICATIONS};")
			count_applications = self.sql.fetchone()[0]

			return count_applications

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					return 0
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.get_count_applications()

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def delete_old_applications(self):
		try:
			self.sql.execute(f"DELETE FROM {TABLE_APPLICATIONS} ORDER BY id DESC LIMIT 250;")
			self.db.commit()

			return 1
		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					return 1
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.delete_old_applications()

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def check_contact_replay(self, contact, user_id, message):
		try:
			if "https://t.me/" in contact:
				contact = contact.replace("https://t.me/", "", 1)
			elif "t.me/" in contact:
				contact = contact.replace("t.me/", "", 1)

			contact = contact.replace("@", "", 1)

			self.sql.execute(f"SELECT COUNT(*) FROM {TABLE_APPLICATIONS} WHERE user_id={user_id} AND (contact='{contact}' OR text_application='{message}') AND category='{CATEGORY}';")
			count_replay = self.sql.fetchone()[0]

			return count_replay

		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					return 0
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.check_contact_replay(contact, user_id, message)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def check_contact_in_black_list(self, contact):
		try:
			if "https://t.me/" in contact:
				contact = contact.replace("https://t.me/", "", 1)
			elif "t.me/" in contact:
				contact = contact.replace("t.me/", "", 1)

			contact = contact.replace("@", "", 1)

			self.sql.execute(f"SELECT black_list FROM {TABLE_DATA};")
			black_list = self.sql.fetchone()

			if black_list == None:
				black_list = []
			else:
				black_list = black_list[0].split(";")

			if contact in black_list:
				return 1
			else:
				return 0
		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					return 0
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.check_contact_in_black_list(contact)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def get_black_list_user(self, user_id):
		try:
			self.sql.execute(f"SELECT black_list FROM {TABLE_USERS} WHERE user_id={user_id};")
			black_list = self.sql.fetchone()[0]

			if black_list == None:
				return ""

			return black_list
			
		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					return ""
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return 0

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.check_contact_in_black_list(user_id)

			else:
				logger.error(error)
				return 0

		except Exception as error:
			logger.error(error)
			return 0


	async def add_spam_contact(self, user_id, contact):
		try:
			black_list = await self.get_black_list_user(user_id)
			if ";" in black_list:
				list_black_list = black_list.split(";")
				if contact in list_black_list:
					return -1
					
			black_list += contact + ";"

			self.sql.execute(f"UPDATE {TABLE_USERS} SET black_list='{black_list}' WHERE user_id={user_id};")
			self.db.commit()

			return 1
		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					await self.add_spam_contact(user_id, contact)
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.add_spam_contact(user_id, contact)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def add_spam(self, username):
		try:
			self.sql.execute(f"SELECT black_list FROM {TABLE_DATA};")
			black_list = self.sql.fetchone()[0]
			black_list += ";" + username

			self.sql.execute(f"UPDATE {TABLE_DATA} SET black_list='{black_list}';")
			self.db.commit()

			return 1
		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					await self.add_spam(username)
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.add_spam(username)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def get_id_users(self, whom):
		try:
			if whom == "mailing_without":
				self.sql.execute(f"SELECT user_id FROM {TABLE_USERS_TARIFF_CATEGORY} WHERE tariff='0';")

			elif whom == "mailing_free":
				self.sql.execute(f"SELECT user_id FROM {TABLE_USERS_TARIFF_CATEGORY} WHERE tariff='free';")

			elif whom == "mailing_pay":
				self.sql.execute(f"SELECT user_id FROM {TABLE_USERS_TARIFF_CATEGORY} WHERE tariff IN ('{COMMAND_ONE_TARIFF}', '{COMMAND_TWO_TARIFF}', '{COMMAND_THREE_TARIFF}');")

			elif whom == "mailing_all_users":
				self.sql.execute(f"SELECT user_id FROM {TABLE_USERS};")

			users = self.sql.fetchall()
			return users
		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					return []
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.get_id_users()

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def get_status_pause(self, user_id):
		try:
			self.sql.execute(f"SELECT pause FROM {TABLE_USERS_TARIFF_CATEGORY} WHERE user_id={user_id};")
			pause = self.sql.fetchone()

			if pause != None:
				return pause[0]
			return 0
		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					await self.get_status_pause(user_id)
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.get_status_pause(user_id)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def change_status_pause(self, user_id, status):
		try:
			if status == PAUSE_LAUNCH:
				self.sql.execute(f"UPDATE {TABLE_USERS_TARIFF_CATEGORY} SET pause={status}, time_pause='{datetime.now()}' WHERE user_id={user_id};")
				self.db.commit()

			elif status == PAUSE_USED:
				self.sql.execute(f"SELECT time_subscribe, time_pause FROM {TABLE_USERS_TARIFF_CATEGORY} WHERE user_id={user_id};")
				time_tariff, time_pause = self.sql.fetchone()
				
				time_delta = datetime.now() - time_pause
				time_tariff += time_delta

				self.sql.execute(f"UPDATE {TABLE_USERS_TARIFF_CATEGORY} SET pause={status}, time_subscribe='{time_tariff}' WHERE user_id={user_id};")
				self.db.commit()

			return 1
		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					await self.change_status_pause(user_id, status)
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.change_status_pause(user_id, status)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def get_show_contact(self, user_id):
		try:
			self.sql.execute(f"SELECT show_contact FROM {TABLE_USERS} WHERE user_id={user_id};")
			show_contact = self.sql.fetchone()

			if show_contact != None:
				return show_contact[0]
			return show_contact
		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					await self.get_show_contact(user_id)
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.get_show_contact(user_id)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error


	async def update_show_contact(self, user_id):
		try:
			show_contact = await self.get_show_contact(user_id)
			if show_contact != None:
				self.sql.execute(f"UPDATE {TABLE_USERS} SET show_contact={show_contact+1} WHERE user_id={user_id};")
				self.db.commit()
			
			return 1
		except mysql.connector.Error as error:
			if error.errno == ERROR_NOT_EXISTS_TABLE:
				result_create = self.create_tables()
				if result_create == 1:
					await self.update_show_contact(user_id)
				else:
					return result_create

			elif error.errno == ERROR_CONNECT_MYSQL:
				logger.error(f"Connection to MYSQL: {error}")
				return error

			elif error.errno == ERROR_LOST_CONNECTION_MYSQL:
				self.connect_db()
				await self.update_show_contact(user_id)

			else:
				logger.error(error)
				return error

		except Exception as error:
			logger.error(error)
			return error