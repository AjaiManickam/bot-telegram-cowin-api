from datetime import datetime
from os import environ

from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater

import CONSTANTS
import KEY
import methods as get
import responses

print ('Initializing Bot')

#Command and Message handlers
def start_command(update, context):
          get.print_input_info(update)
          print(f'Bot: {CONSTANTS.STR_REPLY_TO_START_COMMAND}')
          update.message.reply_text(f'Hey {update.effective_user.first_name}, {CONSTANTS.STR_REPLY_TO_START_COMMAND}')

def help_command(update, context):
          get.print_input_info(update)
          print('Bot: {Sending back help text}')
          update.message.reply_text(f'{update.effective_user.first_name}, {CONSTANTS.STR_REPLY_TO_HELP_COMMAND}')

def vaccine_cbe_command(update, context):
          get.print_input_info(update)
          date = datetime.today().strftime('%d-%m-%Y')
          vaccine_info = get.vaccine_info_as_text(get.get_available_sessions_by_district_on_date(CONSTANTS.DIST_ID_CBE,date))
          result_text = get.get_text_as_list(vaccine_info)
          for text in result_text:
                    print(f'Bot: {text}')
                    update.message.reply_text(text)
          print(f'Data sent back successfully to {update.effective_user.username}')

def vaccine_poy_command(update, context):
          get.print_input_info(update)
          date = datetime.today().strftime('%d-%m-%Y')
          list_available_sessions = get.get_available_sessions_by_district_on_date(CONSTANTS.DIST_ID_CBE,date)
          poy_available_sessions = get.available_sessions_in_poy_list(list_available_sessions)
          result_text = get.get_text_as_list(get.vaccine_info_as_text(poy_available_sessions))
          for text in result_text:
                    print(f'Bot: {text}')
                    update.message.reply_text(text)
          print(f'Data sent back successfully to {update.effective_user.username}')

def seven_day_appt_cbe_command(update,context):
          get.print_input_info(update)
          date = datetime.today().strftime('%d-%m-%Y')
          list_available_sessions = get.get_seven_day_available_sessions_by_district(CONSTANTS.DIST_ID_CBE,date)
          text = get.vaccine_info_as_text(list_available_sessions,'district_calendar')
          result_text = get.get_text_as_list(text)
          for text in result_text:
                    print(f'Bot: {text}')
                    update.message.reply_text(text)
          print(f'Data sent back successfully to {update.effective_user.username}')

def handle_message(update, context):
          get.print_input_info(update)
          text = str(update.message.text).lower()
          response = responses.respond_with(text,update)
          print(f'Bot: {response}')
          update.message.reply_text(response)

def error(update, context):
          print(f'Update {update} caused error {context.error}')

def main():
          api_key = environ['API_KEY']
          updater = Updater(api_key, use_context=True)
          dp = updater.dispatcher
          
          #generic commands
          dp.add_handler(CommandHandler("start",start_command))
          dp.add_handler(CommandHandler("help",help_command))

          #custom commands
          dp.add_handler(CommandHandler("cbe",vaccine_cbe_command))
          dp.add_handler(CommandHandler("poy",vaccine_poy_command))
          dp.add_handler(CommandHandler("7dcbe",seven_day_appt_cbe_command))

          #Message and Error Handling
          dp.add_handler(MessageHandler(Filters.text,handle_message))
          dp.add_error_handler(error)

          print('Bot is started...')
          updater.start_polling()
          updater.idle()

main()