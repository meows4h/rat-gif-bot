import discord
from discord.ext import tasks, commands
import responses
import rat
from datetime import datetime
from pytz import timezone

pst_timezone = timezone('US/Pacific')
datetime_pst = datetime.now(pst_timezone)
last_gif_sent = datetime_pst.day # add a -1 here or something to make this resend on open

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(message, user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():

    # token and intents
    with open('token.txt') as token_file:
        TOKEN = token_file.read()

    # print(TOKEN)

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    # on start
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        game = discord.Game('with the rat pack!')
        await client.change_presence(status=discord.Status.idle, activity=game)

        channel = client.get_channel(1346072552493027429)
        # await channel.send(embed=main_embed)

        try:
            check_loop.start()
            print("Check started.")
        except:
            check_loop.cancel()
            print("Check stopped.")

    @tasks.loop(minutes=1)
    async def check_loop():

        channel = client.get_channel(1346072552493027429)

        global last_gif_sent
        pst_timezone = timezone('US/Pacific')
        datetime_pst = datetime.now(pst_timezone)
        curr_day = datetime_pst.day

        gif_url = ''

        if curr_day != last_gif_sent:
            last_gif_sent = curr_day
            gif_url = rat.get_rat(curr_day)

        # print(f'GIF URL: {gif_url}, TRUE? {gif_url != ''}')

        if gif_url != '':
            await channel.send(gif_url)

        # creating the message to pass as the status based on the array
        # status_message = ''

        # update status message
        # activity_status = discord.Activity(
        #     type=discord.ActivityType.watching, 
        #     name='rat obtainer',
        #     state=f'{status_message}')
        # await client.change_presence(status=discord.Status.idle, activity=activity_status)

    @client.event
    async def on_message(message):

        # checks to not respond to self or bots
        if message.author == client.user or message.author.bot == True:
            return
        
        # gather info
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # print(f'{username} said: "{user_message}" ({channel})')

        # command and ping check.
        if channel == 'Direct Message with Unknown User':
            await send_message(message, user_message, is_private=True)
        else:
            if '!rat ' in user_message: # prefix goes here
                user_message = user_message[5:] # inclusive slice
                print(user_message)
                await send_message(message, user_message, is_private=False)
            elif '<@1367966587184746688>' in user_message:
                user_message = user_message.replace('<@1367966587184746688>', '')
                if user_message[0] == ' ':
                    user_message = user_message[1:]
                if user_message[len(user_message)-1] == ' ':
                    user_message = user_message[:len(user_message)-1]
                if '  ' in user_message:
                    user_message = user_message.replace('  ', ' ')
                await send_message(message, user_message, is_private=False)

    # runs
    client.run(TOKEN)