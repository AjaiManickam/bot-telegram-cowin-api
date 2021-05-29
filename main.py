from telegram import bot
from telegram.ext import *
import methods as get
import Constants as keys
import responses as R
import key

print ('Initializing Bot')

#Command and Message handlers
def start_command(update, context):
          get.print_input_info(update)
          print(f'Bot: {keys.STR_REPLY_TO_START_COMMAND}')
          update.message.reply_text(f'Hey {update.effective_user.first_name}, {keys.STR_REPLY_TO_START_COMMAND}')

def help_command(update, context):
          get.print_input_info(update)
          print('Bot: {Sending back help text}')
          update.message.reply_text(f'{update.effective_user.first_name}, {keys.STR_REPLY_TO_HELP_COMMAND}')

def vaccine_cbe_command(update, context):
          get.print_input_info(update)
          vaccine_info = get.vaccine_info_as_text(539)
          max_char = keys.MAX_CHARS_ALLOWED_IN_TELEGRAM_MSG
          if len(vaccine_info) > max_char:
                    print('Splitting the data and sending in smaller chunks since its too large...')
                    final_note = ''
                    max_typable_char = max_char - len(final_note)
                    for x in range(0, len(vaccine_info), max_typable_char):
                              chunk_text = vaccine_info[x:x+max_typable_char]+final_note
                              print(f'Bot: {chunk_text}')
                              update.message.reply_text(chunk_text)
          else:
                    print(f'Bot: {vaccine_info}')
                    update.message.reply_text(vaccine_info)
          print(f'Data sent back successfully to {update.effective_user.username}')

def vaccine_poy_command(update, context):
          get.print_input_info(update)
          list_available_sessions = get.vaccine_availability_by_district(539)
          is_slots_available_for_POY = False
          final_text = ''
          for session in list_available_sessions:
                    if str(session['pincode'])[0:3] == "642" or str(session['pincode'])== '641202':
                              is_slots_available_for_POY = True
                              final_text = final_text + get.info_formatted(session)
          if not is_slots_available_for_POY:
                    final_text = keys.STR_SLOTS_NOT_AVAILABLE
          print(f'Bot: {final_text}')
          update.message.reply_text(final_text)
          print(f'Data sent back successfully to {update.effective_user.username}')

def handle_message(update, context):
          get.print_input_info(update)
          text = str(update.message.text).lower()
          response = R.response_msg(text,update)
          print(f'Bot: {response}')
          update.message.reply_text(response)

def error(update, context):
          print(f'Update {update} caused error {context.error}')

def main():
          updater = Updater(key.API_KEY, use_context=True)
          dp = updater.dispatcher
          #generic commands
          dp.add_handler(CommandHandler("start",start_command))
          dp.add_handler(CommandHandler("help",help_command))

          #custom commands
          dp.add_handler(CommandHandler("vaccine_cbe",vaccine_cbe_command))
          dp.add_handler(CommandHandler("vaccine_poy",vaccine_poy_command))

          #Message and Error Handling
          dp.add_handler(MessageHandler(Filters.text,handle_message))
          dp.add_error_handler(error)

          print('Bot is started...')
          updater.start_polling()
          updater.idle()

main()




