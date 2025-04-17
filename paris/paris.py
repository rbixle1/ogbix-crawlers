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
        browser = p.firefox.launch(headless=run_headless, slow_mo=5000)
        page = browser.new_page()
        page.goto(url)
        all_quotes = page.query_selector_all('.col-md-1')
 
        for quote in all_quotes:
             broadcast = 'blah'
        #     broadcast =  
             
             band = ''
             song = ''
             if quote.query_selector('.album'):
                offset = quote.query_selector('.text').inner_text()
                offsets = re.split('h', offset)
                #print(offsets)
                broadcast = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(hours=int(offsets[0]), minutes=int(offsets[1]))
                
                song = quote.query_selector('.album').inner_text()
                band = quote.query_selector('.artist').inner_text()
                bucket_key = 'tracks/paris/' + broadcast.strftime("%m-%d-%Y") + '/' + broadcast.strftime("%H:%M") + "/" + band + song + '.json'
                print({'band': band, 'song': song, 'broadcast' : broadcast.strftime("%m/%d/%Y %H:%M")})
                try: 
                    s3_response = s3_client.put_object(
                        Bucket=bucket_name,
                        Key=bucket_key,
                        Body=json.dumps({'band': band, 'song': song, 'broadcast' : broadcast.strftime("%m/%d/%Y %H:%M")})
                    )
                    
                except s3_client.exceptions.NoSuchBucket as e:
                    print('The S3 Bucket does not exist' + e)
 
        browser.close()
 

#https://www.ouifm.fr/retrouver-un-titre

url = "https://www.ouifm.fr/"
crawl_url(url, True)