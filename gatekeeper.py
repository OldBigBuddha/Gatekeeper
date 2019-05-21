'''
Copyright 2019 OldBigBuddha

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''

import discord
import logging
import os

# Log Level の設定
logging.basicConfig(level=logging.WARN)

# dotenv を読み込む
# TOKEN、WELCOME_ID、MEMBER_ID が必要
from dotenv import load_dotenv
load_dotenv()

# Bot のアクセストークン
TOKEN = os.getenv('TOKEN')

# 新しく入ってきた人のみが見れるチャンネル、ここのメッセージにリアクションをすると @member が付与される。
WELCOME_CHANNEL_ID = int( os.getenv('WELCOME_CHANNEL_ID') )

# @member が付与されたことを通知するチャンネル
ENTRY_NOTIFY_CHANNEL_ID = int(os.getenv('ENTRY_NOTIFY_CHANNEL_ID'))

# @member の ID
MEMBER_ROLE_ID = int(os.getenv('MEMBER_ROLE_ID'))


client = discord.Client()

@client.event
async def on_ready():
    print('ログインしたにゃ')

@client.event
async def on_raw_reaction_add(payload):
    received_channel_id = client.get_channel(payload.channel_id).id

    if received_channel_id == WELCOME_CHANNEL_ID:
        guild = client.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        member_role = guild.get_role(MEMBER_ROLE_ID)

        await user.add_roles(member_role)
        await guild.get_channel(ENTRY_NOTIFY_CHANNEL_ID).send(f'{user.name} が member を取得したにゃ!')

client.run(TOKEN)