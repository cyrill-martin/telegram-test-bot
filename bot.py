
import os
import logging
import time
from dotenv import load_dotenv
from telegram import ChatAction
from telegram.ext import Updater, CommandHandler

# Load your environment variables from the .env file
load_dotenv()

# Set the telegram bot credentials
bot_token = os.environ.get("BOT_TOKEN")
bot_url = os.environ.get("BOT_URL")
bot_mode = os.environ.get("BOT_MODE")

# Get chat-ID from update
def get_chat_id(update):
  return update.effective_chat.id

# Mimic typing of the bot
def show_typing(context, chat_id): 
  context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING, timeout=1)
  time.sleep(1)

# Send the actual reply
def send_reply(context, chat_id, text):
  show_typing(context, chat_id)
  context.bot.send_message(chat_id=chat_id, text=text)

################################
# Create telegram bot handlers #
################################
def start(update, context):
  reply = "Hello, I'm your telegram test bot."
  send_reply(context, get_chat_id(update), reply)

def test(update, context):
  reply = "Congrats, you tested the bot."
  send_reply(context, get_chat_id(update), reply)

def cool(update, context):
  reply = "Yes, that's cool."
  send_reply(context, get_chat_id(update), reply)

def sure(update, context):
  reply = "I'm sure."
  send_reply(context, get_chat_id(update), reply)

def sk8(update, context):
  reply = "Do a kickflip!"
  send_reply(context, get_chat_id(update), reply)

def main():
  # Create the telegram bot
  updater = Updater(token=bot_token, use_context=True)
  dispatcher = updater.dispatcher

  logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
  
  # Set the bot handlers
  start_handler = CommandHandler("start", start)
  test_handler = CommandHandler("test", test)
  cool_handler = CommandHandler("cool", cool)
  sure_handler = CommandHandler("sure", sure)
  sk8_handler = CommandHandler("sk8", sk8)
  
  dispatcher.add_handler(start_handler)
  dispatcher.add_handler(test_handler)
  dispatcher.add_handler(cool_handler)
  dispatcher.add_handler(sure_handler)
  dispatcher.add_handler(sk8_handler)

  if bot_mode == "webhook":
    # Use the webhook in production
    port = int(os.environ.get("PORT", 8443))
    updater.start_webhook(listen="0.0.0.0", 
                          port=port,
                          url_path=bot_token, 
                          webhook_url=f"{bot_url}{bot_token}")
    updater.idle()
  else:
    # Use polling locally
    updater.start_polling()

if __name__ == "__main__":
  main()
