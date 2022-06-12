import imp
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os



# 创建你的机器人
MONGO_URI = 'mongodb://localhost:27017/chatterbot'

# 创建你的机器人
chatbot = ChatBot(
    'KafuChino',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database_uri=MONGO_URI)

# 训练你的机器人
# 这是训练对话
conversation = []
for line in open("D:\\python\\cheatbot\\data.txt","rb"):
    conversation.append(line.decode("utf-8"))
trainer = ListTrainer(chatbot)
trainer.train(conversation)

# 跟你的机器人对话
while True:
    try:
        user_input = input('>>> ').strip()
        bot_response = chatbot.get_response(user_input)
        print(bot_response)
    except (KeyboardInterrupt, EOFError, SystemExit):
        break