TIME_SLEEP_MAILING_START_1 = 300
TIME_SLEEP_MAILING_START_2 = 1200
TIME_SLEEP_MAILING_FREE = 21600
TIME_SLEEP_MAILING_PAYMENT = 43200
TIME_SLEEP_CHECK_TARIFFS = 3540
TIME_SLEEP_CHECK_CHANNELS = 100

FREE_TERM = 24
PRICE_ONE_TARIFF = 179
PRICE_TWO_TARIFF = 390
PRICE_THREE_TARIFF = 990

SALE_PRICE_ONE_TARIFF = 143
SALE_PRICE_TWO_TARIFF = 312
SALE_PRICE_THREE_TARIFF = 792

TEXT_ONE_TARIFF = "3 дня"
TEXT_TWO_TARIFF = "1 неделя"
TEXT_THREE_TARIFF = "1 месяц"

COMMAND_FREE_TARIFF = 'free'
COMMAND_ONE_TARIFF = 'three_days'
COMMAND_TWO_TARIFF = 'one_week'
COMMAND_THREE_TARIFF = 'one_month'

TARIFFS = {
	COMMAND_ONE_TARIFF: TEXT_ONE_TARIFF,
	COMMAND_TWO_TARIFF: TEXT_TWO_TARIFF,
	COMMAND_THREE_TARIFF: TEXT_THREE_TARIFF
}

PRICES = {
	COMMAND_ONE_TARIFF: PRICE_ONE_TARIFF,
	COMMAND_TWO_TARIFF: PRICE_TWO_TARIFF,
	COMMAND_THREE_TARIFF: PRICE_THREE_TARIFF
}

SALE_PRICES = {
	COMMAND_ONE_TARIFF: SALE_PRICE_ONE_TARIFF,
	COMMAND_TWO_TARIFF: SALE_PRICE_TWO_TARIFF,
	COMMAND_THREE_TARIFF: SALE_PRICE_THREE_TARIFF
}

DEADLINES_TARIFFS = {
	COMMAND_ONE_TARIFF: 3,
	COMMAND_TWO_TARIFF: 7,
	COMMAND_THREE_TARIFF: 30
}

PAUSE_LAUNCH = 1
PAUSE_SUSPEND = 0
PAUSE_USED = -1

COUNT_SHOW_CONTACT = 2

LINK_CHANNEL = 'https://t.me/Leadscrollinfo'
USERNAME_CHANNEl = '@Leadscrollinfo'
LINK_MANAGER = 'https://t.me/leadscroll'
USERNAME_MANAGER = '@leadscroll'

BUTTON_TARIF_ONE = f"{FREE_TERM} часа free + подарок 🎁"
BUTTON_TARIF_TWO = f"{TEXT_ONE_TARIFF} - {PRICE_ONE_TARIFF}₽ 📕"
BUTTON_TARIF_THREE = f"{TEXT_TWO_TARIFF} - {PRICE_TWO_TARIFF}₽ 📗"
BUTTON_TARIF_FOUR = f"{TEXT_THREE_TARIFF} - {PRICE_THREE_TARIFF}₽ 📘"

SALE_BUTTON_TARIF_TWO = f"{TEXT_ONE_TARIFF} - {SALE_PRICE_ONE_TARIFF}₽ 📕"
SALE_BUTTON_TARIF_THREE = f"{TEXT_TWO_TARIFF} - {SALE_PRICE_TWO_TARIFF}₽ 📗"
SALE_BUTTON_TARIF_FOUR = f"{TEXT_THREE_TARIFF} - {SALE_PRICE_THREE_TARIFF}₽ 📘"

BUTTON_PAYMENT_ONE = "Оплатить в боте 🤖"
BUTTON_PAYMENT_TWO = "Оплатить напрямую 🙋‍♂️"

REPLACE_SYMBOLS = "###"
REPLACE_SYMBOLS_1 = "$$$"
REPLACE_SYMBOLS_2 = "@@@"


start_message_1 = """
Привет! 👋

Как все работает? 🤔: 
🔸 Наш бот ищет заявки по 500+ чатам в Telegram и присылает их в бота, распределяя между вами, что бы не создавать конкуренции.

🔸 Всё что нужно:
 - Подключить бесплатный тариф
 - Получить подарок
 - Начать получать заявки и зарабатывать деньги
"""

start_message_2 = f"""
⚡️Получи бесплатную подписку на {FREE_TERM} часа + подарок 🎁 от нашего сервиса.

Подробнее о подписке и других возможностях бота -> {USERNAME_CHANNEl} 💬
"""

MAILING_MESSAGE_START_1 = """
Тебе дана уникальная возможность опробовать нашего бота на практике 😨

Всего 2 простых действия:
  - Нажать кнопку "Активировать подписку 🎁"
  - Отвечать на новые заявки

Так чего же ты ждешь?!🧐
"""

MAILING_MESSAGE_START_2 = """
Ты ещё не попробовал нашего бота в действии? 🧐

Обрабатывай заявки уже сейчас и получи бесплатный подарок, который поможет тебе максимально эффективно забирать заказы 🤝🔥
"""

CHOOSING_CATEGORY = f"""
✅ После оплаты тарифа {REPLACE_SYMBOLS}, вы получите:

✔️ Качественные и целевые заявки по таргетированной рекламе.
- ВК 
- Инстаграм
- Фейсбук
- Одноклассники (может быть очень мало)
➖➖➖➖➖➖➖➖
• Бот сначала отправляет заявки людям с подпиской, после чего пользователям на бесплатном тарифе.
"""

SUPPORT = """
🤖 Если у вас возник вопрос или проблема с использованием бота, то напишите нашему менеджеру.
"""

INFORMATION = f"""
<b>FAQ | Часто возникающие вопросы</b>

🔸 <b>Откуда и как я получаю заявки?</b>
Бот мониторит сотни открытых и закрытых чатов ежедневно и отбирает только самое нужное.

🔸 <b>Сколько заявок я могу получать в день?</b>
Каждый день в бот поступает 20+ целевых заявок по таргету и это не предел, мы стараемся постоянно находить новые чаты и увеличивать количество заявок.

🔸 <b>Как начать получать заявки?</b>
1) Выберите "Тарифы"
2) Оплатите нужный вам тариф и начниете получать заявки

🔸 <b>В чем преимущества бота?</b>
- Качество и количество заявок (Вам не нужно выискивать среди сотен чатов заявки, которые могут оказаться неактуальными)
- Вы получайте 20+ свежих заявок в день (задержка между публикацией заявки в чате и нашем боте = 30 секунд)

• Вам не нужно тратить время на поиски.
• Сфокусируйтесь на обработке клиентов и своих кейсах.

🔸 <b>У нас есть свой беспллатный обучающий раздел, который поможет вам забирать заявки эффективнее.</b>
(Нажмите на кнопку "Обучение")
"""

STUDY = f"""
🔸 Здесь мы выкладываем различные обучающие материалы и рассказываем, как эффективнее работать с заказчиками.
👉🏻 https://t.me/leadscrolledu
"""

FREE_TARIFF = f"""
Вы выбрали тариф «{FREE_TERM} часа бесплатно»

Бот отправит вам заявки, как только они появятся в каналах.

На бесплатном тарифе мы скрываем контакты. Это нужно, чтобы клиенты оформившие платную подписку, не теряли заказчиков ❗️
"""

FREE_TARIFF_MAILING = """
Забери свой подарок! 🎁
- Специальный чек-лист по составлению правильного отклика на заявки.
👇
https://clck.ru/YvTjG
"""

ALREADY_USING_FREE = f"""
У вас уже подключен бесплатный тариф ☺️
До окончания тарифа: {REPLACE_SYMBOLS}
"""

ALREADY_PURCHASED_TARIFF = f"""
✔️ Вы уже приобрели тариф «{REPLACE_SYMBOLS}»
До окончания тарифа: {REPLACE_SYMBOLS}
Количество присланных заявок: {REPLACE_SYMBOLS}
"""

PAUSE_DESC = """
Внимание! Паузу вы можете использовать только один раз.
"""

PAUSE_USING = """
Ваш тариф сейчас стоит на паузе.
"""

START_PAUSE = """
Ваш тариф поставлен на паузу
"""

STOP_PAUSE = """
Ваш тариф снова возобновлен, попытка ставить тариф на паузу использована
"""

ALREADY_USED_FREE = f"""
❗️Вы уже использовали бесплатный тариф 
Посмотрите другой раздел или попробуйте наши другие тарифы в данной категории ☺️
"""

ENDED_FREE_TARIFF = f"""
ℹ️ Ваша бесплатная подписка закончилась. 

Количество присланных заявок: {REPLACE_SYMBOLS}

Мы предлагаем сотрудничать дальше вместе с нами и ежедневно получать заказы. Благодаря нам 92% специалистов находят своих заказчиков за первые три дня 🤝

Так же, специально для вас мы дарим скидку на любой наш тариф в размере 20% 🔥
"""

MAILING_MESSAGE_AFTER_FREE = f"""
Все еще думаешь? 🧐

А что будет, если я тебе скажу, что ты получишь 20% скидку на любой платный тариф и 3 дня использования в подарок? 🎁

Пиши мне в личные сообщения промокод «SALE» и подключай данное предложение! ⚡️

Внимание: Акция работает только на одном тарифе 
"""

PAYMENT_TITLE = 'Оплата тарифа'

PAID_TARIFF = """
Если у вас возникли трудности во время оплаты, обращайтесь в поддержку - @Leadscroll
"""

ENABLING_TARIFF = f"""
✅ Вы успешно оформили подписку! 

Подождите первые заявки и приступайте к работе!  📲
"""

STOP_TARIFF = f"""
❌ Ваша подписка закончилась
Количество присланных заявок: {REPLACE_SYMBOLS}
"""

END_WARNING_PAYMENT_TARIFF = f"""
Ваша подписка истекает ровно через 24 часа ❗️
"""

MAILING_MESSAGE_AFTER_PAYMENT = """
Продли свою подписку со скидкой 40% ⚡️

Предложение действует только 12 часов ❗️
"""

APPLICATION = f"""
<b>Заявка №{REPLACE_SYMBOLS_1} 🚀 | {REPLACE_SYMBOLS_2}</b>

{REPLACE_SYMBOLS}
"""

HIDE_CONTACT = """

Контакты: *****"""

APPLICATION_FREE = f"""
_________

📚 Почему мы скрываем контакты на бесплатном периоде ❓ -  https://clck.ru/YjYAs

По вопросам бота - {USERNAME_MANAGER}
"""

STATISTIC = f"""
<b>Статистика:</b>
Всего пользователей - {REPLACE_SYMBOLS}
Пользователей с бесплатной подпиской - {REPLACE_SYMBOLS}
Пользователей с платной подпиской - {REPLACE_SYMBOLS}
Не активных пользователей - {REPLACE_SYMBOLS}
"""


CATEGORY = "target"
CATEGODIES = {
	CATEGORY: 'Таргет'
}

target = ["таргетолог", "таргетинг", "таргет", CATEGORY]
target_phrases = ["настроить таргет"]

no = ['дизайн', "дизайнер", 'smm', 'смм', 'копирайтинг', 'копирайтер', 'seo', 'маркетолог', 'креатив', 'клиент', 'ассистент', 'менеджер', 'продюсер']

advertisement = [
	"внимание, читай до конца",
	'кypc',
	'низкие цены',
	"внимательно почитайте", 
	"внимательно прочитайте",
	"внимательно читайте", 
	"читай до конца",
	"что входит в мою работу",
	"меня зовут",
	"чем я могу быть вам", 
	"всем привет",
	"здравствуйте",
	'массовая рассылка',
	"я вам помогу",
	"супер акция",
	"я начинающий",
	"добрый вечер",
	"добрый день",
	"доброе утро",
	"доброго времени суток",
	"#ишуклиента",
	"#помогy",
	'#резюме',
	'спикер',
	"мастер-майнд",
	"будет бесплатный",
	"регистрируйся"
]
