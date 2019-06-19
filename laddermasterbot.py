import pickle
import operator
import discord
from discord.ext import commands
from discord.utils import get
import traceback


# global vars
admin_role = "adminy"

# try:

# except Exception:
#     traceback.print_exc()


class player:
    def __init__(self, tag, discordid):
        self.tag = tag
        self.characters = []
        self.discordid = discordid
        self.dummy = 0
        self.confirmId = ""
        self.challengeId = ""
        self.challengeMember = ""


def saveLadders(ladders):
    with open("ladders.pkl", "wb") as output:
        pickle.dump(ladders, output, pickle.HIGHEST_PROTOCOL)


def loadLadders():
    with open("ladders.pkl", "rb") as input:
        return pickle.load(input)


TOKEN = "NTkwNjYzNjExMTY1MTc5OTcw.XQlgjQ.HvcSd_OeWJpBXhzD_nyvrS-HXso"

bot = commands.Bot(command_prefix=".", case_insensitive=True)

# error handler (mutes errors so comment this out when debugging)
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You don't have permission to use this command YOU IDIOT.")
    if isinstance(error, commands.MissingRequiredArgument):
        if str(ctx.command) == "ladder":
            await ctx.send("The correct usage is !ladder <game>")
        if str(ctx.command) == "joinLadder":
            await ctx.send("The correct usage is !joinLadder <game> <tag>")
        if str(ctx.command) == "beat":
            await ctx.send("The correct usage is !beat <@opponent> <game>")
        if str(ctx.command) == "confirm":
            await ctx.send("The correct usage is !confirm <@opponent> <game>")
        if str(ctx.command) == "deny":
            await ctx.send("The correct usage is !deny <@opponent> <game>")
        if str(ctx.command) == "addMember":
            await ctx.send("The correct usage is !addMember <@player> <player tag> <game>")
        if str(ctx.command) == "moveUp":
            await ctx.send("The correct usage is !moveUp <@player> <player tag> <game>")
        if str(ctx.command) == "moveDown":
            await ctx.send("The correct usage is !moveDown <@player> <player tag> <game>")

# help
@bot.command()
async def ladderhelp(ctx):
    ladders = loadLadders()

    msg = '''```Current commands:
- !ladder <game>: displays ladder
- !joinLadder <game> <tag>: allows you to join a ladder
- !beat <@opponent> <game>: initiates a rank swap between you and someone you beat
- !confirm <@opponent> <game>: accepts a rank swap
- !deny <@opponent> <game>: denies a rank swap
- !addMember <@player> <player tag> <game>: adds a member to a ladder (admin only)
- !moveUp <@player> <player tag> <game>: moves someone up a rank (admin only)
- !moveDown <@player> <player tag> <game>: moves someone down a rank (admin only)
The current possible games are:'''
    for key in ladders:
        msg += "'" + key + "'" + ", "
        msg = msg[:-2]
    msg += ".\n"
    msg += "```"
    await ctx.send(msg)
# test initialization of ladder
@bot.command()
@commands.has_role(admin_role)
async def addDummies(ctx, ladderName):

    ladderName = ladderName.lower()

    ladders = loadLadders()
    p1 = player("dumdum", "dummy")
    p1.dummy = 1

    p2 = player("bigmoist", "sean m#3644")
    p3 = player("kush_apocalypse", "jhinghin#7109")
    ladders[ladderName].append(p1)
    ladders[ladderName].append(p2)
    ladders[ladderName].append(p3)

    saveLadders(ladders)
    await ctx.send("Added dummies to " + ladderName)


# ititializes ladder for the first time, DO NOT RUN THIS IN THE FUTURE
@bot.command()
@commands.has_role(admin_role)
async def firstTimeInit(ctx):
    ladders = {
        "unist": [],
        "tekken": [],
        "melee": [],
        "smush": [],
        "sf3s": [],
        "dbfz": [],
    }
    await ctx.send("Ladders Initialized")

    saveLadders(ladders)


# joins a particular ladder
@bot.command()
async def joinLadder(ctx, ladderName, tag):
    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = "That game doesn't exist.\n" "Possible games are: "
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return

    p1 = player(tag, "{0}".format(ctx.author))

    add = True
    for i in ladderData:
        if i.discordid == "{0}".format(ctx.author):
            add = False
            await ctx.send("You're already in this ladder.")
            return

    if add:
        ladderData.append(p1)
        saveLadders(ladders)

    msg = "{}".format(ctx.author)
    msg += " has joined the " + ladderName + " ladder as '"
    msg += tag + "'."

    await ctx.send(msg)


# display ladder info
@bot.command()
async def ladder(ctx, ladderName):
    ladders = loadLadders()
    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = "That game doesn't exist.\n" "Possible games are: "
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return

    if ladderName == "unist":
        gameName = "UNIST"
    elif ladderName == "tekken":
        gameName = "TEKKEN 7"
    elif ladderName == "melee":
        gameName = "SUPER SMASH BROS MELEE"
    elif ladderName == "smush":
        gameName = "SUPER SMASH BROS ULTIMATE"
    elif ladderName == "sf3s":
        gameName = "STREET FIGHTER 3RD STRIKE"
    elif ladderName == "dbfz":
        gameName = "DRAGON BALL FIGHTERZ"

    # adaptive text formatting rofl
    msg = "```\n------------------"
    for i in range(0, len(gameName)):
        msg += "-"
    msg += "\n-- QFGC " + gameName + " LADDER --\n"
    for i in range(0, len(gameName)):
        msg += "-"
    msg += "------------------\n\n"

    n = 1
    for i in ladderData:
        if i.dummy != 1:
            msg += str(n) + ") " + i.discordid + "\n"
            n += 1

    msg += "```"
    await ctx.send(msg)


"""
def checkInLadder(discID):
    tableData = loadLadders();

    p1 = ""
    for i in tableData:
        if str(i.discordid) == str(discID):
            p1 = i;
            
    if p1 == "":
        return False;
    else:
        return True;
"""

#

# initiates swap between two players
@bot.command()
async def beat(ctx, loser: discord.Member, ladderName):
    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = "That game doesn't exist.\n" "Possible games are: "
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
        winner.confirmId = loser.discordid
        await ctx.send(
            loser_discord.mention
            + " please type !confirm <@opponent> <game> or !deny <@opponent> <game> to validate the set results"
        )
    else:
        await ctx.send(
            "You must wait until your last opponent confirms the results of your set"
        )

    saveLadders(ladders)


# confirms result of set
@bot.command()
async def confirm(ctx, winner: discord.Member, ladderName):
    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = "That game doesn't exist.\n" "Possible games are: "
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

    loser_old_rank = ladderData.index(loser)
    print(loser_old_rank)
    winner_old_rank = ladderData.index(winner)
    print(winner_old_rank)

    # check rank difference
    if loser_old_rank > winner_old_rank:
        await ctx.send("No need to swap, loser is already below winner")
    # swap ranks between winner and loser
    elif winner.confirmId == loser.discordid:
        ladderData[loser_old_rank] = winner
        ladderData[winner_old_rank] = loser
        winner.confirmId = ""
        loser.confirmId = ""
        await ctx.send("Set results confirmed. Ranks have been swapped")
    else:
        await ctx.send("You don't have any pending sets against this person")
        winner.confirmId = ""
        loser.confirmId = ""

    saveLadders(ladders)


# denies the result of a set
@bot.command()
async def deny(ctx, winner: discord.Member, ladderName):
    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = "That game doesn't exist.\n" "Possible games are: "
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


# adds another player to ladder (admin only)
@bot.command()
@commands.has_role(admin_role)
async def addMember(ctx, new_player: discord.Member, tag, ladderName):
    ladders = loadLadders()

    try:
        ladderName = ladderName.lower()
        ladderData = ladders[ladderName]
    except KeyError:
        errmsg = "That game doesn't exist.\n" "Possible games are: "
        for key in ladders:
            errmsg += "'" + key + "'" + ", "
        errmsg = errmsg[:-2]
        errmsg += ". "
        await ctx.send(errmsg)
        return

    new_player = player(tag, "{0}".format(new_player))

    add = True
    for i in ladderData:
        if i.discordid == "{0}".format(new_player):
            add = False
            await ctx.send("Player is already in this ladder.")
            return

    if add:
        ladderData.append(new_player)
        saveLadders(ladders)

    msg = new_player.discordid
    msg += " has joined the " + ladderName + " ladder as '"
    msg += tag + "'."

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
        errmsg = "That game doesn't exist.\n" "Possible games are: "
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
        errmsg = "That game doesn't exist.\n" "Possible games are: "
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


# tests if bot's up (dev purposes only)
@bot.command()
@commands.has_role(admin_role)
async def works(ctx):
    await ctx.send("bot's up atm")


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

