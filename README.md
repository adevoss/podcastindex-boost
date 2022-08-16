# podcastindex-aggregator
Send a boostagram to a podcasts using the Podcast Index (https://podcastindex.org)

To use you need a key. Please go to https://api.podcastindex.org/signup

Example:
/path/to/boost.py 920666 90 1 1000 'Boostmessage'

Options:
/path/to/boost.py VALUE|BOOST <podcastindex-id> <episode nr> [<timestamp> <amount> <message>]

VALUE - Show valueblock of podcast episode
BOOST - Send boostagram

configuration.json:
- podcastindex: use your key and secret

- log: Subdirectory of 'data' where log files are stored
- amount: default amount of sats to send
