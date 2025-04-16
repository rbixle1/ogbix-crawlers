import boto3
from playwright.sync_api import sync_playwright
import datetime
import json

s3_client = boto3.client('s3')
bucket_name = 'tracks.json'
url = "http://www.radiox.co.uk/dynamic/now-playing-card/"
run_headless = True

def handler(event, context):
    print('lets go')
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=run_headless)
        page = browser.new_page()
        page.goto(url)
        all_quotes = page.query_selector_all('.recently_played_track')
 
        for quote in all_quotes:
            offset = quote.query_selector('.last_played').inner_text()
            broadcast =  (datetime.datetime.now() - datetime.timedelta(minutes=int(offset.split()[0]))).strftime("%Y/%m/%d %H:%M")
            song = quote.query_selector('.track').inner_text()
            band = quote.query_selector('.artist').inner_text()
            bucket_key = 'tracks/london/' + broadcast.replace('/', '-').replace(', ','/') + '/' + band + song + '.json'
            print({'band': band, 'song': song, 'broadcast' : broadcast})
            try: 
                s3_response = s3_client.put_object(
                    Bucket=bucket_name,
                    Key=bucket_key,
                    Body=json.dumps({'band': band, 'song': song, 'broadcast' : broadcast})
                )
                
            except s3_client.exceptions.NoSuchBucket as e:
                print('The S3 Bucket does not exist' + e)
 
        browser.close()
def main():
    # Your main program logic here
    handler(None, None)

if __name__ == "__main__":
    main()

