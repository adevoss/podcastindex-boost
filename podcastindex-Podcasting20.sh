#!/bin/bash

MODE=$1
PODCASTINDEX="/home/helipad/podcastindex/podcastindex.sh"


FEEDID=920666

if [ $# == 1 -o $# == 2 -o $# == 6 ]; then

   if [ $# == 1 ]; then
      EPISODENR=0
   fi
   if [ $# == 2 -o $# == 6 ]; then
      EPISODENR=$2
   fi

   if [ "$MODE" == "VALUE" -o "$MODE" == "BOOST" ]; then
      if [ $# == 1 -o $# == 2 ]; then
         $PODCASTINDEX $MODE $FEEDID $EPISODENR
      else
         TIMESTAMP=$3
         SENDER=$4
         SATS=$5
         MESSAGE=$6
         $PODCASTINDEX $MODE $FEEDID $EPISODENR $TIMESTAMP $SENDER $SATS $MESSAGE
      fi
   else
      MODE="--help"
   fi
else
   MODE="--help"
fi 

if [ "$MODE" == "-h" -o "$MODE" == "--help" ]; then
   echo "Usage: $0 [ --help|-h ] or [ <mode VALUE|BOOST> [ [<episode nr>] [<timestamp in seconds> <sender name> <total amount of sats> <boostagram message>] ]"
fi
