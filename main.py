import tweepy
import json
from ShazamAPI import Shazam
from tweepy import OAuthHandler
import wget
import urllib.request
import traceback
from moviepy.editor import *

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse

tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

screen_name = "_subFN"

mentions = api.mentions_timeline(count=1)

replies = open(r'C:\Users\sub\Desktop\musica\files\data\replied-to.txt', 'r')

file = open(r'C:\Users\sub\Desktop\musica\files\data\replied-to.txt', 'r+')
b = file.readlines()
b = str(b)
b = b.replace("['", "").replace("']", "")

mention_id = 0
text = "@" + screen_name + " download"

def detectMusic():
    mp3_file_content_to_recognize = open(r'C:\Users\sub\Desktop\musica\files\audio\file.mp3', 'rb').read()


    shazam = Shazam(mp3_file_content_to_recognize)
    try:
        recognize = shazam.recognizeSong()
        result = next(recognize)

       
        title = result[1]['track']['title']
        artist = result[1]['track']['subtitle']

        replytomessage = "This song is: " + title + " by " + artist + "."
        for mention in mentions:
            api.update_status(status = replytomessage, in_reply_to_status_id = mention.id, auto_populate_reply_metadata=True)
        
    except:
        for mention in mentions:
            api.update_status(status = "The song could not be recognized.", in_reply_to_status_id = mention.id, auto_populate_reply_metadata=True)
        traceback.print_exc()


def detectMention():
    for mention in mentions:
        if (str(b) != mention.in_reply_to_status_id_str):
            if (text.lower() in mention.text.lower()):
                if mention.in_reply_to_status_id is not None:
                    with open(r'C:\Users\sub\Desktop\musica\files\data\replied-to.txt', 'r+') as h:
                        for line in b:
                            if line.strip("\n") != "never will be this so clear":
                              h.write(line)
                    h = open(r'C:\Users\sub\Desktop\musica\files\data\replied-to.txt', 'r+')
                    h.write(mention.in_reply_to_status_id_str)
                    mention_id = mention.in_reply_to_status_id
                    downloadVideo()
                else:
                    with open(r'C:\Users\sub\Desktop\musica\files\data\replied-to.txt', 'r+') as h:
                        for line in b:
                            if line.strip("\n") != "never will be this so clear":
                                h.write(line)
                    h = open(r'C:\Users\sub\Desktop\musica\files\data\replied-to.txt', 'r+')
                    h.write(api.in_reply_to_status_id_str)

            else:
                return



def downloadVideo():
    for mention in mentions:

        ide = mention.in_reply_to_status_id
        tweet = api.get_status(ide)
        media = tweet.extended_entities['media'][0]['video_info']['variants'][1]['url']


    try:
        urllib.request.urlretrieve(media, r'C:\Users\sub\Desktop\musica\files\video\file.mp4')
        convertToAudio()

    except:
        traceback.print_exc()

def convertToAudio():

    try:
        video = VideoFileClip(os.path.join("path","to", r'C:\Users\sub\Desktop\musica\files\video\file.mp4'))
        video.audio.write_audiofile(os.path.join("path","to",r'C:\Users\sub\Desktop\musica\files\audio\file.mp3'))
        detectMusic()
    except:
        traceback.print_exc()



if __name__ == "__main__":
    detectMention()
