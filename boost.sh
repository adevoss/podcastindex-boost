#!/bin/bash

# Using command by Dave Jones of podcastindex
# https://github.com/Podcastindex-org/helipad/blob/main/umbrel/testing.txt

# Example
# boost.sh "Podcast title" "Episode title" 120 "http://test.com/rss.xml" 032f4ffbbafffbe51ae8ac21b8508 "John Doe" "Boost!" 25000

LNCLI="/usr/local/bin/lncli"
APP_NAME="lncli"
SENDER="Arno"

if [ $# == 10 ]; then

PODCASTTITLE=$1
EPISODETITLE=$2
TIMESTAMP=$3
FEEDID=$4
FEEDGUID=$5
FEEDURL=$6
RECIPIENT=$7
NODEID=$8
MESSAGE=$9
SATS=${10}

TIME=$(date +%H:%M)
MSATS=$((SATS*1000))

$LNCLI unlock

DATA="{"
DATA="$DATA\"action\": \"boost\", "

DATA="$DATA\"app_name\": \"$APP_NAME\", \"sender_name\": \"$SENDER\", "

DATA="$DATA\"feedID\": $FEEDID, \"url\": \"$FEEDURL\", "
DATA="$DATA\"podcast\": \"$PODCASTTITLE\", \"episode\": \"$EPISODETITLE\", "
DATA="$DATA\"name\": \"$RECIPIENT\", "

DATA="$DATA\"ts\": $TIMESTAMP, "
DATA="$DATA\"value_msat\": $MSATS, \"value_msat_total\": $MSATS, "

DATA="$DATA\"message\": \"$MESSAGE\""
DATA="$DATA}"

#RECORD=`echo -n $DATA | xxd -pu -c 10000`
RECORD=`echo $DATA |  od -A n -t x1 | sed -z 's/[ \n]*//g'`

#echo "Testing..."
#echo $NODEID
#echo
#echo $DATA
#echo
#echo $RECORD
$LNCLI sendpayment --dest=$NODEID --amt=$SATS --keysend --data 7629169=$RECORD

else
   echo "Usage: $0 <podcast title> <episode title> <timestamp in seconds> <feed url> <node id> <sender name> <message> <amount in sats>"
fi
