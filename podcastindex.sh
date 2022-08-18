#!/bin/bash

PODCASTINDEX="/home/helipad/boost/podcastindex.py"

MODE=$1
FEEDID=$2

if [ $# == 1 -o $# == 2 -o $# == 3 -o $# == 7 ]; then

   if [ $# == 1 ]; then
      FEEDID="--help"
   fi
   if [ $# == 2 ]; then
      EPISODENR=0
   fi
   if [ $# == 3 -o $# == 7 ]; then
      EPISODENR=$3
   fi

   if [ "$MODE" == "VALUE" -o "$MODE" == "BOOST" ]; then
      if [ $# == 2 -o $# == 3 ]; then
         python3 $PODCASTINDEX $MODE $FEEDID $EPISODENR
      else
         TIMESTAMP=$4
         SENDER=$5
         SATS=$6
         MESSAGE=$7
         python3 $PODCASTINDEX $MODE $FEEDID $EPISODENR $TIMESTAMP $SENDER $SATS $MESSAGE
      fi
   fi

else
   MODE="--help"
fi 

if [ "$MODE" == "-h" -o "$MODE" == "--help" ]; then
   echo "Usage: $0 [ --help|-h ] or [ <feedid> <mode VALUE|BOOST> [ [<episode nr>] <timestamp in seconds> <sender name> <total amount of sats> <boostagram message>] ]"
fi
