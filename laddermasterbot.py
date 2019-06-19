import discord
from discord.ext import commands
import pickle
import operator
import sched
import time
from discord.utils import get
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class player:
    def __init__(self, tag, discordid, size):

        self.tag = tag
        self.characters = []
        self.discordid = discordid
        self.rank = size
        self.dummy = 0
        self.confirmId = ""
        self.challengeId = ""
        self.challengeMember = ""
        self.challengeTimer = -1


def saveTable(tableData):
    with open('tableData.pkl', 'wb') as output:
        pickle.dump(tableData, output, pickle.HIGHEST_PROTOCOL)


def loadTable():
    with open('tableData.pkl', 'rb') as input:
        return pickle.load(input)


TOKEN = 'NTg3NzE3NjU1NDgyNTk3NDc4.XP6pEQ.fMFiHX0RgXs0ipzUv1iccC68Xi8'

bot = commands.Bot(command_prefix='!')


@bot.command()
async def addDummy(ctx):
    tableData = []
    p1 = player("dumdum", 'dummy', -100000)
    p1.dummy = 1

    p2 = player('bigmoist', "sean m#3644", 1)
    p3 = player('kush_apocalypse', "jhinghin#7109", 2)
    tableData.append(p1)
    tableData.append(p2)
    tableData.append(p3)

    saveTable(tableData)


@bot.command()
async def joinLadder(ctx, tag):
    tableData = loadTable()
    size = len(tableData)

    p1 = player(tag, '{0}'.format(ctx.author), size)

    add = True
    for i in tableData:
        if i.discordid == '{0}'.format(ctx.author):
            add = False
            break

    if add:
        tableData.append(p1)
        saveTable(tableData)

    await ctx.send('{}, {}'.format(ctx.author, tag))


@bot.command()
async def addCharacter(ctx, char):
    tableData = loadTable()
    
    for i in tableData:
        if str(i.discordid) == str(ctx.author):
            i.characters.append(char)

    saveTable(tableData)
    await ctx.send('{} added to character list'.format(char))

@bot.command()
async def clearCharacters(ctx):
    tableData = loadTable()
    
    for i in tableData:
        if str(i.discordid) == str(ctx.author):
            i.characters.clear()

    saveTable(tableData)
    await ctx.send('Character list cleared')

@bot.command()
async def ladder(ctx):
    tableData = loadTable()
    tableData.sort(key=operator.attrgetter('rank'))

    msg = "```\n-----------------------\n-- QFGC MELEE LADDER --\n-----------------------\n\n"
    n = 1
    for i in tableData:
        if i.dummy != 1:
            print(i.discordid)
            print(i.rank)
            msg += str(n) + ") " + i.discordid + '\n'
            n += 1

    msg += "```"
    await ctx.send(msg)
    updateSheet(tableData)
'''
def checkInLadder(discID):
    tableData = loadTable();

    p1 = ""
    for i in tableData:
        if str(i.discordid) == str(discID):
            p1 = i;
            
    if p1 == "":
        return False;
    else:
        return True;
'''


@bot.command()
async def challenge(ctx, target: discord.Member):
    tableData = loadTable()

    p1 = ""
    p2 = ""
    for i in tableData:
        if str(i.discordid) == str(ctx.author):
            p1 = i
        if str(i.discordid) == str(target):
            p2 = i

    if p1 == "" or p2 == "":
        await ctx.send("You or your opponent are not on the ladder")
        return False

    '''if (str(p2.challengeId) != ""): #abort challenge if target isn't avaliable
        await ctx.send("Opponent has already been challenged");
        return;'''

    if (str(p1.challengeId) != ""):
        await ctx.send("You already have a challenge pending to {}".format(p1.challengeId))
        return

    p1.challengeId = p2.discordid
    p1.challengeMember = target.id
    p1.challengeTimer = time.time()
    saveTable(tableData)

    await ctx.send(target.mention + ": you have been challenged to a match by {} ({})".format(p1.tag, ctx.author))


@bot.command()
async def cancelChallenge(ctx):
    tableData = loadTable()

    p1 = ""
    p2 = ""
    p2Id = ""
    for i in tableData:
        if str(i.discordid) == str(ctx.author):
            p1 = i

    if p1 == "":
        await ctx.send("You aren't on the ladder")
        return False
    else:
        if p1.challengeId != "":
            p2Id = p1.challengeId

    for i in tableData:
        if str(i.discordid) == str(p2Id):
            p2 = i

    await ctx.send("{}, your challenge to <@{}> has been cancelled".format(ctx.author, p1.challengeMember))
    p1.challengeId = ""
    p1.challengeMember = ""

    saveTable(tableData)


@bot.command()
async def beat(ctx, loser: discord.Member):
    tableData = loadTable()

    p1 = 0
    p2 = 0

    # get player info
    for i in tableData:
        if str(i.discordid) == str(ctx.author):
            p1 = i
        if str(i.discordid) == str(loser):
            p2 = i

    r1 = p1.rank
    r2 = p2.rank

    # send confirmation
    if abs(r1-r2) <= 2:
        if str(p1.confirmId) == "":
            p1.confirmId = p2.discordid

            await ctx.send(loser.mention + " please type !confirm or !deny, followed by @ing your last opponent to validate the set results")
        else:
            await ctx.send("You must wait until your last opponent confirms the results of your set")

    saveTable(tableData)


@bot.command()
async def confirm(ctx, loser: discord.Member):
    tableData = loadTable()

    p1 = 0
    p2 = 0

    # check rank difference
    for i in tableData:
        if str(i.discordid) == str(ctx.author):
            p1 = i
        if str(i.discordid) == str(loser):
            p2 = i

    # swap ranks between winner and loser
    if p2.confirmId == p1.discordid:
        t = p1.rank
        p1.rank = p2.rank
        p2.rank = t
        p1.confirmId = ""
        p2.confirmId = ""
        await ctx.send("Set results confirmed. Ranks have been swapped")
    else:
        await ctx.send("You don't have any pending sets against this person")

    saveTable(tableData)


@bot.command()
async def deny(ctx, winner: discord.Member):
    tableData = loadTable()

    p1 = 0
    p2 = 0
    # get player info
    for i in tableData:
        if str(i.discordid) == str(ctx.author):
            p1 = i
        if str(i.discordid) == str(winner):
            p2 = i

    if p2.confirmId == p1.discordid:
        p1.confirmId = ""
        p2.confirmId = ""
        await ctx.send("Set results have been invalidated")
    else:
        await ctx.send("You don't have any pending sets against this person")


# SPREADSHEET PART OF THE CODE ---------------------------------------------------------------------------------------

def updateSheet(tableD):

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("TestLadderMasterSheet")
    workSheet = sheet.worksheet('meleeSheet')

    tableData = tableD
    # 'unist', 'tekken', 'melee', 'smush', 'sf3s', 'dbfz'.
    '''meleeData = tableData['melee']
    unistData = tableData['unist']
    tekkenData = tableData['tekken']
    smushData = tableData['smush']
    sf3sData = tableData['sf3s']
    dbfzData = tableData['dbfz']'''

    x = 0
    for i in tableData:
        if x == 0: #skip dummy acc
            x += 1
            continue

        workSheet.update_cell(11+x, 7, i.tag)
        cList = ""
        for c in i.characters:
            print(c)
            cList += c + ", "

        cList = cList[:-2]
        workSheet.update_cell(11+x, 8, cList)
        workSheet.update_cell(11+x, 9, i.discordid)
        x += 1


bot.run(TOKEN)
