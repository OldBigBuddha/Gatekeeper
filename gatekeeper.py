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
WELCOME_CHANNEL_ID = int( os.getenv('WELCOME_ID') )

# @member が付与されたことを通知するチャンネル
MEMBER_CHANNEL_ID  = int( os.getenv('MEMBER_ID') )

# 起動時に WELCOME_CHANNEL へ投稿するメッセージ
# なんか Bot 起動前のメッセージには on_reaction_add が反応しないっぽい？
welcome_message = '''**「OJI の部屋」へようこそ**
この鯖は主に OJI が実験場として使う鯖です。
OJI が作ってみたソフトウェアがいち早くさわれたり、開発段階から関係を持つこともできちゃいます。
また、日々の情報収集の中でこれはぜひみんなに知ってほしいなと思った情報等も共有していきます。
ほかにも日頃の愚痴であったり失敗談であったりと Twitter などでは見れない意外な一面も見れちゃいます。

OJI という生体に興味がある方は、以下の注意事項に目を通して最後に **Agreement** の意味を込めてこのメッセージに :white_check_mark: をしてください。
本鯖の門衛 Bot が、あなたに本鯖で楽しむために必要な役職を与えてくれるでしょう。

**注意事項**
- 「OJI の部屋」(以下、「本鯖」。)内で起こったいかなる事象においても OJI 及び本鯖のメンバーは **一切責任を持ちません** 。
- **本鯖内における絶対ルールは OJI の意志と気分です。**
- いろいろな方がいるので、想像力をはたらかせながらコミュニケーションを取りましょう。
- **Don't be a dick, be smart.**
'''

client = discord.Client()

@client.event
async def on_ready():
    print('ログインしたにゃ')
    welcome_channel = client.get_channel(WELCOME_CHANNEL_ID)
    await welcome_channel.purge()

    # Welcome Message の投稿
    await welcome_channel.send(welcome_message)

    # 新規ユーザーが Agreement の意味を込めて追加するリアクションを先に設定しておく
    await welcome_channel.last_message.add_reaction('✅')

@client.event
async def on_reaction_add(reaction, user):
    # 鯖内でリアクションがされた際の処理
    if user.bot or reaction.message.channel.id != WELCOME_CHANNEL_ID:
        # Bot からリアクションと Welcome Channel 以外のリアクションを無視
        return

    # @member を取得
    role = discord.utils.get(reaction.message.guild.roles, name='member')

    # @member をリアクションをしたユーザへ付与
    await user.add_roles(role)

    # @member を付与した旨を Member Channel へ流す
    await client.get_channel(MEMBER_CHANNEL_ID).send(f'{user} に {role.name} を付与したにゃ。')

client.run(TOKEN)