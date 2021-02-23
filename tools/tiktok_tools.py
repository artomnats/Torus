try:
    import sys
    import json
    import requests
    from datetime import datetime
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(0)


def get_tiktok_posts(username):
    """
    Get current user posts and create embed files.
    Args:
        username - specific username for getting posts.
    Returns:
        videos - dict with username and all post informationn
    """
    videos = {}
    videos.setdefault('tiktok', [])

    tiktok_url = "https://tiktok.p.rapidapi.com/live/user/feed"
    headers = {'x-rapidapi-host': "tiktok.p.rapidapi.com",
        'x-rapidapi-key': "be0a68b1a4msh397116dc2592dbep13ec3bjsn5d0b34fda599"}

    querystring = {"username": username}
    try:
        response = requests.get(tiktok_url, headers=headers, params=querystring).json()
        #all_videos = [all_video['video'] for all_video in response['media'] if all_video['video']]
        all_videos = [all_video for all_video in response['media'] if all_video['video']]

        for video_info in all_videos:
            info = {}
            info['username'] = video_info['author']['uniqueId']
            info['url'] = video_info['video']['playAddr']
            info['image'] = video_info['video']['originCover']
            info['publishedAt'] = datetime.fromtimestamp(video_info['create_time']).strftime('%Y-%m-%d %H:%M:%S')
            videos['tiktok'].append(info)
    except Exception as exception:
        return json.dumps({'status': 'error/redis client blocked'})

    return videos
