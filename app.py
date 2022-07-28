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

web_title = "Welcome to 409!"


@app.route("/")
def index():
    now = datetime.datetime.now()
    time_string = now.strftime("%Y-%m-%d %H:%M")
    template_data = {
        'title': web_title,
        'time': time_string
    }
    return render_template('main.html', **template_data)


@app.route("/confirmation/<drink>")
def confirmation(drink):
    if drink == 'rum-and-coke':
        template_data = {
            'title': web_title,
            'drink': "rum and coke"
        }
        # TODO: put in a lock file to show that the device is currently in use
        return render_template('confirmation.html', **template_data)

    if drink == 'rainforest':
        template_data = {
            'title': web_title,
            'drink': "rainforest"
        }
        return render_template('confirmation.html', **template_data)

    if drink == 'gin-and-tonic':
        template_data = {
            'title': web_title,
            'drink': "gin and tonic"
        }
        return render_template('confirmation.html', **template_data)


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
