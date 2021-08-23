
import os
import logging
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler

# Load your environment variables from the .env file
load_dotenv()

# Set the telegram bot credentials
bot_token = os.environ.get("BOT_TOKEN")
bot_url = os.environ.get("BOT_URL")
bot_mode = os.environ.get("BOT_MODE")

# Create telegram bot handlers
def start(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id, 
                           text="Hello, I'm your telegram test bot.")

def test(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id,
                           text="Congrats, you tested the bot - again!")

def cool(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id,
                           text="Yes, that's cool.")

def sure(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id,
                           text="I'm sure.")

def sk8(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id,
                           text="Do a kickflip!")

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
