import requests
import winsound
import time 
from datetime import date

d = date.today()
date_str = '{}-{}-{}'.format(d.day,d.month,d.year)
url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=363&date={}'.format(date_str)
headers = {
    'authority': 'cdn-api.co-vin.in',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '^\\^',
    'sec-ch-ua-mobile': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}



# this function alerts your slack, enter the weebhook for your channel/user, don't call this function if you don't wanna alert using slack 
def slackpost(centre_name, pincode):
    """
    curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' https://hooks.slack.com/services/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
    """
    headers = {
    'Content-type': 'application/json',
    }

    data = {
        "text" : "vaccine slot at {} pincode: {}".format(centre_name, pincode)
    }

    data = str(data)

    response = requests.post('https://hooks.slack.com/services/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', data=data)


while True:
    try:
        response = requests.get(url, headers = headers)
        #print(response.text)
        resp_json = response.json()
        center_list = resp_json['centers']

        for center in center_list:
            if center['block_name'] == 'Haveli':
                session_list = center['sessions']
                for session in session_list:
                    if session['min_age_limit'] == 18 and session['available_capacity'] > 0:
                        #insert whatever alert you want
                        print(center['name'], center['pincode'])
                        slackpost(center['name'], center['pincode'])
                        #winsound is only for windows, will hear an ugly beep
                        winsound.Beep(440,5000)
    
    #poll every 5 seconds
    except Exception as e:
        print(response)
    time.sleep(5)
