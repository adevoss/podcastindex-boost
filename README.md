# podcastindex-boost
Send a boostagram to a podcasts using the Podcast Index (https://podcastindex.org)

To use you need a key. Please go to https://api.podcastindex.org/signup

Example on Raspiblitz v1.8:
sudo -u helipad python3 VALUE /path/to/boost.py 920666 90 1
sudo -u helipad python3 BOOST /path/to/boost.py 920666 90 1 'Sender name' 1000 'Boostmessage'

Options:
/path/to/boost.py VALUE|BOOST <podcastindex-id> <episode_nr> [<timestamp> <sender> <sats_total> <message>]

VALUE - Show valueblock of podcast episode
BOOST - Send boostagram

configuration.json:
- podcastindex: use your key and secret

- log: Log directory

- mode: TEST or BOOT
- timestamp: default spot in episode (in seconds)
- message: default text message to send
- sender: default name for sender (you)
- sats_total: default total amount of sats to send

- podcastlist: file containing your podcastlist
- sendboostagram: path to boost.sh


INSTALLATION on Raspiblitz v1.8:

Install extra package:
- sudo apt install python3-dateutil

Get files:
- cd /tmp
- sudo git clone https://github.com/adevoss/podcastindex-boost
- copy \*.sh, \*.py and \*.json to a directory of choice
- copy LICENCE and README.md to the same directory of choice
- sudo rm -rf /tmp/podcastindex-boost
- sudo chown -Rv helipad:helipad <directory of choice>
- sudo mkdir <log-directory> (see config.json)
- sudo chown -Rv helipad:helipad <log-directory>

Configuration:
- edit paths in configuration.py and config.json
- edit settings in config.json
- edit podcastlist.json
