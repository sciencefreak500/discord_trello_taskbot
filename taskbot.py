import trelloWrap as tw
import discord
import asyncio
import json
import os

client = discord.Client()

userIDList = {}
def readJson():
    if not os.path.isfile('trelloUsers.json'):
        file = open('trelloUsers.json','w')
        file.write("{}")
        file.close()
    print("reading json")
    data = json.load(open('trelloUsers.json'))
    for key in data:
        print(key, data[key])
        userIDList[key] = data[key]


def writeJson(author,username):
    for i in userIDList:
        if author in i:
            print("already there")
            return 1
    userIDList[author] = username
    print(userIDList)
    with open('trelloUsers.json','w') as file:
        json.dump(userIDList, file)
    return 0


readJson()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!task'):
        print(message.author)
        discordMessage = message.content
        discordCommand = discordMessage.split(' ')[1]
        print(discordCommand)
        if discordCommand == 'create':
            msg = await client.send_message(message.channel, 'Which Category?\nOptions are: Milestones, To Do, Progress, Done, Backlog, or Resources')
            category = await client.wait_for_message(author=message.author)
            await client.delete_message(msg)
            
            msg = await client.send_message(message.channel, 'Enter a Title\nBest Practice is adding [BUG], [NEW] or [EDIT] before a descriptive, short title\n Example: [BUG] Edit button is too large')
            title = await client.wait_for_message(author=message.author)
            await client.delete_message(msg)
            
            msg = await client.send_message(message.channel, 'Enter a Description\nCan be as long or as short as you want')
            description = await client.wait_for_message(author=message.author)
            await client.delete_message(msg)
            
            #print(category.content,title.content,description.content)
            madeCard = tw.makeCard(category.content,title.content,description.content)
            await client.send_message(message.channel, 'Card "'+title.content+'" has been created on Trello')

        if discordCommand == 'register':
            print('registering user')
            msg = await client.send_message(message.channel, 'What is your Trello username')
            username = await client.wait_for_message(author=message.author)
            await client.delete_message(msg)

            result = writeJson(str(message.author),username.content)
            if result == 0:
                await client.send_message(message.channel, 'Awesome, you have been registered!\nYou can now be assigned to Trello tasks!')
            elif result == 1:
                await client.send_message(message.channel, 'You have already registered')
                
        if discordCommand == 'assigned':
            tw.refresh()
            print(tw.categoryData, userIDList[str(message.author)])
            assignList = tw.getAssigned(tw.categoryData,tw.getMemberID(userIDList[str(message.author)]))
            print(assignList)
            
client.run('MzI1MTU2NDc5MDY3NzUwNDAy.DOJfDQ.2R61oGy-RMB8_iNOwMcCdyLEMsE')
