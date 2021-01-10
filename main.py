import discord
import os
from tabulate import tabulate
from keep_alive import keep_alive
import time

hed=["Worlds","DWF","ELM","RDI","Unknown"]
client = discord.Client()

dicSkill=dict()
dicLoc=dict()
dicBroken=dict()
dicBeam=dict()


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
  if i in dicBeam:
    toret= toret+' (Beamed)'
  if i in dicBroken:
    toret= toret+' (Broken)'
  return "\n"+toret
def pepperTheTable():
  global table
  table = [["Herblore","","","",""],["Farming","","","",""],["Construction","","","",""],["Smithing","","","",""],["Mining","","","",""],["Unknown","","","",""]]
  for i in range(200):
    if i in dicLoc and i in dicSkill:
      for id in Skill2Index(dicSkill[i]):
        table[id][hed.index(dicLoc[i])]+=BeamBroke(i)
      continue
    if i in dicLoc:
      table[5][hed.index(dicLoc[i])]+=BeamBroke(i)
    if i in dicSkill:
      for id in Skill2Index(dicSkill[i]):
        table[id][4]+=BeamBroke(i)
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
      dicBroken[world]=True
      return

    if arr[1] == "BEAM" or arr[1] == "BEAMED":
      dicBeam[world]=True
      return

    if arr[1] == "DEAD":
      dicLoc.pop(world, None)
      dicSkill.pop(world, None)
      dicBroken.pop(world, None)
      dicBeam.pop(world, None)
      return

    if arr[1] in ["DWF","ELM","RDI"]:
      dicLoc[world]=arr[1]
    else:
      if Skill2Index(arr[1])!=[]:
        dicSkill[world]=arr[1]
  if len(arr)==3:
    loc=arr[1].upper()
    skill=arr[2].upper()
    if loc not in ["DWF","ELM","RDI"]:
      loc=arr[2].upper()
      skill=arr[1].upper()
    if loc not in ["DWF","ELM","RDI"]:
      return
    dicLoc[world]=loc
    dicSkill[world]=skill


@client.event
async def on_ready():
    global table
    global timeRestart
    timeRestart=0
    table = [["Herblore","","","",""],["Farming","","","",""],["Construction","","","",""],["Smithing","","","",""],["Mining","","","",""],["Unknown","","","",""]]
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global table
    global timeRestart
    if message.author == client.user:
        return
    msg=message.content

    if int(time.time()/3600)!=timeRestart:
      dicLoc.clear()
      dicSkill.clear()
      dicBroken.clear()
      dicBeam.clear()
      timeRestart=int(time.time()/3600)

    if ' ' in msg:
      arr=msg.split(' ')
      updateTab(arr)

    if msg=='cLeAr eVeRyThInG':
      dicLoc.clear()
      dicSkill.clear()
      dicBroken.clear()
      dicBeam.clear()

    if msg=='s':
        pepperTheTable()
        outy = ("```" + "\n\n" + tabulate(table, tablefmt="fancy_grid", headers=hed) + "```")
        await message.channel.send(outy)
tok=os.getenv('TOKEN')
keep_alive()
client.run(tok)


#https://stackoverflow.com/questions/25244454/python-create-strikethrough-strikeout-overstrike-string-type/25244576
#my_dict.pop('key', None)
#https://stackoverflow.com/questions/57582873/posting-embedded-output-using-tabulate-and-discord-rewrite
#https://pypi.org/project/tabulate/
#https://stackoverflow.com/questions/9535954/printing-lists-as-tabular-data