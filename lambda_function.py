
##############################
# Builders
##############################

#Authors: Bilal Qadar, Harnish Patel 

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

def name(event,context,user_name): 
    
    phrase  = "Hi "+user_name+" . How is it going?"
    display = "Hi, "+user_name
    return statement(display,phrase)
    
def badDay(event,context,user_name):
    #TODO: Varying responses
    
    slots = event['request']['intent']['slots']
    phrase = "I am sorry you had a "+slots['day_type']['value']+" day. Tell me more about it." 
    return statement("Tell me more!",phrase)
        
def breakup(event,context,user_name):
    #TODO: Add a slot type so Alexa better understands gender 
    phrase = "Everything will be alright "+user_name+". Things always change for the better. Tell me more?"
    
    return statement("I love you",phrase)
    
def tellMeMore(event,context,user_name): 

    return statement("title","I'm glad you're feeling better. Thank you for talking. I'm always here if you need other recourses of just want to talk.")

def dontTellMeMore(event,context,user_name):
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
    return statement("title", "Hello, who am I speaking with?")

def try_again(event,context): 
    return statement('Sorry I didnt get that. Could you repeat it please?')


##############################
# Routing
##############################


def intent_router(event, context):
    intent = event['request']['intent']['name']
    user_name = ''
    
    # Custom Intents
    
    if intent == "name_intent":
        user_name = event['request']['intent']['slots']['name']['value']
        return name(event,context,user_name)
        
    if intent == "badDay": 
        return badDay(event,context,user_name)
    
    elif intent == "relationships": 
        return breakup(event,context,user_name)
        
    elif intent == "talkMore":
        
        conversation_continue = ['yes','sure','yeah','okay']
        conversation_stop = ['no','nope', 'fuck']
        user_response = event['request']['intent']['slots']['option']['value']
        
        if user_response in conversation_stop:
            return dontTellMeMore(event,context,user_name)
        elif user_response in conversation_continue: 
            return tellMeMore(event,context,user_name)
        else: 
            statement(":)","I know a lot is going on. Keep talking to me about it!")


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
