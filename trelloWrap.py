from trello import TrelloApi

#ref docs
# https://pythonhosted.org/trello/trello.html#trello.Boards.get_list_filter
#created by Michael Milord

trello = TrelloApi("596e2ae73702acd0ae6eb0f8f0ebaf52")
trello.set_token("2e4eada2861e709648fa4fb8b824e3287b78888eae838521a51e61b4058847ed")

#functions#
def getLabels(board):
    result = {}
    lbl = board['labelNames']
    for i in lbl:
        if lbl[i] != '':
            result[lbl[i]] = i
    return result

def getCategories(boardID):
    result = {}
    foo = trello.boards.get_list(boardID)
    for i in foo:
        for j in i:
            #print j,i[j]
            result[i['name']] = i['id']
        #print ""
    return result
        
def getCategoryData(categories):
    resultList = {}
    for i in categories:
        info = trello.lists.get_card(categories[i])
        #print info
        if info != []:
            infoObj = []
            for j in info:
                infoObj.append({
                    "id": j['id'],
                    "name": j['name'],
                    "description": j['desc'],
                    "labels": j['idLabels'],
                    "members": j['idMembers'],
                    "due": j['due'],
                    "dueComplete": j['dueComplete'],
                    "url" : j['url']
                    })
            #print i, infoObj
            resultList[i] = infoObj
    return resultList

def getCard(array,idOrName):
    for i in array:
        for j in array[i]:
            if idOrName == j['id'] or idOrName == j['name']:
                return j
        #print "not in ", i
    return None


def getCardinCategory(array,idOrName):
    for i in array:
        if idOrName == i['id'] or idOrName == i['name']:
            return i
    return None


def getAssigned(array,member):
    result = []
    for i in array:
        for j in array[i]:
            if member in j['members']:
                result.append(j)
    return result

def getMemberID(username):
    mem = trello.members.get(username)
    return mem['id']

def makeCard(listid,name,description = ""):
    cat = ""
    for i in categories:
        if listid in i:
            cat = categories[i]
            break
    return trello.lists.new_card(cat,name,description)

def addLabel(cardID,label):
    try:
        value = ""
        for i in labels:
            if label in i:
                value = labels[i]
                break
        trello.cards.new_label(cardID,value)
    except:
        print("Label already added")


def addMember(cardID,member):
    try:
        trello.cards.new_member(cardID,getMemberID(member))
    except:
        print("member already there")

def moveCard(cardID,listname):
    catID = ""
    for i in categories:
        if i in listname:
            catID = categories[i]
            break
    return trello.cards.update_idList(cardID,catID)

def refresh():
    eoko = trello.boards.get('59adc21b52e8b12473b6ad26')
    labels = getLabels(eoko)
    categories = getCategories(eoko['id'])
    categoryData = getCategoryData(categories)

#milord = trello.members.get('michaelmilord1')
#boards = milord['idBoards']
eoko = trello.boards.get('59adc21b52e8b12473b6ad26')
labels = getLabels(eoko)
categories = getCategories(eoko['id'])
categoryData = getCategoryData(categories)


#test
#card  = makeCard('Progress',"testcard4","this is a test4")
#addLabel(card['id'],"Low")
#addMember(card['id'],'michaelmilord1')
#card = moveCard(card['id'],'To Do')
#mysign = getAssigned(categoryData, getMemberID('michaelmilord1'))

