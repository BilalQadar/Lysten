
##############################
# Builders
##############################

#Authors: Bilal Qadar, Harnish Patel ************HIRE US PLS***************

def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech


def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    response['reprompt'] = message
    return response


def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = body
    return card


##############################
# Responses
##############################


def conversation(title, body, session_attributes):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = False
    return build_response(speechlet, session_attributes=session_attributes)


def statement(title, body):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = False
    return build_response(speechlet)


def continue_dialog():
    message = {}
    message['shouldEndSession'] = False
    message['directives'] = [{'type': 'Dialog.Delegate'}]
    return build_response(message)


##############################
# Custom Intents
##############################

def badDay(event,context):
    #TODO: Add a slot type so Alexa better understands what kind of day you are having
    #TODO: Varying responses
    slots = event['request']['intent']['slots']
    phrase = "I am sorry you had a "+slots['day_type']['value']+" day. Tell me more about it." 
    return statement("Tell me more!",phrase)
        
def breakup(event,context):
    #TODO: Add a slot type so Alexa better understands genger 
    
    return statement("title","Things always change for the better. Tell me more?")
    
def tellMeMore(event,context): 

    return statement("title","I'm glad you're feeling better. Thank you for talking. I'm always here if you need other recourses of just want to talk.")

def dontTellMeMore(event,context):
    #TODO: End session call when 'goodbye' is heard
    return statement("title","Ok. I am always here if you need me. Let me know if you would like to talk to someone else, I have resources for you.")

##############################
# Required Intents
##############################


def cancel_intent():
    return statement("CancelIntent", "You want to cancel")	#don't use CancelIntent as title it causes code reference error during certification 


def help_intent():
    return statement("CancelIntent", "You want help")		#same here don't use CancelIntent


def stop_intent():
    return statement("StopIntent", "You want to stop")		#here also don't use StopIntent


##############################
# On Launch
##############################


def on_launch(event, context):
    #TODO: Dynamic greeting depending on tone of user
    return statement("title", "Hello, how can I help?")

def try_again(event,context): 
    return statement('Sorry I didnt get that. Could you repeat it please?')


##############################
# Routing
##############################


def intent_router(event, context):
    intent = event['request']['intent']['name']

    # Custom Intents
    
    if intent == "badDay": 
        return badDay(event,context)
    
    elif intent == "relationships": 
        #Detect when a breakup happens using slot_type
        return breakup(event,context)
        
    elif intent == "talkMore":
        #Detect when a breakup happens using a slot_type
        return dontTellMeMore(event,context)


    # Required Intents

    if intent == "AMAZON.CancelIntent":
        return cancel_intent()

    if intent == "AMAZON.HelpIntent":
        return help_intent()

    if intent == "AMAZON.StopIntent":
        return stop_intent()


##############################
# Program Entry
##############################


def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event, context)

    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)
    else: 
        return try_again(event,context)
