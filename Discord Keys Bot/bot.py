import discord
from discord.ext import commands
import json

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix=">", intents=intents)

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))


def ChangeValue(userID:int):
  with open('limit.json') as f:
    data = json.load(f)
    data[str(userID)] = str(int(data[str(userID)])-1)
  with open('limit.json', 'w') as outfile:
      json.dump(data, outfile)
  return int(data[str(userID)])
  #I KNOW, this is terrible, but stfu it works

@client.command()
async def email(ctx):
  try:
    emails = open("keys.txt", 'r').readlines()
    
    limit = ChangeValue(ctx.author.id)
    dm = await ctx.author.create_dm()

    if limit>=0:
      await dm.send(emails[0] + f"\nYou have: {limit} emails left.")
      open("emails.txt", 'w').write("")
      index = 0
      for mail in emails:
        if index == 0:
          pass
        else:
          open("emails.txt", "a").write(mail)
        index=index+1
    else:
      await dm.send("You are out of emails!")

  except IndexError: # You all can do the error handling, this is a foundation
    await ctx.send("ERROR: Out of emails")
  except FileNotFoundError:
    await ctx.send("ERROR: Runner is retarded and ran in the wrong folder")
  except:
    await ctx.send("ERROR: Somthing unexpected happened, maybe your dms are off?")

@client.command()
async def reset_all(ctx):
  with open('limit.json') as f:
    data = json.load(f)
  for user in data:
      data[str(user)] = "5"

  with open('limit.json', 'w') as outfile:
    json.dump(data, outfile)
  
  await ctx.send("All user reset!")

def check_value(data, val):
    return any(user==val for user in data)

@client.command(pass_context = True)
async def reset(ctx, user_id = None):
  if user_id == None:
    await ctx.send("Please provide a user id")
  else:
    with open('limit.json') as f:
      data = json.load(f)
    if check_value(data, user_id):
      data[str(user_id)] = "5"
      with open('limit.json', 'w') as outfile:
        json.dump(data, outfile)
      
      await ctx.send(f"Reset user: {user_id}")
    else:
      await ctx.send(f"Could not find user: **{user_id}**, has to be the User ID")

tokn='' # you thought lol
client.run(tokn)