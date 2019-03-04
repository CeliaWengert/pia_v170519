from flask import Blueprint

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

bp = Blueprint('main', __name__)
bot = ChatBot("PIA", storage_adapter="chatterbot.storage.SQLStorageAdapter")
# trainer = ChatterBotCorpusTrainer(bot)
# trainer.train("chatterbot.corpus.english")
	
from app.main import routes