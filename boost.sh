#!/bin/bash

# Using command by Dave Jones of podcastindex
# https://github.com/Podcastindex-org/helipad/blob/main/umbrel/testing.txt

# Example
# boost.sh "Podcast title" "Episode title" 120 "http://test.com/rss.xml" 032f4ffbbafffbe51ae8ac21b8508 "John Doe" "Boost!" 25000

LNCLI="/usr/local/bin/lncli"

if [ $# == 8 ]; then

PODCASTTITLE=$1
EPISODETITLE=$2
TIMESTAMP=$3
FEEDURL=$4
NODEID=$5
SENDER=$6
MESSAGE=$7
SATS=$8

TIME=$(date +%H:%M)
MSATS=$((SATS*1000))

$LNCLI sendpayment --keysend --dest $NODEID --amt $SATS --data 7629169=$(echo -n '{"podcast": "$PODCASTTITLE", "url": "$FEEDURL", "episode": "$EPISODETITLE", "ts": $TIMESTAMP, "time": "$TIME", "value_msat": $MSATS, "value_msat_total": $MSATS, "action": "boost", "sender_name": "$SENDER", "app_name": "lncli", "message": "$MESSAGE", "feedID": $FEEDID}' | xxd -pu -c 10000)

else
   echo "Usage: $0 <podcast title> <episode title> <timestamp in seconds> <feed url> <node id> <sender name> <message> <amount in sats>"
fi
