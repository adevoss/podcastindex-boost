# podcastindex-boost
Send a boostagram to a podcasts using the Podcast Index (https://podcastindex.org)

To use you need a key. Please go to https://api.podcastindex.org/signup

Example:
/path/to/boost.py 920666 90 1 1000 'Boostmessage'

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
