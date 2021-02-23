try:
    import re
    import sys
    import ast
    import jwt
    import json
    import random
    import string
    import requests

    from itertools import chain

    from rest_framework.response import Response
    from rest_framework.decorators import api_view

    from tools.tiktok_tools import get_tiktok_posts
    from tools.youtube_tools import get_channel_videos
    from tools.orm_tools import user_exist, get_or_none
    from tools.facebook_tools import get_facebook_posts
    from tools.instagram_tools import get_instagram_posts

    from .models import IndividualUser, ProfessionalUser, CorporateUser

    from django.template import loader
    from django.shortcuts import render
    from django.contrib.auth.models import User
    from django.http import HttpResponse, JsonResponse
    from django.views.decorators.csrf import csrf_exempt
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(0)

@csrf_exempt
def MainView(request):
    template = 'index.html'

    context = {}
    return render(request, template, {'context': context})


@api_view(['GET'])
def api_root(request, format=None):
    return Response({})


@csrf_exempt
def create_userid(request, num):
    """
    Create user ids for ordinary and premium accounts.
    Args:
        request - user request
        num - number for choosing account type.
    Returns:
        ---
    """
    try:
        # Create dictionary from jwt token
        user_info = jwt.decode(request.headers['token'], 'SECRET_KEY', algorithms=['HS256'])
    except KeyError:
        return HttpResponse(json.dumps({'token': 'not exist'}), status=500, content_type='application/json')

    userid = int(user_info['id'])

    user = user_exist(userid)
    if not user:
        return HttpResponse(json.dumps({'message': 'User doesn\'t exist', 'id': user_id}),
                status=500, content_type='application/json')

    if num == 0:
        user_id = ''.join(random.choices(string.ascii_uppercase, k=3) + random.choices(string.digits, k=6))
        while user.users_id == user_id:
            user_id = ''.join(random.choices(string.ascii_uppercase, k=3) + random.choices(string.digits, k=6))

        return HttpResponse(json.dumps({'user_id': user_id, 'id': userid}), status=200, content_type='application/json')

    elif num == 1:

        # all data corresponding user input
        data = json.loads(request.body.decode('utf-8'))

        user_id = data['user_id']
        match = re.match(r"([a-z]+)([0-9]+)", user_id, re.I)
        # Get string from user id
        user_id_string_part = match.group(1)
        # Get digits from user id
        user_id_digit_part = match.group(2)
        if len(user_id_string_part) != 3 or len(user_id_digit_part) != 6:
            return HttpResponse(json.dumps({'message': 'Please fill all fileds for user id section'}),
                    status=200, content_type='application/json')

        user_ids = {}

        all_users_id = [user_id['users_id'] for user_id in list(chain(IndividualUser.objects.all().values('users_id'),
            ProfessionalUser.objects.all().values('users_id'),
            CorporateUser.objects.all().values('users_id')))]

        if user_id in all_users_id:
            index = 0
            while len(user_ids.keys()) != 6:
                user_id = ''.join(random.choices(user_id_string_part, k=3) + random.choices(user_id_digit_part, k=6))
                if not user_id in user_ids.values():
                    user_ids['user_id' + str(index)] = user_id
                    index += 1

            return HttpResponse(json.dumps({'is_available': False, 'similar': user_ids}),
                    status=200, content_type='application/json')
        else:
            user_ids['user_id'] = user_id
            return HttpResponse(json.dumps({'is_available': True, 'user_id': user_ids['user_id']}),
                    status=200, content_type='application/json')


@csrf_exempt
def save_userid(request):
    """
    Get user id from given request and save in DB.
    Args:
        request - user request
    Returns:
        message - response according user exist or not
    """
    try:
        # Create dictionary from jwt token
        user_info = jwt.decode(request.headers['token'], 'SECRET_KEY', algorithms=['HS256'])
    except KeyError:
        return HttpResponse(json.dumps({'token': 'not exist'}), status=500, content_type='application/json')

    userid = int(user_info['id'])

    user = user_exist(userid)
    if not user:
        return HttpResponse(json.dumps({'message': 'User doesn\'t exist', 'id': user_id}),
                status=500, content_type='application/json')

    # all data corresponding user input
    data = json.loads(request.body.decode('utf-8'))

    user_id = data['user_id']

    user.users_id = user_id
    user.save()

    return HttpResponse(json.dumps({'message': 'user id saved'}), status=200, content_type='application/json')


def get_user_properties(request):
    """
    Return current user information
    Args:
        request - user request
    Returns:
        user - current user information
    """
    try:
        # Create dictionary from jwt token
        user_info = jwt.decode(request.headers['token'], 'SECRET_KEY', algorithms=['HS256'])
    except KeyError:
        return HttpResponse(json.dumps({'status': 'error', 'token': 'not exist'}), status=500, content_type='application/json')

    user_id = int(user_info['id'])

    user = get_or_none(User, id=user_id)

    if not user:
        return HttpResponse(json.dumps({'message': 'User doesn\'t exist', 'id': user_id}),
                status=500, content_type='application/json')

    first_name, company_name = '',''
    try:
        first_name = user.first_name
    except TypeError:
        company_name = user.company_name

    current_user = user_exist(user_id)
    accounts = ['snapchat' if ast.literal_eval(current_user.snapchat) else '',
            'instagram' if ast.literal_eval(current_user.instagram) else '',
            'facebook' if ast.literal_eval(current_user.facebook) else '',
            'snapchat' if ast.literal_eval(current_user.snapchat) else '',
            'youtube' if ast.literal_eval(current_user.youtube) else '',
            'tiktok' if ast.literal_eval(current_user.tiktok) else '']

    if first_name:
        content = {'id': user.id, 'name': first_name, 'email' : user.email, 'is_verified' : user.is_active,
                'profile_picture': current_user.profile_picture,
                'user_id' : current_user.users_id, 'password': user.password,
                'accounts': list(filter(lambda x:x != "", accounts))}

    if company_name:
        content = {'id': user.id, 'name': company_name, 'email' : email, 'is_verified' : user.is_active,
                'profile_picture': current_user.profile_picture,
                'user_id': current_user.users_id, 'password': user.password,
                'accounts': list(filter(lambda x:x != "", accounts))}

    return HttpResponse(json.dumps(content), status=200, content_type='application/json')


@csrf_exempt
def upload_profile_picture(request):
    """
    Upload picture
    Args:
        request - user request.
    Returns:
        ---
    """
    # Create dictionary from jwt token
    user_info = jwt.decode(request.headers['token'], 'SECRET_KEY', algorithms=['HS256'])

    # all data corresponding user input
    data = json.loads(request.body.decode('utf-8'))

    user_id = int(user_info['id'])

    user = user_exist(user_id)
    if not user:
        return HttpResponse(json.dumps({'message': 'User doesn\'t exist', 'id': user_id}),
                status=500, content_type='application/json')

    user.profile_picture = data['profile_picture']
    user.save()

    return HttpResponse(json.dumps({'message': 'Picture uploaded',}), status=200, content_type='application/json')


def search_users(request):
    """
    Search all users with given name or users_id and return users list.
    Args:
        request - user search pattern
    Returns:
        all_user(s) - list with all searched user(s) if they are exist with given search pattern.
    """
    all_users = []
    # all data corresponding user input
    data = json.loads(request.body.decode('utf-8'))

    search_pattern = data['pattern']

    # Search in individual users
    for user in list(chain(IndividualUser.objects.all().values('user__first_name','user__email', 'users_id', 'image').distinct())):
        if user['user__first_name'] == search_pattern or user['users_id'] == search_pattern:
            all_users.append(user)

    # Search in professional users
    for user in list(chain(ProfessionalUser.objects.all().values('user__first_name','user__email', 'users_id', 'image').distinct())):
        if user['user__first_name'] == search_pattern or user['users_id'] == search_pattern:
            all_users.append(user)

    # Search in corporate users
    for user in list(chain(CorporateUser.objects.all().values('company_name','user__email', 'users_id', 'image').distinct())):
        if user['company_name'] == search_pattern or user['users_id'] == search_pattern:
            all_users.append(user)

    if all_users:
        return HttpResponse(json.dumps({'data': all_users,}), status=200, content_type='application/json')
    else:
        return HttpResponse(json.dumps({'status': 'error', 'data': 'Not found',}), status=200, content_type='application/json')


@csrf_exempt
def edit_profile(request):
    """
    Edit user profile especially picture and full name.
    Args:
        request - user request for editing profile.
    Returns:
        ----
    """
    # Create dictionary from jwt token
    user_info = jwt.decode(request.headers['token'], 'SECRET_KEY', algorithms=['HS256'])

    # all data corresponding user input
    data = json.loads(request.body.decode('utf-8'))

    user_id = user_info['id']
    user = user_exist(user_id)
    if not user:
        return HttpResponse(json.dumps({'message': 'User doesn\'t exist', 'id': user_id}),
                status=500, content_type='application/json')

    try:
        user.profile_picture = data['image']
    except KeyError:
        pass

    if 'IndividualUser' == user.__class__.__name__ or 'ProfessionalUser' == user.__class__.__name__:
        user.first_name = data['name']

    if 'CorporateUser' == user.__class__.__name__:
        user.company_name = data['name']

    user.save()

    return HttpResponse(json.dumps({'message': 'profile edited',}), status=200, content_type='application/json')


def paginate(users_list, page=1, limit=3, **kwargs):
    """
    Show information about each social media by pages.
    Args:
        users_list - dictionary with all connected social media and information.
        page - page number.
        limit - posts limit for showing.
        **kwargs - optional
    """
    min_limit = 3
    max_limit = 5
    try:
        page = int(page)
        if page < 1:
            page = 1
    except (TypeError, ValueError):
        page = 1

    try:
        limit = int(limit)
        if limit < min_limit:
            limit = min_limit
        if limit > max_limit:
            limit = max_limit
    except (ValueError, TypeError):
        limit = max_limit

    paginator = Paginator(users_list, limit)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    data = {
        'previous_page': objects.has_previous() and objects.previous_page_number() or None,
        'next_page': objects.has_next() and objects.next_page_number() or None,
        'users_list' : list(objects)}
    return data


def show_feed(request, page):
    """
    Show all scraped data for each social media web page.
    Args:
        request
    """
    all_users_info = []

    # Create dictionary from jwt token
    user_info = jwt.decode(request.headers['token'], 'SECRET_KEY', algorithms=['HS256'])

    user_id = int(user_info['id'])
    user = user_exist(user_id)
    if not user:
        return HttpResponse(json.dumps({'message': 'User doesn\'t exist', 'id': user_id}),
                status=500, content_type='application/json')

    for users_info in User.objects.all():
        user = user_exist(users_info.id)
        if user:
            data = {**ast.literal_eval(user.facebook), **ast.literal_eval(user.instagram),
                    **ast.literal_eval(user.tiktok), **ast.literal_eval(user.youtube),
                    **ast.literal_eval(user.snapchat), **ast.literal_eval(user.twitter)}
            if data:
                if len(data) > 2:
                    all_users_info.append({'users_id' : user.users_id, 'first_name' : users_info.first_name,
                    'data': random.sample(data.items(), k=3)})
                else:
                    all_users_info.append({'users_id' : user.users_id, 'first_name' : users_info.first_name,
                    'data': data})


    return JsonResponse({"resources": paginate(all_users_info, page, 10)})


@csrf_exempt
def connect_accounts(request):
    """
    Create user feed for show posts from selected social media account.
    Args:
        request - user request for connect social media.
        page - social media number.
    Returns:
        post - connected social media post.
    """
    # dict with all string for show
    payload = ""
    headers = ""
    # Create dictionary from jwt token
    user_info = jwt.decode(request.headers['token'], 'SECRET_KEY', algorithms=['HS256'])

    # all data corresponding user input
    data = json.loads(request.body.decode('utf-8'))

    user_id = int(user_info['id'])

    user = user_exist(user_id)
    if not user:
        return HttpResponse(json.dumps({'message': 'User doesn\'t exist', 'id': user_id}),
                status=500, content_type='application/json')

    for social_media_name, users_info in data.items():
        # Get facebook user posts
        if social_media_name == 'facebook':
            try:
                user.facebook = get_facebook_posts(users_info)
            except Exception:
                pass

        # Get tiktok user posts
        if social_media_name == 'tiktok':
            try:
                user.tiktok = get_tiktok_posts(users_info)
            except Exception:
                pass

        # Get instagram posts
        if social_media_name == 'instagram':
            try:
                user.instagram = get_instagram_posts(users_info)
            except Exception:
                pass

        if social_media_name == 'youtube':
            try:
                user.youtube = get_channel_videos(users_info)
            except Exception:
                pass

        if social_media_name == 'snapchat':
            pass

        if social_media_name == 'twitter':
            pass

    user.save()
    return HttpResponse(json.dumps({'message':'feed updated',}), status=200, content_type='application/json')


##############################################################################################################
#        print(response.text)
#    # Get posts from instagram account.
#    if num == 0:
#
#        #response = requests.get('https://api.instagram.com/oembed?url=https://www.instagram.com/p/B_QyHMvnnRt/')
#        #template = loader.from_string(response.json()['html'])
#        #return HttpResponse(template.render())
#
#        template = loader.get_template("instagram_test.html")
#        return HttpResponse(template.render())
#    if num == 1:
#
#        template = loader.get_template("facebook_test.html")
#        return HttpResponse(template.render())
#    if num == 2:
#
#        template = loader.get_template("tiktok_test.html")
#        return HttpResponse(template.render())
#    if num == 3:
#
#        template = loader.get_template("twitter_test.html")
#        return HttpResponse(template.render())

def profile(request):
    """
    Create user profile with given uesr id.
    Args:
        request - user request for getting user id.
    Returns:
        HttpResponse - user profile image, first name, uesr_id,
    """
    # Create dictionary from jwt token
    user_info = jwt.decode(request.headers['token'], 'SECRET_KEY', algorithms=['HS256'])
    user_id = int(user_info['id'])

    user = user_exist(user_id)
    if not user:
        return HttpResponse(json.dumps({'message': 'User doesn\'t exist'}),
                status=500, content_type='application/json')

    user_information = {'name' : user_info['name'], 'users_id' : user_info['users_id'],
            'profile_picture': user_info['profile_picture'], 'facebook' : user.facebook,
            'tiktok' : user.tiktok, 'instagram' : user.instagram, 'snpachat': user.snapchat,
            'youtube' : user.youtube, 'twitter' : user.twitter}
    print (user_information)
    return HttpResponse(json.dumps({'message': 'feed exist', 'data': user_information}), status=200, content_type='application/json')
