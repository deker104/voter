import simplejson as json

from pathlib import Path

from config import OWNER_ID

database_file = Path('database.json')
if database_file.exists():
    database = json.loads(database_file.read_text())
else:
    database = {}

chat_members_file = Path('chat_members.txt')
if chat_members_file.exists():
    chat_members = list(map(int, chat_members_file.read_text().splitlines()))
else:
    chat_members = [OWNER_ID]


def check_database(id):
    return any(row['id'] == id for row in database)


def update_database(vote):
    database.append(vote)
    database_file.write_text(json.dumps(database))


def check_in_chat(user):
    id = user['id']
    return id in chat_members
