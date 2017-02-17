import json
import requests
import time
import urllib
from dbhelper import DBhelper

TOKEN = "330691777:AAFZWNf3ti5qoKQafX4yQd_tLhbUs1SbTKc"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

db = DBhelper()

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        firstname = update["message"]["chat"]["first_name"]
        lastname = update["message"]["chat"]["last_name"]
        items = db.get_items(chat)
        print(items)
        if text == "/done":
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)
        elif text == "/emptydb":
            items = db.delete_all(chat)
            message = "The database is empty now"
            send_message(message, chat)
        elif text == "/getlist":
            items = db.get_items(chat)
            if not items:
                message = "The database is empty"
            else:
                message = "This is the list for " + firstname + " " + lastname + "\n" + "\n".join(items)
            send_message(message, chat)
        elif text == "/start":
            message = "Welcome to Todobot write /commands for commands"
            send_message(message,chat)
        else:
            if text in items:
                db.delete_item(text, chat)
            else:
                db.add_item(text, chat)
                items = db.get_items(chat)
                message = "\n".join(items)
                send_message(message, chat)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    print(url)
    get_url(url)


def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
