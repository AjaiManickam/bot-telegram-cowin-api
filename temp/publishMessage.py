import requests
import KEY

api_token = KEY.API_KEY
chat_id = "your chat ID here"
message_id= "the message ID here"
textmsg = "MESSAGE"


URL = f"https://api.telegram.org/bot{api_token}/sendMessage?chat_id={chat_id}&text={textmsg}"
#URL =  f"https://api.telegram.org/bot{api_token}/pinChatMessage?chat_id={chat_id}&message_id={message_id}"
print(URL)
response = requests.get(URL)
print(response)
if (response.status_code == 200):
          print("Message sent successfully!")
else:
          print(response.text)
          print("Error sending!")