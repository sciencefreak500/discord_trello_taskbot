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
        print(message.content)
        discordMessage = message.content
        try:
            discordCommand = discordMessage.split(' ')[1]
        except:
            await client.send_message(message.channel, 'List of commands:\n * !task create - creates a new task on Trello\n * !task register - registers a username\n * !task assigned - get all tasks you are assigned to')
            return;
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
            msg = await client.send_message(message.channel, 'Please wait...')
            tw.refresh()
            #print(tw.categoryData, userIDList[str(message.author)])
            assignList = tw.getAssigned(tw.categoryData,tw.getMemberID(userIDList[str(message.author)]))
            print(assignList)
            totalString = ""
            for i in assignList:
                #print(i, assignList[i])
                totalString += '\n=='+ i + '==\n'
                count = 0
                for j in assignList[i]:
                    count += 1
                    totalString += "----------------------------------------\n"
                    totalString += "Name: " + j['name'] + "\nDescription: " + j['description']
                    totalString += "\n----------------------------------------\n"
            print(totalString)
            await client.delete_message(msg)
            await client.send_message(message.channel, totalString)

        if discordCommand == 'give':
            try:
                discordUsername = discordMessage.split(' ')[2]
                discordTrigger = discordMessage.split(' ')[3]
            except:
                await client.send_message(message.channel, '!task give takes 2 additional arguments\n\n * Syntax: `!task give user taskName`\n * Example: `!task give @Milord recent`')
                return;
            print('proceed')
            
            
client.run('MzI1MTU2NDc5MDY3NzUwNDAy.DOJfDQ.2R61oGy-RMB8_iNOwMcCdyLEMsE')




