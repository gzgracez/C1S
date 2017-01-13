from ask import alexa
import urllib2
import json
import helpers


def lambda_handler(request_obj, context={}):
    return alexa.route_request(request_obj)

@alexa.default_handler()
def default_handler(request):
    return launch_request_handler(request)

@alexa.request_handler("LaunchRequest")
def launch_request_handler(request):
    return alexa.create_response(message="Hello! I am here to be your account manager. What would you like to know?",
                                 reprompt_message='You can ask about your bank account and I will tell you!')

@alexa.request_handler(request_type="SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="Be wise in your spending today! Goodbye.", end_session=True)

@alexa.intent_handler("GetCurrentBalance")
def get_current_balance_handler(request):
    helpers.updateAllocations("58000d58360f81f104543d82")
    #net balance
    net_balance = helpers.getTotalBalance("58000d58360f81f104543d82")
    #set initial return message
    message = "Your current net balance is ${}".format(str(net_balance))
    #conditionals if balance does not exist
    if net_balance <= 0:
        message = message + "Be careful of your spending!"
    return alexa.create_response(message=message, end_session=True)

@alexa.intent_handler("GetCreditBalance")
def get_credit_balance_handler(request):
    helpers.updateAllocations("58000d58360f81f104543d82")
    #retrieve current balance of the credit card
    credit_balance = helpers.getCreditCardBalance("58000d58360f81f104543d82")
    #set initial return message
    message = "Credit card current balance is ${}".format(str(credit_balance))
    #conditionals if balance does not exist
    if credit_balance <= 0:
        message = message + "Be careful of your spending!"
    return alexa.create_response(message=message, end_session=True)

@alexa.intent_handler("GetCheckingBalance")
def get_checking_balance_handler(request):
    helpers.updateAllocations("58000d58360f81f104543d82")
    #retrieve current balance of the checking account
    checking_balance = helpers.getCheckingBalance("58000d58360f81f104543d82")
    #set initial return message
    message = "Checking account current balance is ${}".format(str(checking_balance))
    #conditionals if balance does not exist
    if checking_balance <= 0:
        message = message + "Be careful of your spending!"
    return alexa.create_response(message=message, end_session=True)


@alexa.intent_handler("GiveSuggestions")
def give_suggestions_handler(request):
    helpers.updateAllocations("58000d58360f81f104543d82")
    #retrieve what category the user wanted
    category = str(request.get_slot_value("category"))
    #dayInteger
    dayInteger = 0    
    #retrieve what day of the week it is
    day = str(request.get_slot_value("day")).lower()

    if day == "monday":
        dayInteger = 0
    elif day == "tuesday":
        dayInteger = 1
    elif day == "wednesday":
        dayInteger = 2
    elif day == "thursday":
        dayInteger = 3
    elif day == "friday":
        dayInteger = 4
    elif day == "satuday":
        dayInteger = 5
    elif day == "sunday":
        dayInteger = 6
    else:
        dayInteger = 0

    #start with empty string
    message = ""

    print dayInteger

    grocery_value = helpers.calculateSuggestedByCategory("58000d58360f81f104543d82", "grocery", dayInteger)
    print grocery_value
    if grocery_value == None:
        grocery_value = 0

    food_value = helpers.calculateSuggestedByCategory("58000d58360f81f104543d82", "food", dayInteger)
    if food_value == None:
        food_value = 0

    gas_value = helpers.calculateSuggestedByCategory("58000d58360f81f104543d82", "gas", dayInteger)
    if gas_value == None:
        gas_value = 0

    shopping_value = helpers.calculateSuggestedByCategory("58000d58360f81f104543d82", "shopping", dayInteger)
    if shopping_value == None:
        shopping_value = 0

    clothing_value = helpers.calculateSuggestedByCategory("58000d58360f81f104543d82", "clothing", dayInteger)
    if clothing_value == None:
        clothing_value = 0

    if category == "None" and day != "none":
        total_value = grocery_value + food_value + gas_value + shopping_value + clothing_value
        message = message + "On {}, you can spend {} dollars".format(day, total_value)
        return alexa.create_response(message=message, end_session=True)

    elif day == "none" and category != "None":
        today_value = 0
        if category == "groceries" or category=="grocery":
            today_value = grocery_value
        elif category == "food" or category == "foods":
            today_value = food_value
        elif category == "gas":
            today_value = gas_value
        elif category == "shopping":
            today_value == shopping_value
        elif category == "clothes" or category == "clothings":
            today_value = clothing_value
        message = message + "Today, you can spend {} dollars on {}".format(today_value, category)
        return alexa.create_response(message=message, end_session=True)

    elif day == "None" and category == "none":
        message = message + "Please enter category and day."
        return alexa.create_response(message=message, end_session=False)

    else:
        if category == "groceries" or category=="grocery":
            message = message + "For {} on {}, you should spend {} dollars.".format(category, day, grocery_value)
        elif category == "food" or category == "foods":
            message = message + "For {} on {}, you should spend {} dollars.".format(category, day, food_value)
        elif category == "gas":
            message = message + "For {} on {}, you should spend {} dollars.".format(category, day, gas_value)
        elif category == "shopping":
            message = message + "For {} on {}, you should spend {} dollars.".format(category, day, shopping_value)
        elif category == "clothes" or category == "clothings":
            message = message + "For {} on {}, you should spend {} dollars.".format(category, day, clothing_value)
        return alexa.create_response(message=message, end_session=True)


@alexa.intent_handler("Allocations")
def allocate(request):
    helpers.updateAllocations("58000d58360f81f104543d82")
    #retrieve amount 
    amount = str(request.get_slot_value("amount"))
    #retrieve what category the user wanted
    category = str(request.get_slot_value("category"))
    #retrieve what day of the week it is
    date = str(request.get_slot_value("date"))
    #start with empty string
    message = ""
    #if the user didn't provide a slot, tell it to try again
    if category == "None":
        message = message + "Please try again and specify the category."
        return alexa.create_response(message=message, end_session=False)
    elif date == "None":
        message = message + "Please try again and specify the date."
        return alexa.create_response(message=message, end_session=False)
    elif amount == "None":
        message = message + "Please try again and specify the amount."
        return alexa.create_response(message=message, end_session=False)
    else:
        helpers.addAllocation("58000d58360f81f104543d82", category, amount, date)
        message = message + "It has been successfully allocated."
        return alexa.create_response(message=message, end_session=True)


@alexa.intent_handler("AMAZON.HelpIntent")
def help_intent_handler(request):
    return alexa.create_response(message="This skill gives information about your bank account.", end_session=False)

@alexa.intent_handler("AMAZON.StopIntent")
def stop_intent_handler(request):
    return alexa.create_response(message="Bye!", end_session=True)

@alexa.intent_handler("AMAZON.CancelIntent")
def cancel_intent_handler(request):
    return alexa.create_response(message="Bye!", end_session=True)
