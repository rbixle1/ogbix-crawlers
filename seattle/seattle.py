import urllib.request
from time import gmtime, strftime
from datetime import date
import json
import boto3


s3_client = boto3.client('s3')
bucket_name = 'tracks.json'

time_str = strftime('%H:%M', gmtime())
date_str = date.today().strftime('%m/%d/%y')

print ("PROCESSING DAY: " + date_str + '|' + time_str)


#url = PROPERTIES['SEATTLE_URL'] + '=' + str(LIMIT) + '&offset=0'
url = 'https://legacy-api.kexp.org/play/?limit=500&offset=0'



user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'

headers = {'User-Agent': user_agent}

def handler(event, context):
  req = urllib.request.Request(url, headers=headers)
  with urllib.request.urlopen(req) as response:
    data = json.load(response)

  for subdata in data['results']:
    if subdata['artist'] and subdata['airdate'] and subdata['release']:
      try: 
        air_date = (subdata['airdate'][0:10]).replace('-', '/')
        bucket_date = (air_date[5:] + '-' + air_date[0:4]).replace('/', '-')
        print('AIR_DATE: ' + air_date + ' BUCKET Date:' + bucket_date )
        time = subdata['airdate'][11:16]
        artist = subdata['artist']['name'][:64]
        song = subdata['track']['name'][:64]
        album = subdata['release']['name'][:64]
        bucket_key = 'tracks/seattle/' + bucket_date + '/'  + time + '/' + artist + song + '.json'
        print({'band': artist, 'song': song, 'broadcast' : air_date + ' ' + time})
        s3_response = s3_client.put_object(
            Bucket=bucket_name,
            Key=bucket_key,
            Body=json.dumps({'band': artist, 'song': song, 'broadcast' : air_date + ' ' + time})
        )
          
      except s3_client.exceptions.NoSuchBucket as e:
        print(e)
      except UnicodeEncodeError as e:
        print(e)


def main():
    # Your main program logic here
    handler(None, None)

if __name__ == "__main__":
    main()
