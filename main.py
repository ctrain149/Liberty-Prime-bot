import discord
import sys
from random import randint
import urllib.request
from discord.ext import commands
from Map_Functions import *

# Defines Bot, Bot prefix, bot description, and the server
bot = commands.Bot(command_prefix = '.', description = 'Deliverer of Freedom and Democracy. Also serving discord channels near you!')
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
path_quotes = 'C:\\Users\\Challice\\Documents\\Liberty-Prime-bot\\quotes\\'
deagles_server_id = '517471244623544341'
general_channel_id = '517471244623544343'
welcome_channel_id = '546434534791446528'
rules_channel_id = '546434619365654528'
bot_chat_channel_id = '568897911195303976'
general_voice_channel_id = '517471244623544345'

@bot.event
async def on_ready():
    """Add a gamme, load opus, and say that Liberty Prime is online once the bot is ready."""
    discord.opus.load_opus('libopus-0.x64.dll')
    await bot.change_presence(game=discord.Game(name='Testing'))
    # await bot.send_message(bot.get_channel(general_channel_id),
    #                       'Liberty Prime is online. All systems nominal. Weapons hot. Mission: the destruction of any and all Chinese communists')

@bot.event
async def on_error():
    """Send the error message to #bot-chat. Not working currently."""
    await bot.send_message(bot.get_channel(bot_chat_channel_id), sys.exc_info())

@bot.event
async def on_message(message):
    author = message.author
    channel = message.channel
    content = message.content.lower()

    if author != 'Liberty Prime Bot#3840':
        if 'real communism has never been tried' in content:
            await bot.send_message(channel, 'COMMUNISM HAS BEEN TRIED. COMMUNISM IS THE VERY DEFINITION OF FAILURE.')
        elif 'communism' in content:
            await bot.send_message(channel, 'DEATH IS A PREFERABLE ALTERNATIVE TO COMMUNISM.')
            await bot.send_message(channel, author != 'Liberty Prime Bot#3840')
            await bot.send_message(channel, author)
            await bot.send_message(channel, 'IS NOT')
            await bot.send_message(channel, 'Liberty Prime Bot#3840')
    
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    """Great a new member when they join."""
    general = bot.get_channel(general_channel_id)
    welcome = bot.get_channel(welcome_channel_id)
    rules = bot.get_channel(rules_channel_id)
    await bot.send_message(general, 'Welcome ' + member.mention + ', please read ' + welcome.mention +
                           ' and the pinned message in ' + rules.mention)

@bot.event
async def on_member_remove(member):
    """Say who left when someone leaves the server."""
    await bot.send_message(bot.get_channel(general_channel_id), 'Bye bye, ' + str(member))

@bot.command()
async def hello():
    """Liberty Prime says hello."""
    await bot.say("Hello, citizen.")

@bot.command(pass_context = True)
async def cookie(ctx):
    """Do any number of @mentions after the command to send those people a cookie."""
    recipients = ctx.message.mentions
    for recipient in recipients:
        await bot.say(recipient.mention + ', here\'s a cookie ' + '\U0001F36A')

@bot.command(pass_context = True)
async def freedom(ctx):
    """Do any number of @mentions after the command to send those people some freedom."""
    recipients = ctx.message.mentions
    for recipient in recipients:
        await bot.say('\U0001F4A5'+' '+'\U0001F1FA'+'\U0001F1F8'+' '+ recipient.mention +
                      ', HAVE SOME FREEDOM, COMMUNIST SCUM! '+'\U0001F1FA'+'\U0001F1F8'+' '+'\U0001F4A5')

@bot.command(pass_context = True)
async def prime(ctx):
    """Liberty Prime says a quote in a text channel, and if in one, in a voice channel."""
    quotes = []
    with open('C:\\Users\\Challice\\Documents\\Liberty-Prime-bot\\quotes.txt', 'r') as quotefile:
        for line in quotefile:
            quotes.append(line.strip())
    number = randint(0, len(quotes)-1)
    await bot.say(quotes[number])
    if bot.is_voice_connected(bot.get_server(deagles_server_id)):
        for x in bot.voice_clients:
            if x.server == ctx.message.server:
                voice = x
        wav_file = 'C:\\Users\\Challice\\Documents\\Liberty-Prime-bot\\quotes\\quote #{}.wav'.format(str(number+1))
        player = voice.create_ffmpeg_player(wav_file)
        player.start()

@bot.command()
async def join():
    """Makes Liberty Prime join the voice channel."""
    if not bot.is_voice_connected(bot.get_server(deagles_server_id)):
        voice = await bot.join_voice_channel(bot.get_channel(general_voice_channel_id))
        player = voice.create_ffmpeg_player('C:\\Users\\Challice\\Documents\\Liberty-Prime-bot\\quotes\\join.wav')
        player.start()
    else:
        await bot.say('I am already in a voice channel.')

@bot.command(pass_context = True)
async def leave(ctx):
    """Makes Liberty Prime leave the voice channel."""
    if bot.is_voice_connected(bot.get_server(deagles_server_id)):
        for x in bot.voice_clients:
            if x.server == ctx.message.server:
                return await x.disconnect()
        return await bot.say('I am not connected to any voice channel on this server.')
    else:
        return await bot.say('I am not connected to any voice channel on this server.')

@bot.command(pass_context = True)
async def addrole(ctx):
    """Adds the roles you list after the command."""
    server = bot.get_server(deagles_server_id)
    possible_roles = []
    for role in server.roles:
        if role.name not in ['Peasants', 'Mod', 'Tinkerer', 'Bot']:
            possible_roles.append(role)
    try:
        roles = []
        msg = ctx.message.content.split('addroll ')[1]
        for role in possible_roles:
            if role.name in msg and role not in ctx.message.author.roles:
                roles.append(role)
        await bot.add_roles(ctx.message.author, *roles)
        rolestring = ''
        if len(roles)>0:
            for role in roles:
                rolestring += ' {},'.format(role.name)
            await bot.say('Added to{}'.format(rolestring).strip(','))
        else:
            await bot.say('No eligible rolls to add')
    except:
        await bot.say('Problem with the input, please try again.')

@bot.command(pass_context = True)
async def removerole(ctx):
    """Removes the roles you list after the command."""
    server = bot.get_server(deagles_server_id)
    possible_roles = []
    for role in server.roles:
        if role.name not in ['Peasants', 'Mod', 'Tinkerer', 'Bot']:
            possible_roles.append(role)
    try:
        roles = []
        msg = ctx.message.content.split('removeroll ')[1]
        for role in possible_roles:
            if role.name in msg and role in ctx.message.author.roles:
                roles.append(role)
        await bot.remove_roles(ctx.message.author, *roles)
        rolestring = ''
        if len(roles)>0:
            for role in roles:
                rolestring += ' {},'.format(role.name)
            await bot.say('Removed from{}'.format(rolestring).strip(','))
        else:
            await bot.say('No eligible rolls to remove')
    except:
        await bot.say('Problem with the input, please try again.')

@bot.command(pass_context = True)
async def purge(ctx):
    """Purge a certain number of posts, or posts by one author. WIP"""
    await bot.say('Coming soon')

@bot.command(pass_context = True)
async def poll(ctx):
    """Creates a poll using you input in #polling with thumbs up, thumbs down, and shrug(for idk)."""
    try:
        polling = bot.get_channel('344566152535474186')
        question = ctx.message.content.split('!poll ')[1]
        await bot.say('Poll "{}" created in {}'.format(question, polling.mention))
        message = await bot.send_message(polling, question)
        await bot.add_reaction(message, '\N{THUMBS UP SIGN}')
        await bot.add_reaction(message, '\N{THUMBS DOWN SIGN}')
        await bot.add_reaction(message, '\U0001F937')
    except:
        await bot.say('error')

@bot.command(pass_context = True)
async def file(ctx):
    """Takes a country list text file and saves it for use in %create."""
    try:
        URL = ctx.message.attachments[0]['url']
        req = urllib.request.Request(URL, headers={'User-Agent': user_agent})
        with urllib.request.urlopen(req) as url:
            with open('country_list.txt', 'wb') as f:
                f.write(url.read())
        await bot.say('Got the file')
    except:
        await bot.say('error')

@bot.command(pass_context = True)
async def list(ctx):
    """Send the country list as a single discord message (use Shift+Space to do newline)."""
    try:
        content = ctx.message.content
        content = content.split('!list')[1]
        country_list = []
        country = ''
        for n in range(len(content)):
            country += content[n]
            if (n>0 and content[n]=='\n') or n == len(content)-1:
                country_list.append(country)
                country = ''
        country_list[0] = country_list[0][1:]
        with open('country_list.txt', 'r+') as file:
            file.truncate()
            file.writelines(country_list)
    except:
        await bot.say('error')

@bot.command(pass_context = True)
async def addtolist(ctx):
    """Use this to add one independent nation to the country list."""
    try:
        content = ctx.message.content
        country = content.split('!addtolist ')[1]
        current_list = collectCountries()
        country_list = []
        if country in country_list:
            country_list.remove(country)
            return await bot.say(country + ' is already on the list')
        else:
            await bot.say(country + ' added')
        for guy in current_list:
            country_list.append(guy.name)
        with open('country_list.txt', 'a') as file:
            if country not in country_list:
                file.write('\n'+country)
    except:
        await bot.say('error')

@bot.command(pass_context = True)
async def removefromlist(ctx):
    """Use this to add one independent nation to the country list."""
    try:
        content = ctx.message.content
        country = content.split('!removefromlist ')[1]
        current_list = collectCountries()
        country_list = []
        for guy in current_list:
            country_list.append(guy.name)
        if country in country_list:
            country_list.remove(country)
            await bot.say(country + ' removed')
        else:
            return await bot.say(country + ' is not on the list')
        with open('country_list.txt', 'r+') as file:
            file.truncate()
            for n in range(len(country_list)):
                if country_list[n] not in ['ocean','uncolonized','wasteland'] and n!=0:
                    file.writelines('\n'+country_list[n])
                elif n==0:
                    file.writelines(country_list[n])
    except:
        await bot.say('error')

@bot.command()
async def getlist():
    """Liberty Prime will say the country list as he currently has it"""
    countryList = collectCountries()
    message = ''
    for country in countryList:
        if country.name not in ['ocean','uncolonized','wasteland']:
            name = country.name
            if country.isVassal:
                name = '-'+country.name
            message = message + (name) +'\n'
    return await bot.send_message(bot.get_channel('336262010033405952'), message)

@bot.command(pass_context = True)
async def create(ctx):
    """Add this command to the additional comments line when uploading an eu4 map, it will process it and return a map with only the countries specified in the country list."""
    try:
        inputImage = 'original.png'
        outputImage = 'final.png'
        if len(ctx.message.attachments) > 0:
            await bot.say('Processing')
            URL = ctx.message.attachments[0]['url']
            req = urllib.request.Request(URL, headers={'User-Agent': user_agent})
            with urllib.request.urlopen(req) as url:
                with open(inputImage, 'wb') as f:
                    f.write(url.read())
            changeColors(inputImage).save(outputImage)
            return await bot.send_file(bot.get_channel('336262010033405952'), open(outputImage, 'rb'))
        else:
            return await bot.say('Invalid command entry, upload an image and type "%create" in the "add a comment" part')
    except:
        await bot.say('error')

@bot.command(pass_context = True)
async def shutdown(ctx):
    """The command to terminate the bot, only usable by Ghostowl657."""
    if ctx.message.author.id == '196866248984887296':
        await bot.send_message(bot.get_channel(general_channel_id), 'Initiate shutdown protocal')
        await bot.close()
    else:
        hacker = ctx.message.author
        await bot.say('Communist hacking detected, initiating freedom protocol!')
        await bot.say('\U0001F4A5'+' '+'\U0001F1FA'+'\U0001F1F8'+' '+hacker.mention+
                      ', HAVE SOME FREEDOM, COMMUNIST SCUM! '+'\U0001F1FA'+'\U0001F1F8'+' '+'\U0001F4A5')

bot.run('NTY4ODg2Nzk1MDAyMDUyNjE1.XLon0w.PIJlWT5ji5CexwTdbgLp6Q3W72E')
