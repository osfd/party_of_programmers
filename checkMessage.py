#!/usr/bin/python3

import requests, json, mysql.connector, re

linkToChanel = "https://t.me/"
helpText = """Для начала необходимо ознакомиться с манифестом.
Если Вы с ним согласны, то можете вступить в Партию программистов.
Для этого Вам нужно прочитать в Положении 1 инструкцию по вступлению.
На данный момент бот обрабатывает только две команды help и enjoy.
help - выдаст этот текст.
enjoy - имеет следующий синтаксиc:
/enjoy YouMD5sum
где YouMD5sum - это полученнаяя контрольная сумма от заявления.
Все материалы и прочую информацию можно найти на https://github.com/osfd/party_of_programmers
"""
url="https://api.telegram.org/bot"
bot_id="BotId:Token/"
URL = url+bot_id
mydb = mysql.connector.connect(
  host="localhost",
  user="user",
  password="password",
  database="telegram"
)
mycursor = mydb.cursor()

def addNewEmployer(messageText):
  employerId = -1
  data = messageText['text'].split(' ')
  if len(data) == 2:
    print("hash: ", data[1])
    print(messageText)
    if len(re.findall(r'[0-9a-fA-F]', data[1])) == 32:
      sql = """INSERT INTO `users` (hash, chat_id) VALUES ('{}', {});
            """.format(data[1], messageText['chat']['id'])
      mycursor.execute(sql)
      mydb.commit()
      sql = """SELECT `id` FROM `users` WHERE hash='{}' AND chat_id={};
            """.format(data[1], messageText['chat']['id'])
      mycursor.execute(sql)
      for i in mycursor:
        employerId = i[-1]
      response = "You id {}. You can join to our channel {}".format(employerId, linkToChanel)
    else:
      response = "Wrong hash, read /help"
  else:
    print("problem with parsing")
    response = "You need send md5 in next format:%0A/enjoy 79054025255fb1a26e4bc422aef54eb4"
  return response

def checkUpdateId(id):
  status = False
  print("Check in DB update with id ", id)
  sql = "SELECT * FROM updates WHERE update_id={}".format(id)
  mycursor.execute(sql)
  result = mycursor.fetchone()
  if not result:
    print("not found, record to DB")
    sql = "INSERT INTO `updates`  VALUES ({}, FALSE);".format(id)
    mycursor.execute(sql)
    mydb.commit()
    print("Insert success for ", id)
  else:
    print("Found ", result)
    status = True
  return status

def checkMessage(message):

  try:
    command = message['message']['text']
    print(command)
  except:
    print("No message (maby sticker or media)")
    return

  if command.split(' ')[0] == "/help":
    response = helpText
  elif command.split(' ')[0] == "/enjoy":
    response = addNewEmployer(message['message'])
  else:
    response = "Error. Please, read /help"
    print("parsing error")
  sql = "UPDATE `updates` SET status=TRUE WHERE update_id={};".format(message['update_id'])
  mycursor.execute(sql)
  mydb.commit()

  sendMessage(response, message['message']['chat']['id'])

def sendMessage(message, chat_id):
  return requests.get(url = URL+"sendMessage?chat_id="+str(chat_id)+ \
                      "&text="+message)

def getUpdates():
  return json.loads(requests.get(url = URL+"getUpdates").text)


r = getUpdates()
if r['ok']:
  for message in r['result']:
    if not checkUpdateId(message['update_id']):
      checkMessage(message)

