from datetime import datetime
import requests
import CONSTANTS


#Methods                 
def get_data_from_server(end_point,filter_criteria_string):
          print(f'Fetching data from the server')
          url = f'{CONSTANTS.URL_BASE}{end_point}{filter_criteria_string}'
          browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
          print(url)
          response = requests.get(url, headers=browser_header)
          print(f'{response} - {response.reason}')
          return response
          
def get_available_sessions_by_district_on_date(district_id,date):
          end_point = CONSTANTS.URL_ENDPOINT_FINDBYDISTRICT
          filter_criteria_string = f'?district_id={district_id}&date={date}'
          response = get_data_from_server(end_point,filter_criteria_string)
          if response.status_code == 200:
                    list_sessions = response.json()["sessions"]
                    for i in range(len(list_sessions)-1,-1,-1):
                              if list_sessions[i]["available_capacity"] <= 0:
                                        list_sessions.pop(i)
                    return list_sessions
          return []

def get_seven_day_available_sessions_by_district(district_id,date):
          end_point = CONSTANTS.URL_ENDPOINT_CALENDARBYDISTRICT
          filter_criteria_string = f'?district_id={district_id}&date={date}'
          response = get_data_from_server(end_point,filter_criteria_string)
          if response.status_code == 200:
                    list_sessions = response.json()["centers"]
                    for i in range(len(list_sessions)-1,-1,-1):
                              for j in range(len(list_sessions[i]["sessions"])-1,-1,-1):
                                        if list_sessions[i]["sessions"][j]["available_capacity"] <= 0:
                                                  list_sessions[i]["sessions"].pop(j)
                              if len(list_sessions[i]["sessions"]) == 0:
                                     list_sessions.pop(i)   
                    return list_sessions
          return []

def available_sessions_in_poy_list(list_sessions):
          for i in range(len(list_sessions)-1,-1,-1):
                    if not(str(list_sessions[i]['pincode'])[0:3] == "642" or str(list_sessions[i]['pincode']) == '641202'): list_sessions.pop(i)
          return list_sessions
          
def vaccine_info_as_text(list_available_sessions,mode='district_on_date'):
          if len(list_available_sessions)==0:
                 final_text = CONSTANTS.STR_SLOTS_NOT_AVAILABLE
          else:
                 final_text = ''
                 for session in list_available_sessions:
                        final_text = final_text + info_formatted(session,mode)
          return final_text

def get_text_as_list(text_string):
          max_char = CONSTANTS.MAX_CHARS_ALLOWED_IN_TELEGRAM_MSG
          return [text_string[i:i + max_char] for i in range(0, len(text_string), max_char)]
          
def info_formatted(session,mode='district_on_date'):
       if mode=='district_calendar':
              full_address = f"\n{session['name']}, {session['address']}, {session['block_name']}, {session['district_name']} - {session['pincode']}\nFee type: {session['fee_type']}\n"
              sub = ''
              for slot in session["sessions"]:
                     sub = sub + f"\nDate: {slot['date']}\nAge Group: {slot['min_age_limit']}+\nVaccine: {slot['vaccine']}\nTotal Available Capacity: {slot['available_capacity']}\nDose 1 capacity: {slot['available_capacity_dose1']}\nDose 2 capacity: {slot['available_capacity_dose2']}\n"
              end_text = "\nRegister: https://selfregistration.cowin.gov.in/\n______________________________________\n"
              return f"{full_address}{sub}{end_text}"
       else:
              rupee_symbol =  u"\u20B9"
              fee = f"{rupee_symbol} {session['fee']}"
              full_address = f"{session['name']}, {session['address']}, {session['block_name']}, {session['district_name']} - {session['pincode']}"
              return f"\n{full_address}\n\nAge Group: {session['min_age_limit']}\nVaccine: {session['vaccine']}\nTotal Available Capacity: {session['available_capacity']}\nDose 1 capacity: {session['available_capacity_dose1']}\nDose 2 capacity: {session['available_capacity_dose2']}\nFee: {fee}\n\nRegister: https://selfregistration.cowin.gov.in/\n______________________________________\n"

def print_input_info(update):
          print(f'-------------------{str(datetime.now())} {update.effective_user["first_name"]} {update.effective_user["last_name"]} ({update.effective_user["username"]} from {update.effective_chat["title"]} | {update.effective_chat["id"]})-------------------\n{update.effective_user["first_name"]} {update.effective_user["last_name"]}: {update.message.text}')