How to get this set up on a fresh Raspberry Pi:

1. Install the OS using the official tool - make sure to configure it with WiFi and SSH

Install Python and Flask, clone repo
```
mkdir projects
cd projects
sudo apt-get install python3-pip -y
sudo pip install flask
git clone https://github.com/davidwangdw/AutomaticBartender.git
cd AutomaticBartender
sudo python3 app.py
```

This starts the application at whatever IP address the Pi is currently at. To get updates and run again:

```
git pull
sudo python3 app.py
```