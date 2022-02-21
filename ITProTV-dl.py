import requests
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

dirPATH = '/content/drive/Shareddrives/msgsuite/dl-index/handsonhacking'
%cd $dirPATH

headers = {
    'Host': 'api.itpro.tv',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Authorization': '#', ## Add your Authorization Token Here !!!
    'Origin': 'https://app.itpro.tv',
    'Connection': 'close',
    'Referer': 'https://app.itpro.tv/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
}

def fetch_lacture_list(CourseName):
    params = (
        ('url', CourseName),
        ('brand', '00002560-0000-3fa9-0000-1d61000035f3'),
    )
    lacture_url_list, lacture_title_list = [], []
    response = requests.get('https://api.itpro.tv/api/urza/v3/consumer-web/course', headers=headers, params=params, verify=False)
    course_details = response.json()       
    for lacture in course_details['course']['episodes']:
        lacture_url_list.append(lacture['url'])
        lacture_title_list.append(lacture['title'])
    return lacture_url_list,lacture_title_list

    
#print(fetch_lacture_list('certified-ethical-hacker-v11'))

def dl_vtt(lac_list):
    lacture_with_num_obj = zip(lac_list[0], range(1,len(lac_list[0])+1), lac_list[1])
    for lacture,num,title in lacture_with_num_obj:
        params = (
            ('url', lacture),
        )
        response = requests.get('https://api.itpro.tv/api/urza/v3/consumer-web/brand/00002560-0000-3fa9-0000-1d61000035f3/episode', headers=headers, params=params, verify=False)
        result = response.json()
        # Get the vtt content
        r = requests.get((result['episode']['enCaptionLink']))
        # Saving the vtt
        with open(f"{num}. {title}.vtt", 'w', encoding='utf-8') as file:
            file.write(r.text)
        print(f'{num}. {title}.vtt downloaded!')

def dl_videos(lac_list):
    lacture_with_num_obj = zip(lac_list[0], range(1,len(lac_list[0])+1), lac_list[1])
    for lacture,num,title in lacture_with_num_obj:
        params = (
            ('url', lacture),
        )
        response = requests.get('https://api.itpro.tv/api/urza/v3/consumer-web/brand/00002560-0000-3fa9-0000-1d61000035f3/episode', headers=headers, params=params, verify=False)
        vid_url = response.json()['episode']['jwVideo720Embed']  # Change Resolution
        print(f'Downloading file:{num}. {title}.mp4')

        r = requests.get(vid_url, stream = True)
        with open(f"{num}. {title}.mp4", 'wb') as f:
          for chunk in r.iter_content(chunk_size = 1024*1024):
              if chunk:
                  f.write(chunk)  
        print(f'{num}. {title}.mp4 downloaded!')

if __name__ == "__main__":
    course_Name = 'handsonhacking'  ## Change the course name
    lac_list = fetch_lacture_list(course_Name) 
    dl_vtt(lac_list) ## Download captions
    dl_videos(lac_list) ## Download videos
