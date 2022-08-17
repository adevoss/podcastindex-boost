#!/usr/bin/env python3

import sys
import os
import json
import requests
import subprocess
import configuration

import PIfunctions
import configuration
import generalfunctions

def podcastdata(feedId, log_path):
    PIurl = configuration.config["podcastindex"]["url"]
    url = PIurl  + "podcasts/byfeedid?id=" + str(feedId)
    #generalfunctions.log(log_path, url, False, True)
    feed_result = PIfunctions.request(url, log_path)
    return feed_result

def podcast_value(feedId, log_path):
    value = None
    PIurl = configuration.config["podcastindex"]["url"]
    url = PIurl + "value/byfeedid?id=" + str(feedId) + "&pretty"
    result = PIfunctions.request(url, log_path)
    if result !=None:
       value = result['value']['destinations']
    return value

def episodesdata(feedId, log_path):
    value = None
    PIurl = configuration.config["podcastindex"]["url"]
    url = PIurl + "episodes/byfeedid?id=" + str(feedId) + "&max=1000" + "&pretty"
    episodes_result = PIfunctions.request(url, log_path)
    return episodes_result

def episodedata(feedId, episode_nr, log_path):
    value = None
    episodes_result = episodesdata(feedId, log_path)
    for episode in episodes_result['items']:
        if episode['episode'] == str(episode_nr) or str(episode_nr) in episode['title']:
           value = episode
    return value

def episode_value(feedId, episode, log_path):
    value = None
    if episode == None:
       value = podcast_value(feedId, log_path)
    else:
       value = episode['value']['destinations']
       if value == None:
          value = podcast_value(feedId, log_path)
    return value

def process_file(mode, data, episodes_nr, podcast_to_process):
    for podcast_data in data['podcastlist']:

        if podcast_data["id"][:1] != '#':
           if podcast_to_process == "ALL" or str(podcast_to_process) == podcast_data["id"] or str(podcast_to_process) == podcast_data["feed"]:
              if mode == "VALUE" or (mode == "BOOST" and podcast_data["boostable"] == "1"):
                 pi_podcast = podcastdata(podcast_data['id'], log_path)
                 pi_episode = episodedata(podcast_data['id'], episodes_nr, log_path)
                 valueblock = episode_value(podcast_data['id'], pi_episode, log_path)

                 episode_in_index = False
                 if pi_episode != None:
                    episode_in_index = True

                 if episode_in_index:
                    if valueblock != None:
                       logged_boostagrammessage = 0
                       print('Podcast: ' + pi_podcast["feed"]['title'])
                       print('Episode: ' + pi_episode['title'])

                       if mode == "BOOST":
                           print('Boostagram: ' + boostagrammessage)
                       if mode == "BOOST" or mode == "VALUE":
                           for recipient in valueblock:
                               if recipient['type'] == 'node':
                                  if logged_boostagrammessage == 0:
                                     logged_boostagrammessage = 1
                                     if mode == "BOOST":
                                        generalfunctions.log(log_path, 'Podcast: ' + pi_podcast["feed"]['title'], False, False)
                                        generalfunctions.log(log_path, 'Episode: ' + pi_episode['title'], False, False)
                                        generalfunctions.log(log_path, 'Timestamp: ' + str(timestamp), False, False)
                                        generalfunctions.log(log_path, 'Sender: ' + sender, False, False)
                                        generalfunctions.log(log_path, 'sats: ' + str(sats_total), False, False)
                                        generalfunctions.log(log_path, 'Boostagram: ' + boostagrammessage, False, False)

                                  if mode == "BOOST":
                                     message = 'Boosted ' + recipient['name']
                                     sats_recipient = int(int(sats_total) / 100 * int(recipient['split']))
                                     if sats_recipient == 0:
                                        message = message + '. Amount of sats is 0. No sats sent.'
                                     else:
                                        message = message + ' ' + str(sats_recipient) + ' sats.'

                                     command = sendboostagramscript + ' ' + '\"' + str(boostagrammode) + '\"' + ' ' + str(unlocked) + ' ' + '\"' + pi_podcast['feed']['title'] + '\"' + ' ' + '\"' + pi_episode['title'] + '\"' + ' ' + timestamp + ' ' + str(podcast_data["id"]) + ' ' + '\"' + podcast_data["feed"] + '\"' + ' ' + '\"' + recipient['name'] + '\"' + ' ' + recipient['address'] + ' ' + '\"' + boostagrammessage + '\"' + ' ' + '\"' + sender + '\"' + ' ' + str(sats_recipient)
                                     subprocess.call(command, shell=True)
                                     print(message)
                                     generalfunctions.log(log_path, message, False, False)

                                  if mode == "VALUE":
                                     print('Recipient: ' + recipient['name'] + ' Split: ' + str(recipient['split']) + '%')
                    else:
                       message = 'Podcast: ' + pi_podcast["feed"]['title']
                       generalfunctions.log(log_path, message, True, False)
                       print(message)
                       message = 'Episode: ' + pi_episode['title']
                       generalfunctions.log(log_path, message, True, False)
                       print(message)
                       message = 'No value block in index'
                       generalfunctions.log(log_path, message, True, False)
                       print(message)
                 else:
                    message = 'Podcast: ' + pi_podcast["feed"]['title']
                    generalfunctions.log(log_path, message, True, False)
                    print(message)
                    message = 'Episode ' + str(episode_nr) + ' not in index'
                    generalfunctions.log(log_path, message, True, False)
                    print(message)
              else:
                 if mode == "BOOST":
                    message = 'Podcast \'' + podcast_data["title"] + '\'' + 'is set in your configuration to be not boostable'
                    print(message)
                    generalfunctions.log(log_path, message, False, False)
        else:
           if podcast_to_process == "ALL":
              message = 'Skipping podcast \'' + podcast_data["title"] + '\''
              print(message)
              generalfunctions.log(log_path, message, False, False)


try:
    podcast_to_process = "--help"
    unlocked = 1

    configuration.read()
    sendboostagramscript = configuration.config["file"]["sendboostagram"]
    boostagrammode = configuration.config["settings"]["mode"]
    timestamp = configuration.config["settings"]["timestamp"]
    boostagrammessage = configuration.config["settings"]["message"]
    sender = configuration.config["settings"]["sender"]
    sats_total = configuration.config["settings"]["sats_total"]

    if len(sys.argv) == 8:
       mode = sys.argv[1]
       podcast_to_process = sys.argv[2]
       episode_nr = sys.argv[3]
       timestamp = sys.argv[4]
       sender = sys.argv[5]
       sats_total = sys.argv[6]
       boostagrammessage = sys.argv[7]
    if len(sys.argv) == 4:
       mode = sys.argv[1]
       podcast_to_process = sys.argv[2]
       episode_nr = sys.argv[3]

    if (len(sys.argv) == 4 or len(sys.argv) == 8) and (mode == "VALUE" or mode == "BOOST"):
       configuration.read() 
       log_path = configuration.config["directory"]["log"]
       podcastlist_file = configuration.config["file"]["podcastlist"]

       now = generalfunctions.now()
       dateString = generalfunctions.format_dateYYYMMDDHHMMSS(now)

       generalfunctions.create_directory(log_path)
       log_path = os.path.join(log_path, dateString+'.log')
       data = generalfunctions.read_json(podcastlist_file, log_path)
       process_file(mode, data, episode_nr, podcast_to_process)
    else:
        podcast_to_process = "--help"

    if str(podcast_to_process) == "-h" or podcast_to_process == "--help":
       print ('Usage: ' + sys.argv[0] + ' VALUE|BOOST <podcastindex-id> <episode_nr> [<timestamp> <sender> <sats_total> <message>]')

except Exception as e:
    message = e
    message = 'Function: ' + function.__name__ + ': ' + str(e)
    generalfunctions.log(log_path, message, True, False)
    print(message)
