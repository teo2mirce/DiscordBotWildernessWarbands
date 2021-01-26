import discord
import os
from tabulate import tabulate
from keep_alive import keep_alive
import time

hed=["","DWF","ELM","RDI"]
client = discord.Client()

dickSkill=dict()
dickLoc=dict()
dickBroken=dict()
dickBeam=dict()
dickDead=dict()


def Skill2Index(Skills):
  arr=[]
  if 'H' in Skills:
    arr.append(0)
  if 'F' in Skills:
    arr.append(1)
  if 'C' in Skills:
    arr.append(2)
  if 'S' in Skills:
    arr.append(3)
  if 'M' in Skills:
    arr.append(4)
  if len(Skills)==len(arr) and len(arr)<=3:
    return arr
  else:
    return []
    
def BeamBroke(i):
  toret=str(i)
  if i in dickBeam:
    toret= '*'+toret+'*'
  if i in dickBroken:
    toret= toret+' B'
  if i in dickDead:
    toret= toret+' D'
  return "\n"+toret
def pepperTheTable():
  global table
  table = [["H","","",""],["F","","",""],["C","","",""],["S","","",""],["M","","",""],["?","","",""]]
  for i in range(200):
    #3 cazuri
    if i in dickLoc and i in dickSkill:#ambele
      for id in Skill2Index(dickSkill[i]):
        table[id][hed.index(dickLoc[i])]+=BeamBroke(i)
      continue
    if i in dickLoc:#doar locatie
      table[5][hed.index(dickLoc[i])]+=BeamBroke(i)
    if i in dickSkill:#doar skill
      for id in Skill2Index(dickSkill[i]):
        break
        #table[id][4]+=BeamBroke(i)
def updateTab(arr):
  if len(arr)<2 or len(arr) > 3:
    return
  if not arr[0].isnumeric():
    return
  world=int(arr[0])
  if world<1 or world>200:
    return
  if len(arr)==2:
    arr[1]=arr[1].upper()


    if arr[1] == "BROKE" or arr[1] == "BROKEN":
      dickBroken[world]=True
      dickBeam.pop(world, None)
      dickDead.pop(world, None)
      return

    if arr[1] == "BEAM" or arr[1] == "BEAMED":
      dickBeam[world]=True
      dickBroken.pop(world, None)
      dickDead.pop(world, None)
      return

    if arr[1] == "DEAD":
      dickSkill.pop(world, None)
      dickDead[world]=True
      dickBeam.pop(world, None)
      dickBroken.pop(world, None)
      return
    
    if arr[1] == "DELETE" or arr[1] == "CLEAR" or arr[1] == "REMOVE":
      dickLoc.pop(world,None)
      dickSkill.pop(world, None)
      dickDead.pop(world,None)
      dickBeam.pop(world, None)
      dickBroken.pop(world, None)
      return

    if arr[1] in ["DWF","ELM","RDI"]:#a zis locatie deci skill unknown
      dickLoc[world]=arr[1]
    else:#a zis skill deci locatie unknown
      if Skill2Index(arr[1])!=[]:
        dickSkill[world]=arr[1]
  if len(arr)==3:
    loc=arr[1].upper()
    skill=arr[2].upper()
    if loc not in ["DWF","ELM","RDI"]:
      loc=arr[2].upper()
      skill=arr[1].upper()
    if loc not in ["DWF","ELM","RDI"]:
      print(loc,' nu e locatie')
      return
    dickLoc[world]=loc
    dickSkill[world]=skill


@client.event
async def on_ready():
    global table
    global timeRestart
    timeRestart=0
    table = [["H","","",""],["F","","",""],["C","","",""],["S","","",""],["M","","",""],["?","","",""]]
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global table
    global timeRestart
    if message.author == client.user:
        return
    msg=message.content

    if int(time.time()/3600)!=timeRestart:
      dickLoc.clear()
      dickSkill.clear()
      dickBroken.clear()
      dickBeam.clear()
      dickDead.clear()
      timeRestart=int(time.time()/3600)

    if ' ' in msg:
      arr=msg.split(' ')
      updateTab(arr)
    #https://stackoverflow.com/questions/52241051/i-want-to-let-my-discord-bot-send-images-gifs
    if msg=='Rick me':
      await message.channel.send(file=discord.File('tenor.gif'))

    if msg=='cLeAr eVeRyThInG':
      dickLoc.clear()
      dickSkill.clear()
      dickBroken.clear()
      dickBeam.clear()
      dickDead.clear()

    if msg=='s':
        pepperTheTable()
        outy = ("```" + tabulate(table, tablefmt="fancy_grid", headers=hed) + "```")
        await message.channel.send(outy)
tok=os.getenv('TOKEN')
keep_alive()
client.run(tok)



#35 broken = 35 apare taiat
#35 dead = 35 dispare din tabel de peste tot
#35 beamed = 35 apare cu bold si subliniat
#https://stackoverflow.com/questions/25244454/python-create-strikethrough-strikeout-overstrike-string-type/25244576
#my_dict.pop('key', None)

#https://stackoverflow.com/questions/57582873/posting-embedded-output-using-tabulate-and-discord-rewrite
#https://pypi.org/project/tabulate/
#https://stackoverflow.com/questions/9535954/printing-lists-as-tabular-data
