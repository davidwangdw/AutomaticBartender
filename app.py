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
    2: 13
}

# create dictionary for what drinks are connected to which tubes
liquid_sources_dict = {
    'vodka': 0,  # 0 represents not available
    'rum': 1,
    'coke': 2
}
# recipe dict includes each kind of drink, and what ingredients are necessary, as well as their quantity
drink_dict = {
    "rum-and-coke": {
        "description": "good old classic",
        "recipe": {
            "rum": 1,
            "coke": 4
        }
    }
}

for pin in [6, 13]:
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
                [drink, drink_info['description'], 'Available']
            )
        else:
            drink_list_for_html.append(
                [drink, drink_info['description'], 'Missing Ingredients']
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
    while time_elapsed <= longest_time_needed:
        # close relays
        relays_to_activate = [ingredient for ingredient, time_left in recipe.items() if time_left > 0]
        relays_to_deactivate = [ingredient for ingredient, time_left in recipe.items() if time_left == 0]
        for relay in relays_to_deactivate:
            # TODO: add open GPIO code once debugging shows it works
            if relay not in relays_already_deactivated:
                relays_already_deactivated.add(relay)
        for relay in relays_to_activate:
            # TODO: add closing GPIO code once debugging shows it works
            recipe[relay] -= 1
        time.sleep(1)
        time_elapsed += 1
        print(f'{time_elapsed} elapsed')


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
