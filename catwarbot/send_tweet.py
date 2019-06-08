import tweepy
from cairosvg import svg2png
import os

def run(text, path_img):
    consumer_key = os.environ.get('COSTUMER_KEY')
    consumer_secret = os.environ.get('COSTUMER_SECRET')
    access_token = os.environ.get('ACCES_TOKEN')
    access_token_secret = os.environ.get('ACCES_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret) 
    api = tweepy.API(auth)

    image = to_png(path_img)
    #api.update_with_media(image, status=text)

def to_png(path_img):
    with open(path_img, 'r') as f:
        data = f.read()
    svg2png(bytestring=data,write_to='output.png')
    return 'output.png'


    