import discord
from discord import utils

from discord.ext import commands

import datetime

import config

class MyClient(discord.Client):

    async def on_ready(self):
        print(f"Logged on as {self.user}\n")
        game = discord.Game("Racin Drift 3")
        await client.change_presence(status=discord.Status.online, activity=game)

    async def on_raw_reaction_add(self, payload):
        if (payload.message_id == config.POST_ID): # checking if correct message got a reaction
            guild = client.get_guild(payload.guild_id)
            channel = client.get_channel(payload.channel_id) # getting channel
            message = await channel.fetch_message(payload.message_id) # getting message to get user

            '''
            for emoji in config.REACTIONS.keys(): # add bot reactions
                await message.add_reaction(emoji)
            '''

            users = set()
            for reaction in message.reactions:
                async for user in reaction.users():
                    users.add(user)

        try:
            delete_time = 60.0 # in seconds, time to delete message
            emoji = str(payload.emoji) # getting sent emoji

            time_string = config.REACTIONS[emoji]
            time_string_list = time_string.split('~')

            avg_time = 0 # expected time increment

            for item in time_string_list:
                avg_time += int(item)

            this_time = datetime.datetime.now()
            this_time_after = this_time + datetime.timedelta(minutes=(avg_time // 2))
            username_full = config.USERSNAMES[list(users)[0].name] + "я"

            await channel.send(f"{username_full} придёт через {config.REACTIONS[emoji]} минут! (Расчетное время возвращения: {this_time_after.hour}:{this_time_after.minute})", delete_after=delete_time)
            
            for reaction in message.reactions:
                await reaction.remove(list(users)[0])

        except KeyError as e:
            username_full = config.USERSNAMES[list(users)[0].name] + "ю"

            await channel.send(f"Кажется, мы больше не увидим {username_full} :(", delete_after=delete_time)
        except Exception as e:
            print(repr(e))

client = MyClient()
client.run(config.TOKEN)