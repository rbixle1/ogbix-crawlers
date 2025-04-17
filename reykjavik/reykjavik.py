import boto3
from playwright.sync_api import sync_playwright
import datetime
import json
from random import randint
from time import sleep

s3_client = boto3.client('s3')
bucket_name = 'tracks.json'

def crawl_url(url, run_headless=True):
    print('lets go')
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=run_headless)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        context.clear_cookies()
        sleep(7)
        page.click('.cookie-consent__Button-sc-adz38x-5')
        all_songs = page.query_selector_all('.on-air-item__Row-sc-wsbncy-2')
 
        for quote in all_songs:
            broadcast = datetime.datetime.today().replace(minute=0, second=0, microsecond=0) 
            song = quote.query_selector('.on-air-item__Description-sc-wsbncy-5').inner_text()
            band = quote.query_selector('.on-air-item__Title-sc-wsbncy-4').inner_text()
            bucket_key = 'tracks/reykjavík/' + broadcast.strftime("%m-%d-%Y") + '/' + broadcast.strftime("%H:%M") + '/' + band + song + '.json'
            print({'band': band, 'song': song, 'broadcast' : broadcast})
            try: 
                s3_response = s3_client.put_object(
                    Bucket=bucket_name,
                    Key=bucket_key,
                    Body=json.dumps({'band': band, 'song': song, 'broadcast' : broadcast.strftime("%m/%d/%Y %H:%M")})
                )
                
            except s3_client.exceptions.NoSuchBucket as e:
                print('The S3 Bucket does not exist' + e)
        browser.close()

url = "https://x977.visir.is/"
crawl_url(url, True)