try:
    import os
    import sys
    import random
    import string
    from datetime import datetime
    from random import randint
    from django.core.files.storage import FileSystemStorage
    from django.conf import settings
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(0)


def upload_pic(picture, dir_name='services'):
    pic = FileSystemStorage()

    chars = string.ascii_letters + string.digits
    random_char = random.choice(chars)
    i = randint(0, 14)
    time_name = datetime.now().strftime("%m%d%Y%H%M%S")
    full_name = time_name[:i] + random_char + time_name[i:]
    filename = "{}.{}".format(full_name, picture.name.split('.')[-1])
    print("FILE NAME - ",  picture.name, filename)
    pic.save(filename, picture)

    pic_path = os.path.join(settings.MEDIA_ROOT, filename)
    os.system("aws s3 cp {} s3://likelocal-io/{}/".format(pic_path, dir_name))
    os.system("rm {}".format(pic_path))
    return 'https://likelocal-io.s3.us-east-2.amazonaws.com/{}/{}'.format(dir_name, filename)


def remove_pic(pic_url):
    if pic_url != 'https://':
        pic_path = pic_url.split('amazonaws.com/')[1]
        os.system("aws s3 rm s3://likelocal-io/{}".format(pic_path))
