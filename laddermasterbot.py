import discord
from discord.ext import commands
from discord.utils import get

from texttable import Texttable
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import sched
import os, sys
import datetime
import asyncio
import time
import pickle
import operator
import traceback
from datetime import date, timedelta, datetime

import tkfinder    # for tekken bot

# global vars
version_num = "1.6"
admin_role = "Ladder Manager"
super_admin_role = "Ladder Manager"
ladder_boss_name = "LADDER BOSS"
comm_prefix = "!"
gameNames = {
    "p+": "PROJECT+",
    "melee": "SUPER SMASH BROS MELEE",
    "ssbu": "SUPER SMASH BROS ULTIMATE",
    "sf3s": "STREET FIGHTER 3RD STRIKE",
    "ggxrd": "GUILTY GEAR XRD REV 2",
    "gbvs": "GRANBLUE VERSUS"
}
date_format = "%Y-%m-%d"
eligibleLadders = ['p+', 'melee', 'ssbu', 'sf3s', 'ggxrd', 'gbvs', 'chess']
inktober_cues = ['Ring', 'Mindless', 'Bait', 'Freeze', 'Build', 'Husky', 'Enchanted',
                 'Frail', 'Swing', 'Pattern', 'Snow', 'Dragon', 'Ash', 'Overgrown',
                 'Legend', 'Wild', 'Ornament', 'Misfit', 'Sling', 'Tread', 'Treasure',
                 'Ghost', 'Ancient', 'Dizzy', 'Tasty', 'Dark', 'Coat', 'Ride',
                 'Injured', 'Catch', 'Ripe']

# Dict for searching special move types
move_types = {  'ra': 'Rage art',
                'rage_art': 'Rage art',
                'rd': 'Rage drive',
                'rage_drive': 'Rage drive',
                'wb': 'Wall bounce',
                'wall_bounce': 'Wall bounce',
                'ts': 'Tail spin',
                'tail_spin': 'Tail spin',
                'screw': 'Tail spin',
                'homing': 'Homing',
                'homari': 'Homing',
                'armor': 'Power crush',
                'armori': 'Power crush',
                'pc': 'Power crush',
                'power': 'Power crush',
                'power_crush': 'Power crush'}

# TEKKEN STUFF ########################################
def move_embed(character, move):
    '''Returns the embed message for character and move'''
    embed = discord.Embed(title=character['proper_name'], 
            colour=0x00EAFF,
            url=character['online_webpage'],
            description='Move: ' + move['Command'])
    
    embed.set_thumbnail(url=character['portrait'])
    embed.add_field(name='Property', value=move['Hit level'])
    embed.add_field(name='Damage', value=move['Damage'])
    embed.add_field(name='Startup', value='i' + move['Start up frame'])
    embed.add_field(name='Block', value=move['Block frame'])
    embed.add_field(name='Hit', value=move['Hit frame'])
    embed.add_field(name='Counter Hit', value=move['Counter hit frame'])
    embed.add_field(name='Notes', value=move['Notes'])
    
    return embed

def move_list_embed(character, move_list, move_type):
    '''Returns the embed message for a list of moves matching to a special move type'''
    desc_string = ''
    for move in move_list:
        desc_string += move + '\n'

    embed = discord.Embed(title=character['proper_name'] + ' ' + move_type.lower() + ':',
            colour=0x00EAFF,
            description=desc_string)

    return embed

def error_embed(err):
    embed = discord.Embed(title='Error',
            colour=0xFF4500,
            description=err)

    return embed
### TEKKEN STUFF #################################

# try:

# except Exception:
#     traceback.print_exc()

class player:
    def __init__(self, tag, discordid):
        self.tag = tag
        self.characters = []
        self.discordid = discordid
        self.confirmId = ""
        self.challengeId = ""
        self.challengeMember = ""

class playerNew:
    def __init__(
        self,
        tag,
        _discordid,
        _characters=[],
        _confirmId="",
        _challengeId="",
        _challengeMember="",
        _lastPositionChangeDate="2019-07-02",
    ):
        self.tag = tag
        self.characters = _characters
        self.discordid = _discordid
        self.confirmId = _confirmId
        self.challengeId = _challengeId
        self.challengeMember = _challengeMember
        self.winlossData = {}
        self.lastPositionChangeDate = _lastPositionChangeDate

class playerNew2:
    def __init__(
        self,
        tag,
        _discordid,
        _characters=[],
        _confirmId="",
        _challengeId="",
        _challengeMember="",
        _lastPositionChangeDate=str(date.today()),
    ):
        self.tag = tag
        self.characters = _characters
        self.discordid = _discordid
        self.confirmId = _confirmId
        self.challengeId = _challengeId
        self.challengeMember = _challengeMember
        self.winlossData = {}
        self.lastPositionChangeDate = _lastPositionChangeDate
        self.gameWins = 0
        self.gameLosses = 0
        self.setWins = 0
        self.setLosses = 0
        self.scoreProposed = ""

# adds winstreak attribute
class playerNew3:
    def __init__(
        self,
        tag,
        _discordid,
        _characters=[],
        _confirmId="",
        _challengeId="",
        _challengeMember="",
        _lastPositionChangeDate=str(date.today()),
        _gameWins=0,
        _gameLosses=0,
        _setWins=0,
        _setLosses=0,
        _scoreProposed=""
    ):
        self.tag = tag
        self.characters = _characters
        self.discordid = _discordid
        self.confirmId = _confirmId
        self.challengeId = _challengeId
        self.challengeMember = _challengeMember
        self.lastPositionChangeDate = _lastPositionChangeDate
        self.gameWins = _gameWins
        self.gameLosses = _gameLosses
        self.setWins = _setWins
        self.setLosses = _setLosses
        self.winstreak = 0
        self.scoreProposed = _scoreProposed


# helper function, saves ladders to pkl
def saveLadders(ladders):
    # UPDATES THE PLAYER CLASS TO A NEW CLASS WITH MORE VARIABLES if necessary
    for _game in ladders:
        for i, _player in enumerate(ladders[_game]):
            # upgrades players to playernew if needed
            if str(type(_player)) == "<class '__main__.player'>":
                ladders[_game][i] = playerNew(
                    _player.tag,
                    _player.discordid,
                    _player.characters,
                    _player.confirmId,
                    _player.challengeId,
                    _player.challengeMember,
                )
            # upgrades playerNew to playerNew2
            if str(type(_player)) == "<class '__main__.playerNew'>":
                ladders[_game][i] = playerNew2(
                    _player.tag,
                    _player.discordid,
                    _player.characters,
                    _player.confirmId,
                    _player.challengeId,
                    _player.challengeMember,
                )
            # upgrades playerNew2 to playerNew3
            if str(type(_player)) == "<class '__main__.playerNew2'>":
                ladders[_game][i] = playerNew3(
                    _player.tag,
                    _player.discordid,
                    _player.characters,
                    _player.confirmId,
                    _player.challengeId,
                    _player.challengeMember,
                    _player.lastPositionChangeDate,
                    _player.gameWins,
                    _player.gameLosses,
                    _player.setWins,
                    _player.setLosses,
                    _player.scoreProposed
                )
    
    with open("ladders.pkl", "wb") as output:
        pickle.dump(ladders, output, pickle.HIGHEST_PROTOCOL)
    try:
        updateSheet(ladders)
    except:
        pass

# helper function, loads ladders from pkl
def loadLadders():
    with open("ladders.pkl", "rb") as input:
        ladders = pickle.load(input)
        return ladders

TOKEN = ""
f = open("key.txt", "r")
if f.mode == "r":
    TOKEN = f.read()

bot = commands.Bot(command_prefix=comm_prefix, case_insensitive=True)
bot.remove_command("help")

# error handler (mutes errors so comment this out when debugging)
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        if str(ctx.command) == "addMember":
            await ctx.send("That player was not found")

    if isinstance(error, commands.MissingRole):
        await ctx.send("You don't have permission to use this command YOU IDIOT.")
    # if isinstance(error, commands.CommandNotFound):   # temporarily muted to help with tekken
    #     await ctx.send(
    #         "That command doesn't exist, type !help or !helpadmin for a list of commands"
    #     )
    if isinstance(error, commands.MissingRequiredArgument):
        if str(ctx.command) == "ladder":
            await ctx.send("The correct usage is !ladder <game> or !l <game>")
        if str(ctx.command) == "ladderDetailed":
            await ctx.send("The correct usage is !ladderDetailed <game> or !ld <game>")
        if str(ctx.command) == "ladderStats":
            await ctx.send("The correct usage is !ladderStats <game> or !ls <game>")
        if str(ctx.command) == "joinLadder":
            await ctx.send("The correct usage is !joinLadder <tag> <game>")
        if str(ctx.command) == "quitLadder":
            await ctx.send("The correct usage is !quitLadder <game>")
        if str(ctx.command) == "changeTag":
            await ctx.send("The correct usage is !changeLadder <newTag> <game>")
        if str(ctx.command) == "addCharacter":
            await ctx.send("The correct usage is !addCharacter <character> <game>")
        if str(ctx.command) == "clearCharacters":
            await ctx.send("The correct usage is !clearCharacters <game>")
        if str(ctx.command) == "beat":
            await ctx.send("The correct usage is !beat <@opponent> <score> <game>")
        if str(ctx.command) == "confirm":
            await ctx.send("The correct usage is !confirm <@opponent> <score> <game>")
        if str(ctx.command) == "deny":
            await ctx.send("The correct usage is !deny <@opponent> <game>")
        if str(ctx.command) == "addMember":
            await ctx.send("The correct usage is !addMember <@player> <tag> <game>")
        if str(ctx.command) == "removeMember":
            await ctx.send("The correct usage is !removeMember <@player> <game>")
        if str(ctx.command) == "moveUp":
            await ctx.send("The correct usage is !moveUp <@player> <game>")
        if str(ctx.command) == "moveDown":
            await ctx.send("The correct usage is !moveDown <@player> <game>")
        if str(ctx.command) == "addLadder":
            await ctx.send("The correct usage is !addLadder <game>")
        if str(ctx.command) == "removeLadder":
            await ctx.send("The correct usage is !removeLadder <game>")
        if str(ctx.command) == "changeLadderName":
            await ctx.send("The correct usage is !changeLadderName <oldname> <newname>")

### TEKKEN STUFF ###########################################
@bot.event
async def on_message(message):
    '''This has the main functionality of the bot. It has a lot of
    things that would be better suited elsewhere but I don't know
    if I'm going to change it.
    '''
    channel = message.channel
    if message.content.startswith('!') and (channel.name == '3dfighters' or channel.name == 'test-chamber-2'):

        user_message = message.content
        user_message = user_message.replace('!', '')
        user_message_list = user_message.split(' ', 1)

        if len(user_message_list) <= 1:
            # malformed command
            return

        chara_name = user_message_list[0].lower()
        chara_move = user_message_list[1]
        if chara_name == 'armor' or chara_name == 'ak':
            chara_name = 'armor_king'
        elif chara_name == 'dj' or chara_name == 'dvj' or chara_name == 'djin' or chara_name == 'devil' or chara_name == 'deviljin' or chara_name == 'diablojim' or chara_name == 'taika-jim':
            chara_name = 'devil_jin'
        elif chara_name == 'sergei' or chara_name == 'drag' or chara_name == 'dragu':
            chara_name = 'dragunov'
        elif chara_name == 'goose':
            chara_name = 'geese'
        elif chara_name == 'hwo' or chara_name == 'hwoa':
            chara_name = 'hwoarang'
        elif chara_name == 'jack':
            chara_name = 'jack7'
        elif chara_name == 'julle':
            chara_name = 'julia'
        elif chara_name == 'chloe' or chara_name == 'lc' or chara_name == 'lucky':
            chara_name = 'lucky_chloe'
        elif chara_name == 'hei' or chara_name == 'hessu' or chara_name == 'heiska':
            chara_name = 'heihachi'
        elif chara_name == 'kata' or chara_name == 'kat':
            chara_name = 'katarina'
        elif chara_name == 'kaz' or chara_name == 'kazze':
            chara_name = 'kazuya'
        elif chara_name == 'karhu' or chara_name == 'panda':
            chara_name = 'kuma'
        elif chara_name == 'mara':
            chara_name = 'marduk'
        elif chara_name == 'master' or chara_name == 'raven' or chara_name == 'mraven' or chara_name == 'masterraven':
            chara_name = 'master_raven'
        elif chara_name == 'nocto':
            chara_name = 'noctis'
        elif chara_name == 'pave':
            chara_name = 'paul'
        elif chara_name == 'sha':
            chara_name = 'shaheen'
        elif chara_name == 'yoshi':
            chara_name = 'yoshimitsu'
        elif chara_name == 'ling':
           chara_name = 'xiaoyu'

        character = tkfinder.get_character(chara_name)
        if character is not None:
            if chara_move.lower() in move_types:
                chara_move = chara_move.lower()
                move_list = tkfinder.get_by_move_type(character, move_types[chara_move])
                if  len(move_list) < 1:
                    embed = error_embed('No ' + move_types[chara_move].lower() + ' for ' + character['proper_name'])
                    msg = await channel.send(embed=embed, delete_after=150)
                elif len(move_list) == 1:
                    move = tkfinder.get_move(character, move_list[0], False)
                    embed = move_embed(character, move)
                    msg = await channel.send(embed=embed, delete_after=300)
                elif len(move_list) > 1:
                    embed = move_list_embed(character, move_list, move_types[chara_move])
                    msg = await channel.send(embed=embed, delete_after=300)

            else:
                move = tkfinder.get_move(character, chara_move, True)
            
                #First checks the move as case sensitive, if it doesn't find it
                #it checks it case unsensitive
            
                if move is not None:
                    embed = move_embed(character, move) 
                    msg = await channel.send(embed=embed, delete_after=300)
                else:
                    move = tkfinder.get_move(character, chara_move, False)
                    if move is not None:
                        embed = move_embed(character, move)
                    
                        msg = await channel.send(embed=embed, delete_after=300)
                    else:
                        embed = error_embed('Move not found: ' + chara_move)
                        msg = await channel.send(embed=embed, delete_after=150)
        else:
            bot_msg = 'Character ' + chara_name + ' does not exist.'
            embed = error_embed(bot_msg)
            msg = await message.channel.send(embed=embed, delete_after=150)

            return
    await bot.process_commands(message)
### TEKKEN STUFF ##############################

# version
@bot.command()
async def version(ctx):
    await ctx.send("Current version is " + version_num)


# help
@bot.command(aliases=["h"])
async def help(ctx):
    ladders = loadLadders()
    msg = """```Commands:
- !ladder <game>: displays ladder (shortcut: !l)

- !ladderDetailed <game>: displays ladder with detailed player info (shortcut: !ld)

- !ladderstats <game>: displays ladder with player statistics (shortcut:!ls)

- !joinLadder <tag> <game>: allows you to join a ladder

- !quitLadder <game>: allows you to quit a ladder

- !changeTag <new tag> <game>: changes your tag for a certain game

- !addCharacter <character> <game>: adds ONE character to your list of characters

- !clearCharacters <game>: clears ALL characters from your list of characters

- !beat <@opponent> <score> <game>: initiates a rank swap between you and someone you beat, put winner's score first (e.g. 3-0 NOT 0-3)

- !confirm <@opponent> <score> <game>: accepts a rank swap, put winner's score first (e.g. 3-0 NOT 0-3)

- !deny <@opponent> <game>: denies a rank swap

The current possible games are:"""
    for key in ladders:
        msg += "'" + key + "'" + ", "
        msg = msg[:-2]
    msg += ".\n"
    msg += "```"
    await ctx.send(msg)


# help for admins
@bot.command()
@commands.has_role(admin_role)
async def helpadmin(ctx):
    msg = """```Ladder Manager commands:
- !addMember <@player> <tag> <game>: adds a member to a ladder

- !removeMember <@player> <game>: removes a member from a ladder

- !moveUp <@player> <tag> <game>: moves someone up a rank

- !moveDown <@player> <tag> <game>: moves someone down a rank

- !resetChallenge <@player> <game>: resets a player's challenge id, for debugging

- !addLadder <game>: adds a ladder (will need to add spreadsheet tab manually) (illuminati only)

- !removeLadder <game>: removes a ladder (will need to remove from spreadsheet tab manually) (illuminati only)

- !changeLadderName <oldName> <newName>: changes name of ladder"""
    msg += "```"
    await ctx.send(msg)


# joins a particular ladder
@bot.command()
async def joinLadder(ctx, tag, ladderName):
    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = "Correct usage is !joinLadder <tag> <game>.\n" "Possible games are: "
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return

    _player = playerNew2(
        tag, "{0}".format(ctx.author), _lastPositionChangeDate=str(date.today())
    )

    add = True
    for i in ladderData:
        if i.discordid == "{0}".format(ctx.author):
            add = False
            await ctx.send("You're already in this ladder.")
            return

    if add:
        ladderData.append(_player)
        saveLadders(ladders)

    msg = "{}".format(ctx.author)
    msg += " has joined the " + ladderName + " ladder as '"
    msg += tag + "'."

    await ctx.send(msg)


# quits a ladder
@bot.command()
async def quitLadder(ctx, ladderName):
    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = "Correct usage is !quitLadder <game>.\n" "Possible games are: "
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return

    # get player info
    _player = None
    for i in ladderData:
        if str(i.discordid) == str(ctx.author):
            _player = i

    # if player doesn't exist:
    if _player == None:
        await ctx.send("You're not in this ladder.")
        return

    ladderData.remove(_player)
    saveLadders(ladders)

    msg = "{}".format(ctx.author)
    msg += " has quit the " + ladderName + " ladder."

    await ctx.send(msg)


# changes player tag
@bot.command()
async def changeTag(ctx, newTag, ladderName):
    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = (
            "Correct usage is !changeTag <new_tag> <game>.\n" "Possible games are: "
        )
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return

    # get player info
    _player = None
    for i in ladderData:
        if str(i.discordid) == str(ctx.author):
            _player = i

    # if player doesn't exist:
    if _player == None:
        await ctx.send("You're not in this ladder.")
        return

    _player.tag = newTag
    saveLadders(ladders)

    msg = "{}".format(ctx.author)
    msg += " has changed their tag to " + newTag + "."

    await ctx.send(msg)


# adds a character to character list
@bot.command()
async def addCharacter(ctx, char, ladderName):
    ladders = loadLadders()
    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = (
            "Correct usage is !addCharacter <character> <game>.\n"
            "Possible games are: "
        )
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return

    for i in ladderData:
        if str(i.discordid) == str(ctx.author):
            i.characters.append(char)

    saveLadders(ladders)
    await ctx.send("{} added to character list for ".format(char) + ladderName + ".")


# clears character list for a certain game
@bot.command()
async def clearCharacters(ctx, ladderName):
    ladders = loadLadders()
    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = "Correct usage is !clearCharacters <game>.\n" "Possible games are: "
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return

    for i in ladderData:
        if str(i.discordid) == str(ctx.author):
            i.characters.clear()

    saveLadders(ladders)
    await ctx.send("Character list cleared for " + ladderName + ".")

    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = "Correct usage is !ladder <game>.\n" "Possible games are: "
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return

    gameNames = {
            "p+": "PROJECT+",
            "melee": "SUPER SMASH BROS MELEE",
            "ssbu": "SUPER SMASH BROS ULTIMATE",
            "sf3s": "STREET FIGHTER 3RD STRIKE",
            "ggxrd": "GUILTY GEAR XRD REV 2",
            "gbvs": "GRANBLUE VERSUS"
    }

    try:
        gameName = gameNames[ladderName]
    except KeyError:
        gameName = ladderName.upper()

    # adaptive text formatting rofl
    msg = "Sheet Link: <http://tinyurl.com/qfgcladdersheet>\n```\n------------------"
    for i in range(0, len(gameName)):
        msg += "-"
    msg += "\n-- QFGC " + gameName + " LADDER --\n"
    for i in range(0, len(gameName)):
        msg += "-"
    msg += "------------------\n\n"

    ###### minimalist version to display players in ladder #####
    rank_counter = 1
    for _player in ladderData:
        # add row to table
        msg += str(rank_counter) + ") " + _player.discordid + "\n"
        rank_counter += 1

    msg += "```"

    await ctx.send(msg)


# display ladder info
@bot.command(aliases=["l"])
async def ladder(ctx, ladderName):
    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = (
            "Correct usage is !ladder <game> or !l <game>.\n" "Possible games are: "
        )
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        if ladderName == "smush":
            await ctx.send("WARNING: 'SMUSH' IS A BANNABLE WORD.")
        return

    try:
        gameName = gameNames[ladderName]
    except KeyError:
        gameName = ladderName.upper()

    # adaptive text formatting rofl
    for i in range(0, len(gameName)):
        msg += "-"
    msg += "\n-- QFGC " + gameName + " LADDER --\n"
    for i in range(0, len(gameName)):
        msg += "-"
    msg += "------------------\n\n"

    msg += "Ladder boss: " + ladderData[0].discordid + "\n"
    msg += "Title defends: " + str(ladderData[0].winstreak) + "\n"

    ###### minimalist version to display players in ladder #####
    rank_counter = 1
    for _player in ladderData:
        # add row to table
        msg += str(rank_counter) + ") " + _player.discordid + "\n"
        rank_counter += 1

    msg += "```"

    await ctx.send(msg)


# display detailed ladder info
@bot.command(aliases=["ld"])
async def ladderDetailed(ctx, ladderName):
    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = (
            "Correct usage is !ladderDetailed <game> or !ld <game>.\n"
            "Possible games are: "
        )
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        if ladderName == "smush":
            await ctx.send("WARNING: 'SMUSH' IS A BANNABLE WORD.")
        return

    try:
        gameName = gameNames[ladderName]
    except KeyError:
        gameName = ladderName.upper()

    # adaptive text formatting rofl
    for i in range(0, len(gameName)):
        msg += "-"
    msg += "\n-- QFGC " + gameName + " LADDER --\n"
    for i in range(0, len(gameName)):
        msg += "-"
    msg += "------------------\n\n"

    msg += "Ladder boss: " + ladderData[0].discordid + "\n"
    msg += "Title defends: " + str(ladderData[0].winstreak) + "\n"

    ###### verbose table ######
    # intialize table
    rows = []
    header = ["", "Tag", "Character(s)", "Discord"]
    rows.append(header)  # header with tag

    # display players in ladder
    rank_counter = 1
    for _player in ladderData:

        # format player character list
        chars = ""
        if len(_player.characters) == 0:  # no characters
            chars = "???"
        else:
            for char in _player.characters:
                chars += char + ", "
            chars = chars[:-2]

        # add row to table
        rows.append([rank_counter, _player.tag, chars, _player.discordid])
        rank_counter += 1

    # render table        
    else:
        rankTable = Texttable()
        rankTable.add_rows(rows)
        testmsg = msg + rankTable.draw()
        testmsg += "```"
        # rerender if too long
        if len(testmsg) > 1900:
            rowsTopHalf = rows[0:len(rows) // 2]
            rowsBotHalf = rows[len(rows) // 2:]
            rowsBotHalf.insert(0, header)

            rankTableTopHalf = Texttable()
            rankTableTopHalf.add_rows(rowsTopHalf)
            rankTableBotHalf = Texttable()
            rankTableBotHalf.add_rows(rowsBotHalf)

            msgTopHalf = msg + rankTableTopHalf.draw() + "```"
            msgBotHalf = "```" + rankTableBotHalf.draw() + "```"

            await ctx.send(msgTopHalf)
            await ctx.send(msgBotHalf)
        # testmsg is fine
        else:
            msg = testmsg
            await ctx.send(msg)


# display ladder stats
@bot.command(aliases=["ls"])
async def ladderStats(ctx, ladderName):
    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = (
            "Correct usage is !ladderStats <game> or !ls <game>.\n"
            "Possible games are: "
        )
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        if ladderName == "smush":
            await ctx.send("WARNING: 'SMUSH' IS A BANNABLE WORD.")
        return

    try:
        gameName = gameNames[ladderName]
    except KeyError:
        gameName = ladderName.upper()

    # adaptive text formatting rofl
    for i in range(0, len(gameName)):
        msg += "-"
    msg += "\n-- QFGC " + gameName + " LADDER --\n"
    for i in range(0, len(gameName)):
        msg += "-"
    msg += "------------------\n\n"

    msg += "Ladder boss: " + ladderData[0].discordid + "\n"
    msg += "Title defends: " + str(ladderData[0].winstreak) + "\n"

    ###### verbose table ######
    # intialize table
    rows = []
    header = ["", "Discord", "Rank Held For:", "Game W/L", "Set W/L"]
    rows.append(header)  # header with tag

    # display players in ladder
    rank_counter = 1
    for _player in ladderData:

        # format player character list
        timeSpent = (
            date.today()
            - datetime.strptime(_player.lastPositionChangeDate, date_format).date()
        )
        timeSpent = timeSpent.days
        timeSpent = str(timeSpent) + " days"

        # format w/l data
        wlgames = str(_player.gameWins) + ":" + str(_player.gameLosses)
        wlsets = str(_player.setWins) + ":" + str(_player.setLosses)

        # add row to table
        rows.append([rank_counter, _player.discordid, timeSpent, wlgames, wlsets])
        rank_counter += 1

    # render table        
    else:
        rankTable = Texttable()
        rankTable.add_rows(rows)
        testmsg = msg + rankTable.draw()
        testmsg += "```"
        # rerender if too long
        if len(testmsg) > 1900:
            rowsTopHalf = rows[0:len(rows) // 2]
            rowsBotHalf = rows[len(rows) // 2:]
            rowsBotHalf.insert(0, header)

            rankTableTopHalf = Texttable()
            rankTableTopHalf.add_rows(rowsTopHalf)
            rankTableBotHalf = Texttable()
            rankTableBotHalf.add_rows(rowsBotHalf)

            msgTopHalf = msg + rankTableTopHalf.draw() + "```"
            msgBotHalf = "```" + rankTableBotHalf.draw() + "```"

            await ctx.send(msgTopHalf)
            await ctx.send(msgBotHalf)
        # testmsg is fine
        else:
            msg = testmsg
            await ctx.send(msg)


# initiates swap between two players
@bot.command()
async def beat(ctx, loser: discord.Member, score, ladderName):  # score is 'x-x' string
    ladders = loadLadders()

    # check that scores were entered properly
    winScore = 0
    lossScore = 0
    if (
        len(score) == 3
        and score[1] == "-"
        and score[0].isdigit()
        and score[2].isdigit()
    ):
        winScore = score[0]
        lossScore = score[2]
        if lossScore > winScore:
            lossScore, winScore = winScore, lossScore
    else:
        errmsg = (
            "Correct usage is !confirm <@opponent> <score> <game>\n"
            "Possible games are: "
        )
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        errmsg = "Score must be input as number hyphen number. eg: 3-0, with WINNER'S SCORE FIRST"
        await ctx.send(errmsg)
        return

    # error for beating oneself
    if str(loser) == str(ctx.author):
        await ctx.send("You can't beat yourself you doofus")
        return

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = (
            "Correct usage is !beat <@opponent> <score> <game>.\n"
            "Possible games are: "
        )
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return

    # get player info
    for i in ladderData:
        if str(i.discordid) == str(ctx.author):
            winner = i
        if str(i.discordid) == str(loser):
            loser_discord = loser
            loser = i

    # check that player is in ladder
    try:
        ladderData.index(winner)
    except:
        await ctx.send("You are not on the " + ladderName + " ladder.")
        return

    try:
        ladderData.index(loser)
    except:
        await ctx.send("That person is not on the " + ladderName + " ladder.")
        return

    # send confirmation
    if str(winner.confirmId) == "":
        winner.confirmId = loser.discordid  # update confirm id
        winner.scoreProposed = score  # update confirm score
        await ctx.send(
            loser_discord.mention
            + " please type !confirm <@opponent> <score> <game> or !deny <@opponent> <game> to validate the set results. Reminder that scores have to match."
        )
    else:
        await ctx.send(
            "You must wait until your last opponent confirms the results of your set"
        )

    saveLadders(ladders)


# confirms result of set
@bot.command()
async def confirm(ctx, winner: discord.Member, score, ladderName):
    try:
        ladders = loadLadders()

        # check that scores were entered properly
        winScore = 0
        lossScore = 0
        if (
            len(score) == 3
            and score[1] == "-"
            and score[0].isdigit()
            and score[2].isdigit()
        ):
            winScore = score[0]
            lossScore = score[2]
            if lossScore > winScore:
                lossScore, winScore = winScore, lossScore
        else:
            errmsg = (
                "Correct usage is !confirm <@opponent> <score> <game>\n"
                "Possible games are: "
            )
            for key in ladders:
                errmsg += "'" + key + "'" + ", "
            errmsg = errmsg[:-2]
            errmsg += ". "
            await ctx.send(errmsg)

            errmsg = "Score must be input as number hyphen number. eg: 3-0, with WINNER'S SCORE FIRST"
            await ctx.send(errmsg)
            return

        try:
            ladderName = ladderName.lower()
            ladderData = ladders[ladderName]
        except KeyError:
            errmsg = (
                "Correct usage is !confirm <@opponent> <score> <game>\n"
                "Possible games are: "
            )
            for key in ladders:
                errmsg += "'" + key + "'" + ", "
            errmsg = errmsg[:-2]
            errmsg += ". "
            await ctx.send(errmsg)
            return

        # get player info
        for i in ladderData:
            if str(i.discordid) == str(ctx.author):
                loser = i
            if str(i.discordid) == str(winner):
                _winner = i

        # update stats and swap if needed
        if _winner.confirmId == loser.discordid:

            # check scores match
            if score != _winner.scoreProposed:
                errmsg = (
                "Correct usage is !confirm <@opponent> <score> <game>\n"
                "Possible games are: "
                )
                for key in ladders:
                    errmsg += "'" + key + "'" + ", "
                errmsg = errmsg[:-2]
                errmsg += ". "
                await ctx.send(errmsg)

                await ctx.send("The proposed scores don't match, please try again.")
                return

            loser_old_rank = ladderData.index(loser)
            winner_old_rank = ladderData.index(_winner)
            # # update winLossData
            # windata = _winner.winlossData
            # lossdata = loser.winlossData

            # winDictPair = windata.setdefault(loser.discordid, [])
            # lossDictPair = lossdata.setdefault(_winner.discordid, [])

            # winDictPair.append([str(winScore + "-" + lossScore), time.time()])
            # lossDictPair.append([str(lossScore + "-" + winScore), time.time()])

            # update cumulative totals
            _winner.gameWins += int(winScore)
            _winner.gameLosses += int(lossScore)
            loser.gameLosses += int(winScore)
            loser.gameWins += int(lossScore)
            _winner.setWins += 1
            loser.setLosses += 1

            # check rank difference
            if loser_old_rank > winner_old_rank:
                # no need to swap
                _winner.confirmId = ""
                loser.confirmId = ""
                _winner.scoreProposed = ""
                await ctx.send("Set results confirmed. w/l data has been recorded, ranks didn't need swapping. Thank you for reporting your match results!")
                if winner_old_rank == 0:
                    _winner.winstreak += 1
                    await ctx.send("Ladder boss winstreak has improved by 1")
            else:
                # swap ranks
                ladderData[loser_old_rank] = _winner
                ladderData[winner_old_rank] = loser
                _winner.confirmId = ""
                loser.confirmId = ""
                _winner.scoreProposed = ""
                _winner.lastPositionChangeDate = str(date.today())
                loser.lastPositionChangeDate = str(date.today())
                await ctx.send("Set results confirmed. Ranks have been swapped, and w/l data has been recorded.")

                # new ladder boss if ladder is eligible
                if loser_old_rank == 0 and ladderName in eligibleLadders:
                    game_role_name = ladderName.upper() + " " + ladder_boss_name
                    game_role = get(ctx.author.guild.roles, name=game_role_name)

                    await winner.add_roles(game_role)
                    await ctx.author.remove_roles(game_role)
                    
                    # check if author is a ladder boss in another game before removing role
                    loser_boss_titles = 0
                    for eligibleGame in eligibleLadders:
                        tempLadder = ladders[eligibleGame]
                        if tempLadder[0].discordid == str(ctx.author):
                            loser_boss_titles += 1

                    print(loser_boss_titles)
                    if loser_boss_titles < 1:
                        await ctx.author.remove_roles(boss_role)

                    boss_msg = "Congratulations to " + _winner.discordid + " for becoming the new " + ladderName + " Ladder Boss!"
                    await ctx.send(boss_msg)
        else:
            await ctx.send("You don't have any pending sets against this person")
    except:
        e = traceback.format_exc()
        await ctx.send(e)

    saveLadders(ladders)


# denies the result of a set
@bot.command()
async def deny(ctx, winner: discord.Member, ladderName):
    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = "Correct usage is !deny <@opponent> <game>\n" "Possible games are: "
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return

    # get player info
    for i in ladderData:
        if str(i.discordid) == str(ctx.author):
            loser = i
        if str(i.discordid) == str(winner):
            winner = i

    if winner.confirmId == loser.discordid:
        loser.confirmId = ""
        winner.confirmId = ""
        await ctx.send("Set results have been invalidated")
    else:
        await ctx.send("You don't have any pending sets against this person")

    saveLadders(ladders)


# resets challenge id for a player for a game
@bot.command()
@commands.has_role(admin_role)
async def resetChallenge(ctx, _player: discord.Member, ladderName):
    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = (
            "Correct usage is !resetChallenge <@player> <game>.\n"
            "Possible games are: "
        )
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return

    _player = None
    for ladderName, ladderData in ladders.items():
        for i in ladderData:
            if str(i.discordid) == str(ctx.author):
                _player = i
                _player.confirmId = ""
                saveLadders(ladders)


# adds another player to ladder (admin only)
@bot.command()
@commands.has_role(admin_role)
async def addMember(ctx, new_player: discord.Member, tag, ladderName):
    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = (
            "Correct usage is !addMember <@player> <tag> <game>.\n"
            "Possible games are: "
        )
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return

    # code essentially same as !joinLadder
    _player = playerNew2(
        tag, "{0}".format(new_player), _lastPositionChangeDate=str(date.today())
    )

    add = True
    for i in ladderData:
        if i.discordid == "{0}".format(new_player):
            add = False
            await ctx.send("Player is already in this ladder.")
            return

    if add:
        ladderData.append(_player)
        saveLadders(ladders)

    msg = _player.discordid
    msg += " has joined the " + ladderName + " ladder as '"
    msg += tag + "'."

    await ctx.send(msg)


# removes player from ladder (admin only)
@bot.command()
@commands.has_role(admin_role)
async def removeMember(ctx, target_player: discord.Member, ladderName):
    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = (
            "Correct usage is !removeMember <@player> <game>.\n" "Possible games are: "
        )
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return

    # code essentially same as !quitladder
    # get player info
    _player = None
    for i in ladderData:
        if str(i.discordid) == str(target_player):
            _player = i

    # if player doesn't exist:
    if _player == None:
        await ctx.send("Player is not in this ladder.")
        return

    ladderData.remove(_player)
    saveLadders(ladders)

    msg = "{}".format(target_player)
    msg += " has been removed from the " + ladderName + " ladder."

    await ctx.send(msg)


# moves player up a ranking (admin only)
@bot.command()
@commands.has_role(admin_role)
async def moveUp(ctx, _player: discord.Member, ladderName):
    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = "Correct usage is !moveUp <@player> <game>.\n" "Possible games are: "
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return

    # get player info
    for i in ladderData:
        if str(i.discordid) == str(_player):
            _player = i

    # shuffle player up
    old_player_idx = ladderData.index(_player)
    if old_player_idx == 0:
        await ctx.send("Player already rank 1")
    else:
        temp = ladderData[old_player_idx]
        ladderData[old_player_idx] = ladderData[old_player_idx - 1]
        ladderData[old_player_idx - 1] = temp
        saveLadders(ladders)
        await ctx.send("Player shuffled up")


# moves player down a ranking (admin only)
@bot.command()
@commands.has_role(admin_role)
async def moveDown(ctx, _player: discord.Member, ladderName):
    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = "Correct usage is !moveDown <@player> <game>.\n" "Possible games are: "
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return

    # get player info
    for i in ladderData:
        if str(i.discordid) == str(_player):
            _player = i

    # shuffle player up
    old_player_idx = ladderData.index(_player)
    if old_player_idx == len(ladderData) - 1:
        await ctx.send("Player already ranked bottom")
    else:
        temp = ladderData[old_player_idx]
        ladderData[old_player_idx] = ladderData[old_player_idx + 1]
        ladderData[old_player_idx + 1] = temp
        saveLadders(ladders)
        await ctx.send("Player shuffled down")


# adds a ladder
@bot.command()
@commands.has_role(super_admin_role)
async def addLadder(ctx, ladderName):
    ladders = loadLadders()

    ladderName = ladderName.lower()
    ladders[ladderName] = []

    await ctx.send("The " + ladderName + " ladder has been created.")

    saveLadders(ladders)


# removes a ladder
@bot.command()
@commands.has_role(super_admin_role)
async def removeLadder(ctx, ladderName):
    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = "Correct usage is removeLadder <game>.\n" "Possible games are: "
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return

    ladders.pop(ladderName)

    await ctx.send("The " + ladderName + " ladder has been removed.")

    saveLadders(ladders)


# changes name of ladder
@bot.command()
@commands.has_role(admin_role)
async def changeLadderName(ctx, oldName, newName):
    ladders = loadLadders()

    try:
        oldName = oldName.lower()
        ladderData = ladders[oldName]
    except KeyError:
        errmsg = (
            "Correct usage is changeLadderName <oldName> <newName>.\n"
            "Possible games are: "
        )
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return

    ladders[newName] = ladders.pop(oldName)

    await ctx.send(oldName + " has been renamed to " + newName)

    saveLadders(ladders)
    
# sets various attributes
@bot.command()
async def setAttr(ctx, _player: discord.Member, ladderName, attrName, newValue):
    ladders = loadLadders()
    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = (
            "wrong args.\n"
            "Possible games are: "
        )
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return
    
    # get player info
    for i in ladderData:
        if str(i.discordid) == str(_player):
            _player = i
    
    if attrName == 'gameWins':
        _player.gameWins = int(newValue)
    elif attrName == 'gameLosses':
        _player.gameLosses = int(newValue)
    elif attrName == 'setWins':
        _player.setWins = int(newValue)
    elif attrName == 'setLosses':
        _player.setLosses = int(newValue)

    saveLadders(ladders)
    await ctx.send("Attribute changed.")

# inktober
@bot.command()
async def inktober(ctx):

    date_delta = (date.today() - datetime.strptime("2019-10-01", date_format).date()).days

    if date_delta > 30:
        msg = "Inktober is over, come back next year!"
    else:
        msg = "Welcome to Inktober! Today's cue is: **"
        msg += inktober_cues[date_delta]
        msg += "**. Happy drawing!"
        
    await ctx.send(msg)

# SPREADSHEET PART OF THE CODE ---------------------------------------------------------------------------------------
def updateSheet(ladders):
#     ladders = loadLadders()

#     # use creds to create a client to interact with the Google Drive API
#     scope = [
#         "https://spreadsheets.google.com/feeds",
#         "https://www.googleapis.com/auth/drive",
#     ]
#     creds = ServiceAccountCredentials.from_json_keyfile_name(
#         "client_secret.json", scope
#     )
#     client = gspread.authorize(creds)

#     sheet = client.open("QFGC Linear Ladder Sheets")

#     # iterate over ladder dict
#     for ladderName, ladderData in ladders.items():
#         ladderSheet = sheet.worksheet(ladderName)

#         # clear cells F13:I33
#         cell_list = ladderSheet.range('F13:I33')

#         xx = 0
#         yy = 0

#         for cell in cell_list:
#             cell.value = ''

#             yy = cell.row-13
#             xx = cell.col-6
#             if yy < len(ladderData):
#                 if xx == 0:
#                     cell.value = yy+1
#                 elif xx == 1:
#                     cell.value = ladderData[yy].tag
#                 elif xx == 2:
#                     cList = ""
#                     for c in ladderData[yy].characters:
#                         cList += c + ", "

#                     cList = cList[:-2]
#                     cell.value = cList
#                 elif xx == 3:
#                     cell.value = ladderData[yy].discordid

#         ladderSheet.update_cells(cell_list)
    return


if __name__ == "__main__":
    bot.run(TOKEN)


#### TABLED CODE ######

# challenges another player to a duel
# @bot.command()
# async def challenge(ctx, target: discord.Member):
#     tableData = loadLadders()

#     p1 = ""
#     p2 = ""
#     for i in tableData:
#         if str(i.discordid) == str(ctx.author):
#             p1 = i
#         if str(i.discordid) == str(target):
#             p2 = i

#     if p1 == "" or p2 == "":
#         await ctx.send("You or your opponent are not on the ladder")
#         return False

#     """if (str(p2.challengeId) != ""): #abort challenge if target isn't avaliable
#         await ctx.send("Opponent has already been challenged");
#         return;"""

#     if str(p1.challengeId) != "":
#         await ctx.send(
#             "You already have a challenge pending to {}".format(p1.challengeId)
#         )
#         return

#     p1.challengeId = p2.discordid
#     p2.challengeId = p1.discordid
#     p1.challengeMember = target.id
#     saveLadders(tableData)

#     await ctx.send(
#         target.mention
#         + ": you have been challenged to a match by {} ({})".format(p1.tag, ctx.author)
#     )


# # cancels a challenge
# @bot.command()
# async def cancelChallenge(ctx):
#     tableData = loadLadders()

#     p1 = ""
#     p2 = ""
#     p2Id = ""
#     for i in tableData:
#         if str(i.discordid) == str(ctx.author):
#             p1 = i

#     if p1 == "":
#         await ctx.send("You aren't on the ladder")
#         return False
#     else:
#         if p1.challengeId != "":
#             p2Id = p1.challengeId

#     for i in tableData:
#         if str(i.discordid) == str(p2Id):
#             p2 = i

#     await ctx.send(
#         "{}, your challenge to <@{}> has been cancelled".format(
#             ctx.author, p1.challengeMember
#         )
#     )
#     p1.challengeId = ""
#     p1.challengeMember = ""

#     saveLadders(tableData)

# """
# def checkInLadder(discID):
#     tableData = loadLadders();

#     p1 = ""
#     for i in tableData:
#         if str(i.discordid) == str(discID):
#             p1 = i;

#     if p1 == "":
#         return False;
#     else:
#         return True;
# """

# # test initialization of ladder
# @bot.command()
# @commands.has_role(admin_role)
# async def addDummies(ctx, ladderName):
#     ladderName = ladderName.lower()

#     ladders = loadLadders()
#     p1 = player("dumdum", "dummy")
#     p1.dummy = 1

#     p2 = player("bigmoist", "sean m#3644")
#     p3 = player("kush_apocalypse", "jhinghin#7109")
#     ladders[ladderName].append(p1)
#     ladders[ladderName].append(p2)
#     ladders[ladderName].append(p3)

#     saveLadders(ladders)
#     await ctx.send("Added dummies to " + ladderName)

# bot.run(TOKEN)
