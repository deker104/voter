from telethon import TelegramClient
from telethon.tl.types import Chat

from sys import argv

api_id = int(argv[1])
api_hash = argv[2]

client = TelegramClient('chat_parsing', api_id, api_hash)
client.start()


async def main():
    channel = await client.get_input_entity('dshindov_chat')
    user_list = client.iter_participants(entity=channel)
    async for _user in user_list:
        print(_user.id)


client.loop.run_until_complete(main())
