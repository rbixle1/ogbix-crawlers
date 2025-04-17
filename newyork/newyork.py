import boto3
from playwright.sync_api import sync_playwright
import datetime
import json
import time
import re
from datetime import timedelta

s3_client = boto3.client('s3')
bucket_name = 'tracks.json'

def crawl_url(url, run_headless=True):
    print('lets go')
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=run_headless)
        page = browser.new_page()
        page.goto(url)
        songs =  page.locator("table tr")
        for i in range(1, songs.count()):
            row = songs.nth(i)
            day_time = re.split(',', row.locator('.views-field-created').inner_text())
            day = re.split('/', day_time[0])
            time = re.split(':', day_time[1])

            broadcast = datetime.datetime.today().replace(day=int(day[1]), month=int(day[0]), hour=int(time[0]), minute=int(time[1][:2]), second=0, microsecond=0)  
            song = row.locator('.views-field-title').inner_text()
            band = row.locator('.views-field-field-artist').inner_text()
            print({'band': band, 'song': song, 'broadcast' : broadcast.strftime("%m/%d/%Y %H:%M")})
            bucket_key = 'tracks/newyork/' + broadcast.strftime("%m-%d-%Y") + '/' + broadcast.strftime("%H:%M") + "/" + band + song + '.json'
            try: 
                s3_response = s3_client.put_object(
                    Bucket=bucket_name,
                    Key=bucket_key,
                    Body=json.dumps({'band': band, 'song': song, 'broadcast' : broadcast.strftime("%m/%d/%Y %H:%M")})
                )
                
            except s3_client.exceptions.NoSuchBucket as e:
                print('The S3 Bucket does not exist' + e)
 
        browser.close()
url = 'https://wfuv.org/playlist' 
crawl_url(url, True)