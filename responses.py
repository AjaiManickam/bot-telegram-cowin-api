import Constants as keys

def response_msg(input_text,update):
          user_message = input_text.lower()
          msg_list = {'hi','hello','hey','yo','bro','dude'}
          if any(ele in user_message for ele in msg_list):
                    name = update.effective_user.first_name
                    return f'Hello {name}, {keys.STR_REPLY_TO_GREETINGS}'
          else:
                    return keys.STR_REPLY_TO_UNRECOGNIZED_TEXT
