from flask import Flask, render_template, redirect, flash
import datetime
import RPi.GPIO as GPIO
import uuid

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())
GPIO.setmode(GPIO.BCM)

# create dictionary for what drinks are connected to which tubes
liquid_sources_dict = {
    'rum': 1,
    'coke': 2
}

for pin in [6, 13]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

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
    GPIO.output(6, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    time_string = now.strftime("%Y-%m-%d %H:%M")
    template_data = {
        'title': web_title,
        'time': time_string
    }
    return render_template('main.html', **template_data)


@app.route("/confirmation/<drink>")
def confirmation(drink):
    if drink == 'rum-and-coke':
        # GPIO.output(23, GPIO.HIGH)
        template_data = {
            'title': web_title,
            'drink': "rum and coke"
        }
        # TODO: put in a lock file to show that the device is currently in use
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


@app.route("/relay-1/start")
def relay_1_start():
    GPIO.output(6, GPIO.HIGH)
    flash("relay 1 has started")
    return redirect('/')


@app.route("/relay-1/stop")
def relay_1_stop():
    GPIO.output(6, GPIO.LOW)
    flash("relay 1 has stopped")
    return redirect('/')


@app.route("/relay-2/start")
def relay_2_start():
    GPIO.output(13, GPIO.HIGH)
    flash("relay 2 has started")
    return redirect('/')


@app.route("/relay-2/stop")
def relay_2_stop():
    GPIO.output(13, GPIO.LOW)
    flash("relay 2 has stopped")
    return redirect('/')


@app.route("/relay-1-2/start")
def relay_1_2_start():
    GPIO.output(6, GPIO.HIGH)
    GPIO.output(13, GPIO.HIGH)
    flash("relay 1 and 2 has started")
    return redirect('/')


@app.route("/relay-1-2/stop")
def relay_1_2_stop():
    GPIO.output(6, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    flash("relay 1 and 2 has stopped")
    return redirect('/')


@app.route("/rum-and-coke")
def rum_coke():
    print("you have ordered a rum and coke")
    return redirect('/confirmation/rum-and-coke')


@app.route("/rainforest")
def rainforest():
    print("you have ordered a rainforest")
    return redirect('/confirmation/rainforest')


@app.route("/gin-and-tonic")
def gin_and_tonic():
    print("you have ordered a gin and tonic")
    return redirect('/confirmation/gin-and-tonic')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
