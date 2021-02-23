try:
    import sys
    import json
    import requests
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(0)

#def create_embed_post(url):
#    """
#    Create iframe for showing facebook posts.
#    Args:
#        url - post url for create iframe
#    Returns:
#        iframe - string with given post url.
#    """
#    iframe = "<iframe src=\"https://www.facebook.com/plugins/post.php?href={0}&width=500\" width=\"500\" height=\"463\" style=\"border:none;overflow:hidden\" scrolling=\"no\" frameborder=\"0\" allowTransparency=\"true\" allow=\"encrypted-media\"></iframe>".format(url)
#    return iframe


def get_facebook_posts(access_token):
    """
    Get current user posts and create embed files.
    Args:
        access_token - user specific access token for getting permisions from profile.
    Returns:
        iframes - dict with all post information
    """
    facebook_feed_info = {}
    facebook_feed_info.setdefault('facebook', [])

    querystring = {"access_token": access_token}


    username_url = "https://graph.facebook.com/v6.0/me/"
    ids_url = "https://graph.facebook.com/v6.0/me/posts"
    attachment_url = 'https://graph.facebook.com/v6.0/{0}/attachments'
    # Get all ids from user posts
    try:
        data = requests.get(ids_url, params=querystring).json()['data']
    except Exception:
        print ('Access Token was expired')
    # Get first 5 post_ids for showing in the app.
    for post in data:
        post_info = {}
        try:
            response = requests.get(attachment_url.format(post['id']), params=querystring).json()
        except Exception:
            continue
        try:

            post_info['username'] = requests.get(username_url, params=querystring).json()['name']
            post_info['publishedAt'] = post['created_time']
            try:
                post_info['url'] = response['data'][0]['target']['url'].replace('\\', '')
                post_info['image'] = response['data'][0]['media']['image']['src']
                #facebook_feed_info['post_html'] = create_embed_post(post_url)
                #iframes[post_url]  = facebook_feed_info
            except Exception:
                post_info['url'] = response['data'][0]['subattachments']['data'][0]['target']['url'].replace('\\', '')
                post_info['image'] = response['data'][0]['subattachments']['data'][0]['media']['image']['src']
        except Exception:
            pass

        facebook_feed_info['facebook'].append(post_info)

    return facebook_feed_info
