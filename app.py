from flask import Flask, render_template, redirect
import datetime

app = Flask(__name__)

# http://mattrichardson.com/Raspberry-Pi-Flask/
# https://learn.adafruit.com/adafruit-keg-bot?view=all
# https://randomnerdtutorials.com/raspberry-pi-web-server-using-flask-to-control-gpios/
# https://hydrosysblog.wordpress.com/
# https://www.youtube.com/watch?v=3w4tOuRyBSc
# https://www.instructables.com/Raspberry-Pi-With-4-Relay-Module-for-Home-Automati/
# https://www.electronicshub.org/control-a-relay-using-raspberry-pi/
# https://robu.in/how-to-connect-relay-to-raspberry-pi-3/

@app.route("/")
def index():
    now = datetime.datetime.now()
    time_string = now.strftime("%Y-%m-%d %H:%M")
    template_data = {
        'title': 'Welcome to Apt 409!',
        'time': time_string
    }
    return render_template('main.html', **template_data)

@app.route("/confirmation/<drink>")
def confirmation(drink):
    if drink == 'rum-and-coke':
        template_data = {
            'title': 'Welcome to Apt 409!',
            'drink': "rum and coke"
        }
        return render_template('confirmation.html', **template_data)

@app.route("/rum-and-coke")
def rum_coke():
    print("you have ordered a rum and coke")
    return redirect('/confirmation/rum-and-coke')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

