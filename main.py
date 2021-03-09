import os
import requests
import discord
from dotenv import load_dotenv

from discord.ext import commands

def filename(url, iden):
    file = ''
    for char in url:
        if char not in './:':
            file += char
    file += iden
    return file

usersitelist = {}
with open("sites.txt") as file:
    for line in file:
        line = line.strip()
        username = ''
        counter = 0
        for char in line:
            if(char != '!'):
                username += char
                counter+= 1
            else:
                break
        line = line[counter+1:]
        usersitelist[username] = line.split(',')

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='ping')
async def ping(ctx):
    response = 'hello!'
    await ctx.send(response)

@bot.command(name='rmvsite')
async def rmvsite(ctx, url):
    found = False
    user = str(ctx.author.id)
    if user in usersitelist:
        for site in usersitelist[user]:
            if site == url or site + '/' == url:
                found = True
                sitetodel = site
        if found:
            os.remove(filename(url,iden) + '.txt')
            usersitelist[user].remove(sitetodel)
            with open("sites.txt",'w') as file:
                filetext = ''
                for person in usersitelist:
                    personline = ''
                    personline += person + '!'
                    for website in usersitelist[person]:
                        personline += website + ','
                    personline = personline[:len(personline)-1]
                    filetext += personline + '\n'
                file.write(filetext)
            response = 'site deleted!'
        else:
            response = 'site not found in list :('
    else:
        response = 'you dont have any sites yet, silly!'
    await ctx.send(response)

@bot.command(name='addsite')
async def addsite(ctx, url):
    inuse = False
    user = str(ctx.author.id)
    if user in usersitelist:
        for site in usersitelist[user]:
            if site == url:
                message = "you're already tracking this one!"
                inuse = True
        if inuse == False:
            usersitelist[user].append(url)
    else:
        usersitelist[user] = [url]
    if inuse == False:
        with open("sites.txt",'w') as file:
            filetext = ''
            for person in usersitelist:
                personline = ''
                personline += person + '!'
                for website in usersitelist[person]:
                    personline += website + ','
                personline = personline[:len(personline)-1]
                filetext += personline + '\n'
            file.write(filetext)
        open(filename(url,user)+'.txt','a').close()
        message = 'site added to list!'
    await ctx.send(message)

@bot.command(name='siteupdate')
@commands.cooldown(1, 300, commands.BucketType.user)
async def siteupdate(ctx):
    response = ''
    user = str(ctx.author.id)
    if user in usersitelist and usersitelist[user] != []:
        for site in usersitelist[user]:
            with open(filename(site,user) + ".txt") as file:
                oldsite = file.read()
                newsite = requests.get(site).text
            diff = False
            if len(oldsite) != len(newsite):
                diff = True
            else:
                for i in range(len(oldsite)):
                    if oldsite[i] != newsite[i]:
                        if newsite[i] not in "\n\r\t ":
                            diff = True
            if diff:
                response += site + " updated!"
            else:
                response += 'No updates to ' + site
            with open(filename(site,user) + ".txt", 'w') as file:
                file.write(newsite)
    else:
        response = 'You dont have any sites you are tracking yet!'
    await ctx.send(response)
    
@siteupdate.error
async def siteupdate_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send('Try again in a bit, you can only update once every five minutes')

bot.run(token)
