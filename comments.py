#bilibili
#youtube 
#tiktok
# https://commentpicker.com/


import json
import yt_dlp
import os
URL = os.getenv('URL')
keyword = os.getenv('keyword')

# URL = 'https://www.youtube.com/c/DailyDoseComedy100'


if not os.path.exists('./videos'):
    os.makedirs('videos')
def commentsfromURL(URL):
    if '/video/' in URL:
        videoid=URL.split('/')[-1]
        data={'id':videoid}
        json_obj = json.dumps(data)
        with open('./videos/'+videoid+"episode.json", "w") as file:
                file.write(json_obj)    
    elif '/c/' in URL or '/channel/' in URL:
        channelid=URL.replace('https://youtube.com/channel/','')
        if channelid.endswith('/'):
                channelid=channelid.replace('/','')
        # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
        ydl_opts = {
                # 'outtmpl': videopath+'/%(title)s'+'.mp4',
                'format': 'best',
                'proxy': 'socks5://127.0.0.1:1080',
                'writeinfojson': 'true',
                'getcomments': 'true', 
                # 'postprocessors': [{ # Embed metadata in video using ffmpeg. 'key': 'FFmpegMetadata', 'add_metadata': True, }, { # Embed thumbnail in file 'key': 'EmbedThumbnail', 'already_have_thumbnail': False, }
                # 'postprocessors': [{
                #     # Embed metadata in video using ffmpeg.
                #     # ℹ️ See yt_dlp.postprocessor.FFmpegMetadataPP for the arguments it accepts
                #     'key': 'FFmpegMetadata',
                #     'add_chapters': True,
                #     'add_metadata': True,
                # }],
                # 'logger': MyLogger(),
                # 'progress_hooks': [my_hook],
                }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(URL, download=False)

        for entry in info['entries']:
            data={'id':entry['id']}
            json_obj = json.dumps(data)
            with open('./videos/'+entry['id']+"episode.json", "w") as file:
                file.write(json_obj)
