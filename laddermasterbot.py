import discord
from discord.ext import commands
import pickle
import operator

class player:
    def __init__(self, tag, discordid, size):
        
        self.tag = tag
        self.characters = []
        self.discordid = discordid
        self.rank = size
        self.dummy = 0;
        self.confirmId = ""
        self.challengeID = ""
        
        
def saveTable(tableData):
    with open('tableData.pkl', 'wb') as output:
        pickle.dump(tableData, output, pickle.HIGHEST_PROTOCOL)
        
def loadTable():
    with open('tableData.pkl', 'rb') as input:
        return pickle.load(input)
    

TOKEN = 'NTg3NzE3NjU1NDgyNTk3NDc4.XP6pEQ.fMFiHX0RgXs0ipzUv1iccC68Xi8'

bot = commands.Bot(command_prefix='!')

@bot.command()
async def joinLadder(ctx, tag):
    tableData = loadTable()
    size = len(tableData)
    
    p1 = player(tag, '{0}'.format(ctx.author), size)
    
    add = True;
    for i in tableData: 
        if i.discordid == '{0}'.format(ctx.author):
            add = False;
            break;
   
    if add:
        tableData.append(p1);
        saveTable(tableData);
        
        
    await ctx.send('{}, {}'.format(ctx.author,tag))
    
@bot.command()
async def ladder(ctx):
    tableData = loadTable()
    tableData.sort(key=operator.attrgetter('rank'))
    
    msg = "```\n-----------------------\n-- QFGC MELEE LADDER --\n-----------------------\n\n"
    n = 1;
    for i in tableData:
        if i.dummy != 1:
            print(i.discordid)
            print(i.rank)
            msg += str(n) + ") " + i.discordid + '\n';
            n += 1
            

    msg += "```"
    await ctx.send(msg)

@bot.command()
async def challenge(ctx, target : discord.Member):
    tableData = loadTable();
    
    for i in tableData:
        if str(i.discordid) == str(ctx.author):
            p1 = i;
    
    await ctx.send(target.mention + ": you have been challenged to a match by {} ({})".format(p1.tag, ctx.author))


@bot.command()
async def beat(ctx, loser : discord.Member):
    tableData = loadTable()

    p1 = 0;
    p2 = 0;

    #get player info
    for i in tableData:
        if str(i.discordid) == str(ctx.author):
            p1 = i;
        if str(i.discordid) == str(loser):
            p2 = i;

    r1 = p1.rank
    r2 = p2.rank
    
    #send confirmation
    if abs(r1-r2) <= 2:
        if str(p1.confirmId) == "":
            p1.confirmId = p2.discordid
      
            await ctx.send(loser.mention + " please type !confirm or !deny, followed by @ing your last opponent to validate the set results")
        else:
            await ctx.send("You must wait until your last opponent confirms the results of your set")
    
    saveTable(tableData)


@bot.command()
async def confirm(ctx, loser : discord.Member):
    tableData = loadTable()

    p1 = 0;
    p2 = 0;

    #check rank difference
    for i in tableData:
        if str(i.discordid) == str(ctx.author):
            p1 = i;
        if str(i.discordid) == str(loser):
            p2 = i;

    #swap ranks between winner and loser
    if p2.confirmId == p1.discordid:        
        t = p1.rank
        p1.rank = p2.rank
        p2.rank = t;
        p1.confirmId = ""
        p2.confirmId = ""
        await ctx.send("Set results confirmed. Ranks have been swapped")
    else:
        await ctx.send("You don't have any pending sets against this person")
    
    saveTable(tableData);


    
@bot.command()
async def deny(ctx, winner : discord.Member):
    tableData = loadTable()
    
    p1 = 0;
    p2 = 0;
    #get player info
    for i in tableData:
        if str(i.discordid) == str(ctx.author):
            p1 = i;
        if str(i.discordid) == str(winner):
            p2 = i;

    if p2.confirmId == p1.discordid:
        p1.confirmId = ""
        p2.confirmId = ""
        await ctx.send("Set results have been invalidated");
    else:
        await ctx.send("You don't have any pending sets against this person")    
'''

bot.run(TOKEN)




