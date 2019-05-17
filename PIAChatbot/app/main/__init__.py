from flask import Blueprint

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

bp = Blueprint('main', __name__)
bot = ChatBot("PIA", storage_adapter="chatterbot.storage.SQLStorageAdapter")
# bot.storage.drop()
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.french.greetings")
# trainer = ListTrainer(bot)
# trainer.train(["Bonjour",
# "Je suis ravie de te rencontrer !",
# "Comment vas-tu ?","Je vais bien, merci. Et toi ?",
# "Je vais bien.",
# "Je te propose d'apprendre a se connaitre un peu plus ! Quel est ton prenom ?",])
	
from app.main import routes