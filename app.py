import time

from flask import Flask, render_template, redirect, flash
import datetime
import RPi.GPIO as GPIO
import uuid

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())
GPIO.setmode(GPIO.BCM)
gpio_to_relay_dict = {
    1: 6,  # represents GPIO 6 is connected to relay 1
    2: 13,
    3: 19,
    4: 26,
    5: 12,
    # 6: 16,
    # 7: 20,
    # 8: 21
}

# create dictionary for what drinks are connected to which tubes
liquid_sources_dict = {
    'coke': 0,
    'vodka': 1,  # 0 represents not available
    'rum': 2,
    'mango_juice': 3,
    'midori': 4,
    'blue_curacao': 5
}
# recipe dict includes each kind of drink, and what ingredients are necessary, as well as their quantity
# based on testing, a value of 20 here represents about 4.5oz of liquid
# so, about a 6.7 is equivalent to roughly one shot. round to 7, we use integers and no need to be super precise
# another lesson: taking liquid out of soda makes a lot of bubbles. need to x3 the amount of soda
# 7: 1.5oz
# 5: 1oz
# 3: 0.5oz
drink_dict = {
    "rum-and-coke": {
        # 5 parts coke to 2 parts rum
        "name": "Rum and Coke",
        "description": "good old classic",
        "recipe": {
            "rum": 7,
            "coke": 60
        }
    },
    "vodka-coke": {
        "name": "Vodka Coke",
        "description": "like rum and coke, but with vodka",
        "recipe": {
            "vodka": 1,
            "coke": 4
        }
    },
    "rainstorm": {
        "name": "The Rainstorm",
        "description": "Green juice",
        "recipe": {
            "vodka": 5,
            "rum": 3,
            "midori": 3,
            "blue_curacao": 3,
            "mango_juice": 20
        }
    }
}

for pin in gpio_to_relay_dict.keys():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

# http://mattrichardson.com/Raspberry-Pi-Flask/
# https://learn.adafruit.com/adafruit-keg-bot?view=all
# https://randomnerdtutorials.com/raspberry-pi-web-server-using-flask-to-control-gpios/
# https://hydrosysblog.wordpress.com/
# https://www.youtube.com/watch?v=3w4tOuRyBSc
# https://www.instructables.com/Raspberry-Pi-With-4-Relay-Module-for-Home-Automati/
# https://www.electronicshub.org/control-a-relay-using-raspberry-pi/
# https://robu.in/how-to-connect-relay-to-raspberry-pi-3/

web_title = "Welcome to 409!"


@app.route("/clean")
def clean():
    # activate all pumps
    for pump, gpio_pin in gpio_to_relay_dict.items():
        activate_relay(gpio_pin)

    # wait to let the water move through
    time.sleep(7)
    for pump, gpio_pin in gpio_to_relay_dict.items():
        deactivate_relay(gpio_pin)


@app.route("/")
def index():
    now = datetime.datetime.now()
    time_string = now.strftime("%Y-%m-%d %H:%M")

    # create a drink list, which will be used in the template. also shows which drinks are available
    drink_list_for_html = []
    for drink, drink_info in drink_dict.items():
        recipe = drink_info['recipe']
        recipe_valid = True
        for ingredient in recipe.keys():
            if liquid_sources_dict[ingredient] == 0:
                # represents an ingredient not attached to a pump
                recipe_valid = False

        if recipe_valid:
            # drink name, description, and status
            drink_list_for_html.append(
                [drink, drink_info['name'], drink_info['description'], 'Available']
            )
        else:
            drink_list_for_html.append(
                [drink, drink_info['name'], drink_info['description'], 'Missing Ingredients']
            )

    template_data = {
        'title': web_title,
        'length': len(drink_list_for_html),
        'drinks': drink_list_for_html
    }
    return render_template('main.html', **template_data)


def make_drink(recipe):
    relays_already_deactivated = set()

    time_elapsed = 0
    longest_time_needed = max(recipe.values())

    # change recipe dict so that we replace the ingredient names with the relay number
    recipe_with_relays = {gpio_to_relay_dict[liquid_sources_dict[ingredient]]: time_left for (ingredient, time_left) in
                          recipe.items()}
    while time_elapsed < longest_time_needed:
        relays_to_activate = [relay for relay, time_left in recipe_with_relays.items() if time_left > 0]
        relays_to_deactivate = [relay for relay, time_left in recipe_with_relays.items() if time_left == 0]
        print(f'relays to activate: {relays_to_activate}')
        print(f'relays to deactivate: {relays_to_deactivate}')
        for relay in relays_to_deactivate:
            if relay not in relays_already_deactivated:
                deactivate_relay(relay)
                relays_already_deactivated.add(relay)
        for relay in relays_to_activate:
            activate_relay(relay)
            recipe_with_relays[relay] -= 1
        time.sleep(1)
        time_elapsed += 1
        print(f'{time_elapsed} elapsed')
    # deactivate all relays
    for relay, _ in recipe_with_relays.items():
        deactivate_relay(relay)


@app.route("/order/<drink>")
def confirmation(drink):
    if drink == 'rum-and-coke':
        # GPIO.output(23, GPIO.HIGH)
        template_data = {
            'title': web_title,
            'drink': "rum and coke"
        }
        # TODO: put in a lock file to show that the device is currently in use

        # this is how to make a drink
        recipe = dict(drink_dict['rum-and-coke']['recipe'])
        make_drink(recipe)

        return render_template('confirmation.html', **template_data)

    if drink == 'rainforest':
        # GPIO.output(24, GPIO.HIGH)
        template_data = {
            'title': web_title,
            'drink': "rainforest"
        }
        return render_template('confirmation.html', **template_data)

    if drink == 'gin-and-tonic':
        # GPIO.output(25, GPIO.HIGH)
        template_data = {
            'title': web_title,
            'drink': "gin and tonic"
        }
        return render_template('confirmation.html', **template_data)


def activate_relay(relay):
    GPIO.output(relay, GPIO.LOW)
    print(f'relay {relay} has been activated')


def deactivate_relay(relay):
    GPIO.output(relay, GPIO.HIGH)
    print(f'relay {relay} has been deactivated')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
