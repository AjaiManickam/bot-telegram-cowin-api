import CONSTANTS

def respond_with(input_text,update):
          user_message = input_text.lower()
          msg_list = {'hi','hello','hai','hey','bro','dude'}
          if any(ele in user_message for ele in msg_list):
                    return f'Hello {update.effective_user.first_name}, {CONSTANTS.STR_REPLY_TO_GREETINGS}'
          else:
                    return CONSTANTS.STR_REPLY_TO_UNRECOGNIZED_TEXT