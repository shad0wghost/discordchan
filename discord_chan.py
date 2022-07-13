import discord_webhook
from discord_webhook import DiscordWebhook
import requests
import json 
import re
import time as t
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--webhook", help="discord webhook", required=True)
parser.add_argument("--user", help="Username to post as", required=True)
parser.add_argument("--time", help="Time between scans Defualt: 30mins", default=30, type=float)
args = parser.parse_args()

webhook = DiscordWebhook(url=str(args.webhook), username=str(args.user))
postwaittime = 10
refreshtime = args.time * 60


webhook = DiscordWebhook(url=str(args.webhook), content='Monitoring for dank Memes...')
response = webhook.execute()

while True:
    from pathlib import Path
    fle = Path('funnydb.txt')
    fle.touch(exist_ok=True)
    f = open(fle)

    gifcat_url = "https://boards.4chan.org:443/gif/catalog"
    gifcat_headers = {"Connection": "close", "Cache-Control": "max-age=0", "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "DNT": "1", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "sec-gpc": "1", "If-Modified-Since": "Tue, 12 Jul 2022 18:54:02 GMT"}
    gifcat_request = requests.get(gifcat_url, headers=gifcat_headers)
    #print (gifcat_request.text)

    gifcat_text = gifcat_request.text
    subfind = gifcat_text[gifcat_text.find('var catalog'):]

    #find where the stuff is 
    sub_str = "var style_group = "
    
    # slicing off after length computation
    res = subfind[:subfind.index(sub_str) + len(sub_str)]
    
    #make list of threads using json
    json_maybe = str(res)[14:-19]

    #import the json
    realjson = json.loads(json_maybe)

    #print(type(realjson))
    #print (realjson['threads']["23129985"].keys())

    #print(json.dumps(realjson, indent=2, sort_keys=True))

    #print (realjson['threads'])
    #print (realjson['threads']['23133641']['sub'])
    #for key, value in realjson['threads'].items():
    #    print(key, ' : ', value)

    #make list of threads using json
    current_threads_list = []
    for element in realjson['threads']:
        current_threads_list.append(element + ":" + realjson['threads'][element]['sub'])
        current_threads_list.append(element + ":" + realjson['threads'][element]['teaser'])

    #look for ylyl in list and retun as list
    ylyl_threads = []
    for i in current_threads_list:
        if re.search(r'\bylyl\b', i, re.I):
            ylyl_threads.append(current_threads_list.index(i))

    #get all current ylyl thrads
    ylyl_threads_codes = []
    for i in ylyl_threads: 
        ylyl_threads_codes.append(current_threads_list[i].split(':')[0])

    #print (ylyl_threads_codes)

    funny_links = []
    for ylyl_id in ylyl_threads_codes:
        #make request
        ylyl_id_url = "https://boards.4chan.org:443/gif/thread/" + ylyl_id
        ylyl_id_headers = {"Connection": "close", "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1", "DNT": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://boards.4chan.org/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "sec-gpc": "1", "If-Modified-Since": "Tue, 12 Jul 2022 19:15:45 GMT"}
        ylyl_id_reaponce = requests.get(ylyl_id_url, headers=ylyl_id_headers)
        #sort and find cdn links
        ylyl_id_reaponce_split = ylyl_id_reaponce.text.split('"')
        #print (ylyl_id_reaponce_split)
        for i in ylyl_id_reaponce_split:
            if re.search(r'\bi\.4cdn\.org\b', i, re.I):
                funny_link = "https:" + i
                if not '.jpg' in funny_link:
                    funny_links.append(funny_link)
                else:
                    pass 
    #get dedupe db file befor u say anything i dont care that im doing it this way
    verified_funny_links = []
    for funnies in funny_links:
        with open('funnydb.txt') as funnyfile:
            if not funnies in funnyfile.read():
                verified_funny_links.append(funnies)
            else: 
                pass
    for thegoodstuff in verified_funny_links:
        file_object = open('funnydb.txt', 'a')
        # Append 'hello' at the end of file
        file_object.write(thegoodstuff + '\n')
        # Close the file
        file_object.close()


    path = 'memes'
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
    # Create a new directory because it does not exist 
        os.makedirs(path)
    #delete all old memes
    cmd = 'rm memes/*'
    #do
    os.system(cmd)


    for dankmeme in verified_funny_links: 
        # Define the remote file to retrieve
        remote_url = dankmeme
        print ("Downloading: " + remote_url)
        # Define the local filename to save data
        local_file = 'memes/' + dankmeme.split("/")[4]
        # Make http request for remote file data
        data = requests.get(remote_url)
        # Save file data to local copy
        with open(local_file, 'wb')as file:
            file.write(data.content)
            
    #print(verified_funny_links)

    ls_contents = list(Path('memes').iterdir())
    for filename in ls_contents:
        print ("Converting :" + str(filename))
        #convert webms
        cmd = 'ffmpeg -i ' + str(filename) + ' -crf 30 ' + str(filename) + '.mp4 -y'
        # Using os.system() method
        os.system(cmd)

    #delete all old webm's 
    cmd = 'rm memes/*.webm'
    #do
    os.system(cmd)

    #get updated list of files 
    ls_contents_convert = list(Path('memes').iterdir())
    for filename_convert in ls_contents_convert:
        print ("uploading: " + str(filename_convert))
        with open(str(filename_convert), "rb") as f:
            webhook.add_file(file=f.read(), filename=str(filename_convert))
            response = webhook.execute()
            #reset the webhook
            webhook = DiscordWebhook(url=str(args.webhook), username=str(args.user))


        print ("waiting...")
        t.sleep(postwaittime)

        #convert webms
    #delete all old memes
    cmd = 'rm memes/*'
    #do
    os.system(cmd)
    print ("sleeping for : " + str (refreshtime))
    t.sleep(refreshtime)
