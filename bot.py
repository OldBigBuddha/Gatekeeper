import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('NTc4MTY1MTQ5MDAxODQyNjg4.XN7NiQ.UIAcO7qsLJ710QboiT3M8scvcs8')