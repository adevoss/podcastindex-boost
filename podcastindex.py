#!/usr/bin/env python3

import sys
import os
import json
import requests
import subprocess
import configuration

import PIfunctions
import Appfunctions
import configuration
import generalfunctions

def get_app_name(log_path):
    App_url = configuration.config["app"]["url"]
    url = App_url  + "appname"
    result = Appfunctions.request(url, log_path)
    if result != None and 'name' in result and type(result['name']) is str:
       result = result['name']
    else:
       result = 'NodeBoost'
    return result

def get_app_split(log_path):
    result = None
    take_split = configuration.config["app"]["insplit"]
    if bool(take_split):
       app_url = configuration.config["app"]["url"]
       url = app_url  + "appsplit"
       result = Appfunctions.request(url, log_path)
       if result == None:
          result = 1
       else:
          if 'split' in result and type(result['split']) is int:
             result = result['split']
    return result

def get_app_address(log_path):
    App_url = configuration.config["app"]["url"]
    url = App_url  + "appnodeaddress"
    result = Appfunctions.request(url, log_path)
    if result != None and 'address' in result and type(result['address']) is str:
       result = result['address']
    else:
       result = None
    return result

def get_app_customKey(log_path):
    App_url = configuration.config["app"]["url"]
    url = App_url  + "appcustomkey"
    result = Appfunctions.request(url, log_path)
    if result != None and 'customkey' in result and type(result['customkey']) is int:
       result = result['customkey']
    else:
       result = None
    return result

def get_app_customValue(log_path):
    App_url = configuration.config["app"]["url"]
    url = App_url  + "appcustomvalue"
    result = Appfunctions.request(url, log_path)
    if result != None and 'customvalue' in result and type(result['customvalue']) is int:
       result = result['customvalue']
    else:
       result = None
    return result

def send_boostagram_command(sendboostagramscript, boostagrammode, unlocked, title, episode, timestamp, podcast_id, feed_url, name, address, customKey, customValue, message, sender, sats):
    command = sendboostagramscript + ' ' + '\"' + str(boostagrammode) + '\"' + ' ' + str(unlocked) + ' ' + '\"' + title + '\"' + ' \"' + episode + '\"' + ' ' + str(timestamp) + ' ' + str(podcast_id) + ' ' + '\"' + feed_url + '\"' + ' ' + '\"' + str(name) + '\"' + ' ' + str(address) + ' ' + str(customKey) + ' ' + str(customValue) + ' ' + '\"' + message + '\"' + ' ' + '\"' + str(sender) + '\"' + ' ' + str(sats)
    return command

def podcastdata(feedId, log_path):
    PIurl = configuration.config["podcastindex"]["url"]
    url = PIurl  + "podcasts/byfeedid?id=" + str(feedId)
    feed_result = PIfunctions.request(url, log_path)
    return feed_result

def calculate_sats_after_fees(sats_total, valueblock):
    sats_after_fees = int(sats_total)
    if app_split != None:
       sats_after_fees -= int(int(sats_total) / 100 * int(app_split))
    for recipient in valueblock:
        if 'fee' in recipient and recipient['fee']:
           sats_after_fees -= int(int(sats_total) / 100 * int(recipient['split']))
    return sats_after_fees

def check_splits(valueblock):
    passed = False
    if valueblock !=None:
       split_total = 0
       for recipient in valueblock:
           if 'fee' not in recipient or not recipient['fee']:
              split_total += int(recipient['split'])
       if split_total <= 100:
          passed = True
    return passed

def check_valueblock(valueblock):
    passed = False
    if valueblock !=None:
       for recipient in valueblock:
           if 'type' in recipient and recipient['type'] == 'node':
              passed = True
    return passed

def nodesdata(data):
    value = None
    if data !=None:
        if 'value' in data and 'model' in data['value'] and 'destinations' in data['value']:
          if 'type' in data['value']['model'] and 'method' in data['value']['model']:
             if data['value']['model']['type'] == 'lightning':
                if data['value']['model']['method'] == 'keysend':
                   value = data['value']['destinations']
    return value

def podcast_value(feedId, log_path):
    value = None
    PIurl = configuration.config["podcastindex"]["url"]
    url = PIurl + "value/byfeedid?id=" + str(feedId) + "&pretty"
    result = PIfunctions.request(url, log_path)
    if result !=None:
        value = nodesdata(result)
    return value

def episodesdata(feedId, log_path):
    value = None
    PIurl = configuration.config["podcastindex"]["url"]
    url = PIurl + "episodes/byfeedid?id=" + str(feedId) + "&max=1000" + "&pretty"
    episodes_result = PIfunctions.request(url, log_path)
    return episodes_result

def episodedata(feedId, episode_nr, log_path):
    value = None
    match = False
    if int(episode_nr) > 0:
       episodes_result = episodesdata(feedId, log_path)
       for episode in episodes_result['items']:
           if not match:
              value = episode
              if episode['episode'] == str(episode_nr):
                  match = True
              else:
                 if str(episode_nr) in episode['title']:
                    match = True
                 else:
                    if '#' + str(episode_nr) in episode['description'] or ' ' + str(episode_nr) in episode['description']:
                       match = True
    return value

def episode_value(feedId, episode, log_path):
    value = None
    if episode != None:
       value = nodesdata(episode)
       if value == None:
          value = podcast_value(feedId, log_path)
    else:
       value = podcast_value(feedId, log_path)
    return value

def process_file(mode, data, episode_nr, podcast_to_process):
    for podcast_data in data['podcastlist']:

        if podcast_data["id"][:1] != '#':
           if podcast_to_process == "ALL" or str(podcast_to_process) == podcast_data["id"] or str(podcast_to_process) == podcast_data["feed"]:
              if mode == "VALUE" or (mode == "BOOST" and podcast_data["boostable"] == "1"):
                 pi_podcast = podcastdata(podcast_data['id'], log_path)
                 pi_episode = episodedata(podcast_data['id'], episode_nr, log_path)
                 valueblock = episode_value(podcast_data['id'], pi_episode, log_path)

                 episode_in_index = False
                 if pi_episode != None:
                    episode_in_index = True

                 message = 'Podcast: ' + pi_podcast["feed"]['title']
                 generalfunctions.log(log_path, message, False, False)
                 print(message)
                 if int(episode_nr) > 0:
                    message = 'Episode: ' + pi_episode['title']
                    generalfunctions.log(log_path, message, False, False)
                    print(message)

                 if mode == "BOOST":
                    message = 'Timestamp: ' + str(timestamp)
                    generalfunctions.log(log_path, message, False, False)
                    message = 'Sender: ' + sender
                    generalfunctions.log(log_path, message, False, False)
                    message = 'sats: ' + str(sats_total)
                    generalfunctions.log(log_path, message, False, False)


                 if int(episode_nr) == 0 or episode_in_index:
                    if valueblock != None:
                       if mode == "BOOST":
                          message = 'Boostagram: ' + boostagrammessage
                          generalfunctions.log(log_path, message, False, False)
                          print(message)

                       if mode == "BOOST" or mode == "VALUE":
                          if check_valueblock(valueblock) and check_splits(valueblock):
                             sats_after_fees = calculate_sats_after_fees(sats_total, valueblock)

                             if int(episode_nr) == 0:
                                episode_title = 'No specific episode'
                             else:
                                episode_title = pi_episode['title']

                             if app_split == None:
                                message = 'Fee for app can\'t be determined.'
                             else:
                                message = 'App takes a ' + str(app_split) + '% fee'
                             print(message)

                             if mode == "BOOST":
                                if app_split != None:
                                   sats_app = int(int(sats_total) / 100 * int(app_split))
                                   command = send_boostagram_command(sendboostagramscript, boostagrammode, unlocked, pi_podcast['feed']['title'], episode_title, timestamp, pi_podcast['feed']['id'], pi_podcast['feed']['url'], app_name, app_address, app_customKey, app_customValue, boostagrammessage, app_name, sats_app)
                                   boostagram_result=subprocess.run(command, shell=True).returncode
                                   message = 'Sent split to app developer. '
                                   if boostagram_result == 0:
                                      message += '(Successful)'
                                      generalfunctions.log(log_path, message, False, False)
                                   else:
                                      message += '(FAILED)'
                                      generalfunctions.log(log_path, message, True, False)
                                else:
                                   message = 'No API (Application fee). Server (application side) offline or no internet connection.'
                                   generalfunctions.log(log_path, message, True, False)

                             for recipient in valueblock:

                                 if mode == "BOOST":
                                    if os.path.exists(sendboostagramscript):
                                       message = 'Boosting ' + recipient['name']

                                       if 'fee' in recipient and recipient['fee']:
                                          sats_recipient = int(int(sats_total) / 100 * int(recipient['split']))
                                       else:
                                          sats_recipient = int(int(sats_after_fees) / 100 * int(recipient['split']))

                                       if sats_recipient == 0:
                                          message = message + '. Amount of sats is 0. No sats sent.'
                                          generalfunctions.log(log_path, message, True, False)
                                          print(message)
                                       else:
                                          message = message + ' ' + str(sats_recipient) + ' sats'
                                          if 'fee' in recipient and recipient['fee']:
                                             message = message + ' (fee)'
                                          message +=  '.'

                                          customKey = 0
                                          customValue = 0
                                          if 'customKey' in recipient and len(recipient['customKey']) > 0:
                                             if 'customValue' in recipient and len(recipient['customValue']) > 0:
                                                customKey = recipient['customKey']
                                                customValue = recipient['customValue']

                                          command = send_boostagram_command(sendboostagramscript, boostagrammode, unlocked, pi_podcast['feed']['title'], episode_title, timestamp, pi_podcast['feed']['id'], pi_podcast['feed']['url'], recipient['name'], recipient['address'], customKey, customValue, boostagrammessage, sender, sats_recipient)
                                          boostagram_result=subprocess.run(command, shell=True).returncode

                                          message += ' '
                                          if boostagram_result == 0:
                                             message += 'Successful'
                                          else:
                                             message += 'FAILED (lncli return code: ' + str(boostagram_result) + ')'

                                          generalfunctions.log(log_path, message, False, False)
                                          print(message)
                                    else:
                                       message = 'File \'' + sendboostagramscript + '\' does not exist'
                                       print(message)
                                       generalfunctions.log(log_path, message, True, False)

                                 if mode == "VALUE":
                                    message = 'Recipient: ' + recipient['name'] + ' Split: ' + str(recipient['split']) + '%'
                                    if 'fee' in recipient and recipient['fee']:
                                       message += ' (fee)'
                                    print(message)
                    else:
                       message = 'No valueblock in index'
                       generalfunctions.log(log_path, message, False, False)
                       print(message)
                 else:
                    if int(episode_nr) > 0:
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

    podcastlist_file = configuration.config["file"]["podcastlist"]

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
       if boostagrammessage == 'fromfile':
           boostagrammessage = generalfunctions.read_file(configuration.config["file"]["boostagramfile"])
       if os.path.exists(boostagrammessage):
           boostagrammessage = generalfunctions.read_file(boostagrammessage)
       else:
           if boostagrammessage[:1] == '/':
              boostagrammessage = configuration.config["settings"]["message"]
              
    if len(sys.argv) == 4:
       mode = sys.argv[1]
       podcast_to_process = sys.argv[2]
       episode_nr = sys.argv[3]

    if (len(sys.argv) == 4 or len(sys.argv) == 8) and (mode == "VALUE" or mode == "BOOST"):
       configuration.read() 
       log_path = configuration.config["directory"]["log"]

       now = generalfunctions.now()
       dateString = generalfunctions.format_dateYYYMMDDHHMMSS(now)

       generalfunctions.create_directory(log_path)
       log_path = os.path.join(log_path, dateString+'.log')

       app_name = get_app_name(log_path)
       print('Fetching app split...')
       app_split = get_app_split(log_path)
       app_address = get_app_address(log_path)
       app_customKey = get_app_customKey(log_path)
       app_customValue = get_app_customValue(log_path)

       if os.path.exists(podcastlist_file):
          data = generalfunctions.read_json(podcastlist_file, log_path)
          process_file(mode, data, episode_nr, podcast_to_process)
       else:
          message = 'Can\'t read podcastlist: ' + podcastlist_file
          print(message)
          generalfunctions.log(log_path, message, True, False)

    else:
        podcast_to_process = "--help"

    if str(podcast_to_process) == "-h" or podcast_to_process == "--help":
       print ('Usage: ' + sys.argv[0] + ' VALUE|BOOST <podcastindex-id> <episode_nr> [<timestamp> <sender> <sats_total> <message>]')

except Exception as e:
    message = e
    message = str(e)
    generalfunctions.log(log_path, message, True, False)
    print(message)
