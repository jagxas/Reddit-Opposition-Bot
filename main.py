import praw
import os
import constants
import random
import re
from unidecode import unidecode
from datetime import datetime
from keep_alive import keep_alive

reddit = praw.Reddit(client_id=os.getenv('client_id'),
                     client_secret=os.getenv('client_secret'),
                     username=os.getenv('username'),
                     password=os.getenv('password'),
                     user_agent="<OppositionBot1.0>")


def preProcess(comment):
  comment = comment.lower()
  comment = re.sub(r'[^A-Za-z0-9 ]+', '', comment)
  comment = unidecode(comment)

  return comment


lastPosted = 0


class OppositionBot:

  def __init__(self):
    global lastPosted
    self.responses = constants.clauses
    lastPosted = 0

  def find_fitting_comment(self, comment):
    print(abs(lastPosted - datetime.now().minute))
    for i in constants.keywords:
      if preProcess(comment.body).__contains__(i):
        if self.avoid_ban():
          print(comment.body)
          self.send_reply(comment)
          break

  def avoid_ban(self):
    global lastPosted
    if (abs(lastPosted - datetime.now().minute)) >= 10:
      return True
    elif (abs(lastPosted - datetime.now().minute)) < 10:
      return False

  def send_reply(self, comment):
    global lastPosted
    replyMessage = self.takeRandomThree()
    try:
      comment.reply(replyMessage)
      print(replyMessage)
      lastPosted = datetime.now().minute
    except Exception as e:
      pass

  def takeRandomThree(self):
    first = constants.clauses[random.randint(0, len(constants.clauses))]
    second = constants.clauses[random.randint(0, len(constants.clauses))]
    third = constants.clauses[random.randint(0, len(constants.clauses))]

    reply_text = """
    Merhaba, yorumunda siyasi ögeler bulunduğu için bu mesajı yazıyorum. Aşağıda 6'lı Masanın Mutabakat Metni'nden rastgele 3 madde bırakıyorum:
    
    1){}
    2){}
    3){}

    Birçok insan uzun yazılar okumayı sevmiyor. Eh, haklılar. Benim, yani Altili-Masa-Bot'un amacı insanlara bu maddeleri olabildiğince duyurabilmek. Herhangi bir siyasi partiyle alakam yok ve tamamen bağımsız 3. kişiler tarafından programlandım. İyi günler dilerim :)
    """.format(first, second, third)
    return reply_text


keep_alive()

bot = OppositionBot()
subreddit = reddit.subreddit("turkey")

for comment in subreddit.stream.comments(skip_existing=True):
  bot.find_fitting_comment(comment)
