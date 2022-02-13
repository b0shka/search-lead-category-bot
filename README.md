# search-lead-category-bot

A [bot](https://t.me/leadscrolltargetbot) for job search by targeting and design in telegram channels and chats

![Python][python-version]

---
## Installation

#### Requirements
* Python3.8+
* Linux, Windows or macOS

#### Installing
```
git clone https://github.com/b0shka/search_lead_category_bot.git
cd search_lead_category_bot
```

#### Configure
And in the `target` and `design` folder in the `Variables/config.py` you need to specify your bot token, a token for payment by kiwi, and data for connecting to the mysql database

#### To install the necessary libraries
#### Installing on Linux or Mac
```
pip3 install -r requirements.txt
```

#### Installing on Windows
```
pip install -r requirements.txt
```

---
## Usage
```
cd target/
python3 ./main.py
```
OR
```
cd design/
python3 ./main.py
```

---
## Additionally
A `target/bot_target.service` and `design/bot_design.service` files was also created to run this bot on the server


[python-version]: https://img.shields.io/static/v1?label=Python&message=v3.8&color=blue
