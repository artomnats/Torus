try:
    import jwt
    import sys
    import json

    from tools import email_tools, str_tools
    from tools.email_tools import last_sended_email
    from tools.orm_tools import user_exist, get_or_none

    from django.http import HttpResponse
    from django.contrib.auth.models import User
    from django.views.decorators.csrf import csrf_exempt
    from django.contrib.auth import authenticate, login, logout

    from api.models import IndividualUser, ProfessionalUser, CorporateUser
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(0)


@csrf_exempt
def user_register(request, num):
    """
    Create db according to user input and choosing account type.
    Args:
        request - user request.
        num - account type identification number.
    Returns:
        ---
    """
    # Create verification code for sending emails
    verification_code = str_tools.random_str(10)
    subject = 'Verification email'
    text = "Welcome to Torus family.\nPlease verify your account by entering in app\n\nVerification Code - %s" % verification_code

    user = User()
    # all data corresponding user input
    data = json.loads(request.body.decode('utf-8'))

    if num == 0:

        # Full name from user input
        first_name = data['name']
        # Get email for user
        email = data['email'].lower()
        # Get password for user
        password = data['password']
        try:
            # Get profile picture
            image = data['image']
        except KeyError as valerr:
            image = ''

        # Check user exist or not
        if get_or_none(User, email=email):
            return HttpResponse(json.dumps({'status': 'error', 'error':\
                    {'code': 1, 'text': 'Username already registered'},}),
                    status=500, content_type='application/json')

        user.first_name = first_name
        user.username = email
        user.email = email
        user.password = password
        user.is_active = False

        user.save()

        IndividualUser.objects.create(user=user, profile_picture=image)

        print("START SENDING EMAIL\n")
        email_tools.send_email(email, subject, text, user.id)
        print("END SENDING EMAIL\n")

        content = {'id': user.id, 'first_name': first_name, 'email' : email,
                   'password': password, 'online': user.is_active}

        jwt_token = {'token': jwt.encode(content, "SECRET_KEY").decode("utf-8")}

        return HttpResponse(json.dumps(jwt_token), status=200, content_type='application/json')

    elif num == 1:

        # Full name from user input
        first_name = data['name']
        # Get email for user
        email = data['email']
        # Get password for user
        password = data['password']
        # Get verified account link
        verified_account = data['verified_account']

        try:
            # Get profile picture
            image = data['image']
        except KeyError as valerr:
            image = ''

        # Check user exist or not
        if get_or_none(User, email=email):
            return HttpResponse(json.dumps({'status': 'error', 'error':\
                    {'code': 1, 'text': 'Username already registered'},
                    }), status=500, content_type='application/json')

        user.first_name = first_name
        user.email = email
        user.username = email
        user.password = password
        user.is_active = False
        user.save()

        ProfessionalUser.objects.create(user=user, profile_picture=image, verified_account_link=verified_account)

        print("START SENDING EMAIL\n")
        email_tools.send_email(email, subject, text, user.id)
        print("END SENDING EMAIL\n")

        content = {'id': user.id, 'first_name': first_name, 'email' : email,
                   'password': password, 'online': user.is_active}

        jwt_token = {'token': jwt.encode(content, "SECRET_KEY").decode("utf-8")}

        return HttpResponse(json.dumps(jwt_token), status=200, content_type='application/json')

    elif num == 2:

        # Get email for user
        email = data['email']
        # Get password for user
        password = data['password']
        # Company name from user input
        company_name = data['name']
        # Get corporate link address
        corporate_link = data['corporate_link']

        try:
            # Get profile picture
            image = data['image']
        except KeyError as valerr:
            image = ''

        # Check user exist or not
        if get_or_none(User, email=email):
            return HttpResponse(json.dumps({'status': 'error', 'error': \
                    {'code': 1, 'text': 'Username already registered'},
                    }), status=500, content_type='application/json')

        user.email = email
        user.password = password
        user.is_active = False
        user.save()

        # Create corporate user
        corporate = CorporateUser()

        CorporateUser.objects.create(user=user, company_name=company_name, profile_picture=image,
                corporate_link=corporate_link)

        print("START SENDING EMAIL\n")
        email_tools.send_email(email, subject, text, user.id)
        print("END SENDING EMAIL\n")

        content = {'id': user.id, 'company_name': company_name, 'email' : email,
                    'password': password, 'online': user.is_active}

        jwt_token = {'token': jwt.encode(content, "SECRET_KEY").decode("utf-8")}

        return HttpResponse(json.dumps(jwt_token), status=200, content_type='application/json')


@csrf_exempt
def signup_verification(request):
    """
    Checking sign up verification code
    Args:
        request - user request
    Returns:
        ---
    """
    # Create dictionary from jwt token
    user_info = jwt.decode(request.headers['token'], 'SECRET_KEY', algorithms=['HS256'])

    # all data corresponding user input
    data = json.loads(request.body.decode('utf-8'))

    user_id = int(user_info['id'])
    verification_key = data['key']

    user = user_exist(user_id)
    if not user:
        return HttpResponse(json.dumps({'message': 'user doesn\'t exist', 'id': user_id,}),
                status=200, content_type='application/json')
    try:
        key = last_sended_email[user_id]
    except KeyError:
        key = ''

    print("VERIF KEY - {}".format(verification_key))
    print("AMAZON KEY - {}".format(key))

    if key != verification_key:
        return HttpResponse(json.dumps({'status': 'ok','is_verified':'False'}), status=405, content_type='application/json')

    user.verified = 'True'
    user.is_active = True
    user.save()

    return HttpResponse(json.dumps({'message': 'user finished verification','is_verified':'True'}),
            status=200, content_type='application/json')


@csrf_exempt
def reset_password(request):
    """
    Reset user password
    Args:
        user_id - unique id for each user.
        password - new password for user.
    """
    # Create dictionary from jwt token
    user_info = jwt.decode(request.headers['token'], 'SECRET_KEY', algorithms=['HS256'])

    # all data corresponding user input
    data = json.loads(request.body.decode('utf-8'))

    user_id = int(user_info['id'])
    password = user_info['password']

    user = User.objects.get(id=user_id)
    if not user:
        return HttpResponse(json.dumps({'message': 'user doesn\'t exist', 'id': user_id,}),
                status=200, content_type='application/json')

    #email = data['email']
    #verification_key = data['key']

    #print("Email - ", email)

    #user = get_or_none(User, username=email)
    #if not user:
    #    return HttpResponse(json.dumps({'status': 'ok',}), status=405, content_type='application/json')

    #key = last_sended_email[email]

    #print("VERIF KEY - {}".format(verification_key))
    #print("REDIS KEY - {}".format(key))


    #if key != verification_key:
    #    context = {'validated': False, 'error': 'invalid verification code', 'first_name': user.first_name,
    #                    'last_name': user.last_name,}
    #    return HttpResponse(json.dumps({'status': 'ok', 'data': context}), status=405, content_type='application/json')
    #else:
    user.password = password
    user.save()
    return HttpResponse(json.dumps({'message': 'password changed',}), status=200, content_type='application/json')


@csrf_exempt
def user_login(request):
    """
    Login to Torus app.
    Args:
        request - user request with email and password.
    Returns:
        ----
    """
    # all data corresponding user input
    data = json.loads(request.body.decode('utf-8'))

    # Get email from user request
    email = data['email']
    # Get password from user request
    password = data['password']

    user = get_or_none(User, email=email, password=password)
    if not user:
        return HttpResponse(json.dumps({'message': 'Username doesn\'t exist'}),
                status=500, content_type='application/json')
    else:
        if request.user.is_authenticated:
            return HttpResponse(json.dumps({'status': 'User already loged in',}), status=200, content_type='application/json')
        else:
            login(request, user)
            print("\nUSER - {}".format(email))
            print("PASSWORD - {}".format(password))
            first_name, company_name = '',''
            try:
                first_name = user.first_name
            except AttributeError:
                company_name = user.company_name

            user.is_active = True
            if first_name:
                content = {'id': user.id, 'name': first_name, 'email' : email,
                            'password': password, 'online': user.is_active}

            elif company_name:
                content = {'id': user.id, 'name': company_name, 'email' : email,
                            'password': password, 'online': user.is_active}

            jwt_token = {'token': jwt.encode(content, "SECRET_KEY").decode("utf-8")}

            return HttpResponse(json.dumps(jwt_token), status=200, content_type='application/json')


def user_logout(request):
    """
    Logout from application.
    Args:
        request - user request
    Returns:
        ----
    """
    logout(request)
    return HttpResponse(json.dumps({'status': 'ok',}), status=200, content_type='application/json')
