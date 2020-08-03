from flask import Flask, request
import requests
from currentCasesState import final_dict
import drivingDistance
import currentCasesCounty
from countiesCasesJSON import countiesJSON

app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = ''# <paste your verify token here>
PAGE_ACCESS_TOKEN = 'EAAJgLyjDxGEBAJOxYrZCBQSxxymf1BWsbY7TFMbWejAsZBOXjdQe5JqSIzz5r5duXGtZC8hhoTBS1INRnhb406fln9cBO5CKhCUL4oI36EbgxUuqgQ0hNnOGMWPoG0ZBG1mAkNy6rcMzyF5NRiZAROGgLJNSxeN0ZAbTIFIVCb5AZDZD'# paste your page access token here>"

sender_information = {}

hello_message = 'Hi there! This CovidBot. This chatbot is designed in order to help you navigate your way through this pandemic as ' \
                'easily and efficient as possible. You can search for nearest test center by typing: Find me the nearest test center. You can search for local ' \
                'and state statistics about the pandemic by typing: How many cases are there near me. You will be asked to provide your zip code and possibly your ' \
                'county name to provide you with the best results. You can also find some useful daily news insights on the virus by typing in: ' \
                'Give me daily updates. This chatbot does not store your data and is made use friendly in order to be interactive and user friendly!'

def get_bot_response(message):
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    return message


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    global final_county
    send_message(sender, hello_message)
    response = get_bot_response(message)

    if response == "Give me daily updates":
        message = final_dict['Quick News']
        send_message(sender, message)

    elif response == 'Find me the nearest test center':
        send_message(sender, "Please text your zip code: ")
        zip_code = get_bot_response(message)

        sender_information[sender] = [zip_code]

        send_message(sender, "This may take a minute: ")
        test_centers= drivingDistance.process_distance(zip_code, drivingDistance.add2)
        send_message(sender, test_centers)

    elif response == "How many cases are there near me" or response == "How many cases are there near me?":
        send_message(sender, "Local or statewide?")
        local_state = get_bot_response(message)
        if local_state == "local" or local_state == "Local":
            if sender in sender_information.keys():
                counties = currentCasesCounty.find_county_by_zip_code(sender_information[sender])
                if len(counties) > 1:
                    send_message(sender, "County is not recognized, perhaps you made a typo?")
                    county = get_bot_response(message)
                    while county not in counties:
                        send_message(sender, "County is not recognized, perhaps you made a typo?")
                        send_message(sender, "Which one of these counties do you live in?")
                        final_county = get_bot_response(message)
                else:
                    final_county = counties[0]
            else:
                send_message(sender, "Can you please provide you zip code?")
                zip_code = get_bot_response(message)
                counties = currentCasesCounty.find_county_by_zip_code(zip_code)
                if len(counties) > 1:
                    send_message(sender, "County is not recognized, perhaps you made a typo?")
                    county = get_bot_response(message)
                    while county not in counties:
                        send_message(sender, "County is not recognized, perhaps you made a typo?")
                        send_message(sender, "Which one of these counties do you live in?")
                        final_county = get_bot_response(message)
                else:
                    final_county = counties[0]
            cases_number = countiesJSON[final_county][0]
            death_number = countiesJSON[final_county][1]
            send_message(sender, "There are {} cases and {} deaths in {} county".format(cases_number, death_number, final_county))
        elif response == "state" or response == "State" or response == "statewide" or response == "Statewide":
            send_message(sender, "There are {} cases and {} deaths in NY state".format(final_dict['Total Confirmed Cases'], final_dict['Total Deaths']))
            send_message(sender, "I can also provide data for trends, number of tests, positivity rate, and increase in daily positive cases. Which one would you like to look into? If not, simply reply no,")
            answer_yes_no = get_bot_response(message)
            while answer_yes_no == "yes":
                send_message(sender, "Which statistic would you like to research?")
                response = get_bot_response(message)
                if response == "trends":
                    send_message(sender, "There were {} new cases today".format(final_dict['Daily Cases Trend']))
                    send_message(sender, "Would you like anything else?")
                    answer_yes_no = get_bot_response(message)
                elif response == 'number of tests':
                    send_message(sender, "The healthcare system has currently tested {} people".format(final_dict['Total Tested']))
                    send_message(sender, "Would you like anything else?")
                    answer_yes_no = get_bot_response(message)
                elif response == 'Positivity Rate':
                    send_message(sender, "The updated postivity rate according to CDC is {}".format(final_dict['Postivity Rate']))
                    send_message(sender, "Would you like anything else?")
                    answer_yes_no = get_bot_response(message)
                elif response == 'Increase in Daily Cases':
                    send_message(sender, "The increase in cases stands at {}".format(final_dict['% Positive Tests Daily']))
                    send_message(sender, "Would you like anything else?")
                    answer_yes_no = get_bot_response(message)
        else:
            send_message(sender, "I'm sorry. I cannot provide data for any other locations")

def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))


@app.route("/webhook")
def listen():
    """This is the main function flask uses to
    listen at the `/webhook` endpoint"""
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                respond(sender_id, text)

        return "ok"

def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()