import requests
import Constants as keys
from datetime import datetime

#Methods                      
def vaccine_availability_by_district(district_id):
          print(f'Getting data for the district ID - {district_id}...')
          date = datetime.today().strftime('%d-%m-%Y')
          url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={district_id}&date={date}'
          browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
          print(url)
          response = requests.get(url, headers=browser_header)
          print(f'{response} - {response.reason}')
          if response.status_code == 200:
                    return get_sessions_only_with_vaccine_available(response)
          return []
          

def get_sessions_only_with_vaccine_available(success_response):
          list_sessions = success_response.json()["sessions"]
          for i in range(len(list_sessions)-1,-1,-1):
                    if list_sessions[i]["available_capacity"] <= 0: list_sessions.pop(i)
          return list_sessions
          
def vaccine_info_as_text(district_id):
          list_available_sessions = vaccine_availability_by_district(district_id)
          final_text = ''
          if len(list_available_sessions)==0:
                    final_text = keys.STR_SLOTS_NOT_AVAILABLE
          else:
                    for session in list_available_sessions:
                              final_text = final_text + info_formatted(session)
          return final_text

def info_formatted(session):
          rupee_symbol =  u"\u20B9"
          fee = f"{rupee_symbol} {session['fee']}"
          full_address = f"{session['name']}, {session['address']}, {session['block_name']} - {session['pincode']}"
          return f"\nName: {full_address}\nTotal Available Capacity: {session['available_capacity']}\nDose 1 capacity: {session['available_capacity_dose1']}\nDose 2 capacity: {session['available_capacity_dose2']}\nAge Group: {session['min_age_limit']}+\nFee: {fee}\nVaccine: {session['vaccine']}\n\nRegister: https://selfregistration.cowin.gov.in/\n-------------------------------------------------------------"

def print_input_info(update):
          print(f'{str(datetime.now())} {update.effective_user["username"]} (from {update.effective_chat["title"]} | {update.effective_chat["id"]}) :: {update.message.text}')
