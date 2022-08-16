#!/bin/bash

# Using command by Dave Jones of podcastindex
# https://github.com/Podcastindex-org/helipad/blob/main/umbrel/testing.txt

# Example
# boost.sh "Podcast title" "Episode title" 120 "http://test.com/rss.xml" 032f4ffbbafffbe51ae8ac21b8508 "John Doe" "Boost!" 25000

LNCLI="/usr/local/bin/lncli"
APP_NAME="lncli"

if [ $# == 12 ]; then

MODE=$1
UNLOCKED=$2
PODCASTTITLE=$3
EPISODETITLE=$4
TIMESTAMP=$5
FEEDID=$6
FEEDURL=$7
RECIPIENT=$8
NODEID=$9
MESSAGE=${10}
SENDER=${11}
SATS=${12}

TIME=$(date +%H:%M)
MSATS=$((SATS*1000))

# If automatic unlock is not set on node then you can only send boosts manually by using boost.sh
if [ $MODE == "SEND" -a $UNLOCKED == 0 ]; then
   $LNCLI unlock
fi

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

if [ $MODE == "TEST" ]; then
   echo $MODE 
   echo
   echo $NODEID
   echo $PODCASTTITLE
   echo $EPISODETITLE
   echo $TIMESTAMP
   echo $FEEDID
   echo $FEEDURL
   echo $RECIPIENT
   echo $NODEID
   echo $MESSAGE
   echo $SENDER
   echo $SATS
   echo
   echo $DATA
   echo
   echo $RECORD
fi
if [ $MODE == "SEND" ]; then
   if [ -f $LNCLI ]; then
      $LNCLI sendpayment --dest=$NODEID --amt=$SATS --keysend --data 7629169=$RECORD
   else
      echo "$LNCLI does not exist and/or is not executable."
   fi
fi

else
   echo "Usage: $0 <mode [TEST|SEND]> <podcast title> <episode title> <timestamp in seconds> <feed id> <feed url> <recipient> <node id> <message> <sender name> <amount in sats>"
fi # number of arguments
