try:
    import sys
    from os import environ
    from apiclient.discovery import build
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(0)


def get_channel_videos(channel_id):
    """
    Get video ids from user channel and create embed posts.
    Args:
        channel_id - user channel id from youtube.
    Returns:
        videos - all videos from channel with embed posts.
    """
    videos_information = {}
    videos_information.setdefault('youtube', [])
    api_key = 'AIzaSyBZjcGApanP9VB1P83Z-kte5uXWSu8iNeQ'
    youtube = build('youtube', 'v3', developerKey=api_key)
    result = youtube.channels().list(id=channel_id, part='contentDetails').execute()

    playlist_id = result['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    videos = []
    next_page_token = None

    while True:
        res = youtube.playlistItems().list(playlistId=playlist_id, part='snippet', pageToken=next_page_token).execute()

        videos += (res['items'])
        try:
            next_page_token = res['nextPageToken']
        except KeyError:
            next_page_token = None

        if next_page_token is None:
            break

    for video in videos:
        each_video_info = {}
        each_video_info['image'] = video['snippet']['thumbnails']['maxres']['url']
        each_video_info['username'] = video['snippet']['channelTitle']
        each_video_info['publishedAt'] = video['snippet']['publishedAt']
        each_video_info['url'] = 'https://www.youtube.com/watch?v=' + video['snippet']['resourceId']['videoId']
        videos_information['youtube'].append(each_video_info)

    return videos_information


#def create_embed_posts(video_ids):
#    """
#    Create embed posts from all video ids.
#    Args:
#        video_ids - all video ids from youtube user channel.
#    Returns:
#        embed_posts - embed posts from youtube.
#    """
#    embed_posts = []
#    for each_video_id in video_ids:
#        embed = """<div style="overflow:hidden;position: relative;"><iframe frameborder="0" scrolling="no" marginheight="0" marginwidth="0"width="800" height="443" type="text/html" src="https://www.youtube.com/embed/%s?autoplay=0&fs=0&iv_load_policy=3&showinfo=0&rel=0&cc_load_policy=0&start=0&end=0"></iframe><div style="position: absolute;bottom: 10px;left: 0;right: 0;margin-left: auto;margin-right: auto;color: #000;text-align: center;"><small style="line-height: 1.8;font-size: 0px;background: #fff;"> <a href="https://youtube-embed.com/">Youtube Embed Code</a> </small></div><style>.newst{position:relative;text-align:right;height:420px;width:520px;} #gmap_canvas img{max-width:none!important;background:none!important}</style></div><br />""" % each_video_id['snippet']['resourceId']['videoId']
#        embed_posts.append(embed)
#
#    return embed_posts

#def get_user_channel_videos():
#    """
#    Get all videos from user channel and create embed posts
#    Args:
#        user_id - user specific id from youtube.
#    Returns:
#        channel_videos - dict with each channel video link and embed post.
#    """
#
#    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
#
#    # Disable OAuthlib's HTTPS verification when running locally.
#    # *DO NOT* leave this option enabled in production.
#    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
#
#    api_service_name = "youtube"
#    api_version = "v3"
#    client_secrets_file = "client_secret.json"
#
#    # Get credentials and create an API client
#    #flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
#    data = {"client_id":"976386814836-t4dsag3kgm26gaceglufir1i2qp2emu4.apps.googleusercontent.com","project_id":"torus-275211","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"biUfVI3N_gsq4HicRiX-cCBH"}
#
#    #credentials = flow.run_console()
#    url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&myRating=like&'
#    request = requests.get(url, data=data)#.videos().list(part="snippet,contentDetails,statistics",myRating="like")
#    print (request.text)
#    response = request.execute()
#
#    print(response)
#
#    url = "https://www.youtube.com/channel/UCs6YQthy97HMDOqb4KO9bCg"
#
#
#    payload = ""
#    headers = {'cookie': "VISITOR_INFO1_LIVE=_9CZA-7D8I4; GPS=1; YSC=Khb39qv_zcs", 'accept': "application/json",
#                'authorization': "Bearer : ya29.a0Ae4lvC1IsO0gGTg95JyI37CG5f1ySS4Evj4XeI8oe0OOy0eOwwVyPYYY994rf5dF340PTFn65qRi38CoArkTyOFcpAahJpk-YPAXz-RWqwZwbeRhK5d2avBiNdBWiyqys2ixw-9z7hazvu54zNSdCoAM8MjS4MR4fq0"
#
#                }
#    response = requests.get(url, headers=headers)
#
#    print(response.text)
#get_user_channel_videos()
