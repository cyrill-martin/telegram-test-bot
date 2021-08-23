
import os
import logging
import time
from dotenv import load_dotenv
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

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

# You may also want to take a look at https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example

def start(update: Update, context: CallbackContext):
  keyboard = [
    [
      InlineKeyboardButton("Option 1", callback_data="1"),
      InlineKeyboardButton("Option 2", callback_data="2"),
    ],
    [
      InlineKeyboardButton("Option 3", callback_data="3")],
    ]

  reply_markup = InlineKeyboardMarkup(keyboard)

  context.bot.send_message(chat_id=get_chat_id(update), text="What would you like to do?", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    query.edit_message_text(text=f"You chose option {query.data}")

    if query.data == "1":
      option_1(update, context)
    else: 
      option_sth(update, context, query.data)

def option_1(update, context):
  reply = "Lets proceed with option 1"
  send_reply(context, get_chat_id(update), reply)

def option_sth(update, context, option): 
  reply = f"Lets proceed with option {option}"
  send_reply(context, get_chat_id(update), reply)

def sk8(update, context):
  reply = "Do a kickflip!"
  send_reply(context, get_chat_id(update), reply)

def main():
  # Create the telegram bot
  updater = Updater(token=bot_token, use_context=True)

  # Log to terminal
  logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
  
  # Set the bot handlers
  updater.dispatcher.add_handler(CommandHandler("start", start))
  updater.dispatcher.add_handler(CallbackQueryHandler(button))
  updater.dispatcher.add_handler(CommandHandler("sk8", sk8))

  if bot_mode == "webhook":
    # Use the webhook if deployed to Heroku
    port = int(os.environ.get("PORT", 8443))
    updater.start_webhook(listen="0.0.0.0", 
                          port=port,
                          url_path=bot_token, 
                          webhook_url=f"{bot_url}{bot_token}")
    updater.idle()
  else:
    # Use polling on your local machine
    updater.start_polling()

if __name__ == "__main__":
  main()
