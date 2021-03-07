# prpd_usb

Read data of your NEDAP PowerRouter via USB. Current output modules:
json on stdout, mqtt and a prometheus exporter.

Tested with NEDAP PowerRouter `PR37Bi` Version `7.1.2`

## Installing

```
# install dependencies as root
apt-get install python3 python3-venv

git clone https://github.com/BenediktSeidl/prpd_usb.git
cd prpd_usb
python3 -mvenv v
source v/bin/activate
pip install .

# print data on stdout
prpd_usb -vvv stdout
```

## Deployment

*This is just an example how to make use of `prpd_usb` there are many other
ways to visualize the data or install the software*

The example assumes a debian installation, for example on a raspberry pi.

```
# don't forget the install step above!

apt-get install prometheus docker.io

# prometheus setup
cat >> /etc/prometheus/prometheus.yml << EOF
  - job_name: prpd_usb
    scrape_interval: 30s
    scrape_timeout: 20s
    static_configs:
      - targets: ['localhost:9091']
EOF
systemctl restart prometheus
# the target page of prometheus should now show prpd_usb target
# which is currently red, but should get green after the last step
# http://<address of rpi>:9090/targets

# grafana setup
systemctl enable docker
systemctl start docker
mkdir /home/pi/grafana
chown 472:root /home/pi/grafana
docker run \
    -p 3000:3000 \
    --restart always \
    -e GF_SECURITY_ADMIN_PASSWORD=password \
    -e GF_USERS_ALLOW_SIGN_UP=false \
    -e GF_ANALYTICS_REPORTING_ENABLED=false \
    -e GF_ANALYTICS_CHECK_FOR_UPDATES=false \
    -v /home/pi/grafana:/var/lib/grafana \
    -d \
    --name grafana \
    grafana/grafana
# surf to http://<address of rpi>:3000/
# login with user admin and the password above (you should change it)
# configuration -> data sources -> add data source
# choose prometheus; change url to http://<address of rpi>:9090/
# save & test

# prpd_usb setup
cat > /etc/systemd/system/prpd_usb.service << EOF
[Unit]
Description=prpd_usb
StartLimitIntervalSec=0 # always restart

[Service]
Restart=always
RestartSec=20
User=pi
ExecStart=/home/pi/prpd_usb/v/bin/prpd_usb prometheus --bind 127.0.0.1

[Install]
WantedBy=default.target
EOF

systemctl enable prpd_usb
systemctl start prpd_usb
```

See [doc/grafana_dashboard.json](doc/grafana_dashboard.json) for a simple
dashboard you can import into grafana.


## Updating

```
cd prpd_usb
source v/bin/activate
pip install .
# as root:
systemctl restart prpd_usb
```


## Development

The USB-Port on the NEDAP PowerRouter, is just a Serial Port in disguise and
uses some popular FTDI chip that is recognised by the linux kernel.
You can find some information about the protocol [here](doc/README.md)

### running faker

Provides sample data to test without an PowerRouter

```
# new terminal: link tty
socat PTY,link=/tmp/tty10 PTY,link=/tmp/tty11

# new terminal: create fake data
prpd_usb faker /tmp/tty10

# test prpd_usb
prpd_usb --device /tmp/tty11 stdout
```

## Disclaimer

Use at your own risk!
