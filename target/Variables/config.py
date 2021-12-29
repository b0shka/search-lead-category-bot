import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pyqiwip2p import QiwiP2P
from dotenv import load_dotenv


dotenv_path = '../../.env'
load_dotenv(dotenv_path)

TOKEN = os.getenv("TOKEN_TEST")
SECRET_KEY_PAYMENT = os.getenv("SECRET_KEY_PAYMENT")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot,  storage=MemoryStorage())
p2p = QiwiP2P(auth_key=SECRET_KEY_PAYMENT)

USER = "q"
PATH_TO_BOT = f"/home/{USER}/p/python/projects/search_lead_category_bot/target"
PATH_TO_IMG = f"{PATH_TO_BOT}/img/start.jpg"
PATH_TO_LOGS = f"{PATH_TO_BOT}/Logs/info.log"

PROGRAMMER_ID = int(os.getenv("PROGRAMMER_ID"))
MANAGER_ID = int(os.getenv("MANAGER_ID"))
admins = [PROGRAMMER_ID, MANAGER_ID]


API_ID = int(os.getenv("API_ID_target"))
API_HASH = os.getenv("API_HASH_target")
NAME_SESSION = "test"


IP_DB = os.getenv("BOTS_CATEGORY_IP")
USER_DB = os.getenv("USER_DB")
PASSWORD_DB = os.getenv("BOTS_CATEGORY_PASSWORD")
DATABASE = os.getenv("DATABASE")

TABLE_DATA = "data"
TABLE_USERS = 'users_target'
TABLE_USERS_TARIFF_CATEGORY = 'users_tariff_target'
TABLE_APPLICATIONS = "applications_target"

ERROR_NOT_EXISTS_TABLE = 1146
ERROR_CONNECT_MYSQL = 2006
ERROR_LOST_CONNECTION_MYSQL = 2013


if not os.path.exists('Logs'):
	os.mkdir('Logs')

logging.basicConfig(filename=PATH_TO_LOGS, format = u'[%(levelname)s][%(asctime)s] %(funcName)s:%(lineno)s: %(message)s', level='INFO')
logger = logging.getLogger()
