try:
    import sys
    import json
    from django.db import models
    from django.contrib.auth.models import User
    from django.db.models import URLField, TextField, CharField
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(0)


class IndividualUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Individual')
    User._meta.get_field('first_name')._unique = False
    profile_picture = models.URLField(max_length=256, null=True)
    verified = TextField(default='False')
    users_id = CharField(max_length=20, unique=True, blank=True, null=True)

    facebook = TextField(blank=True, null=True, default='{}')
    instagram = TextField(blank=True, null=True, default='{}')
    tiktok = TextField(blank=True, null=True, default='{}')
    twitter = TextField(blank=True, null=True, default='{}')
    youtube = TextField(blank=True, null=True, default='{}')
    snapchat = TextField(blank=True, null=True, default='{}')

    def __str__(self):
        return str(json.dumps({'first_name': self.user.first_name, 'email': self.user.email,
            'user_id': self.users_id, 'picture': self.profile_picture}))

    class Meta:
        db_table = 'individual'


class ProfessionalUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Professional')
    User._meta.get_field('first_name')._unique = False
    verified_account_link = TextField()
    verified = CharField(max_length=10, default='False', editable=True, blank=True)
    profile_picture = URLField(max_length=256, null=True)
    users_id = CharField(max_length=20, unique=True, blank=True, null=True)

    facebook = TextField(blank=True, null=True, default='{}')
    instagram = TextField(blank=True, null=True, default='{}')
    tiktok = TextField(blank=True, null=True, default='{}')
    twitter = TextField(blank=True, null=True, default='{}')
    youtube = TextField(blank=True, null=True, default='{}')
    snapchat = TextField(blank=True, null=True, default='{}')

    def __str__(self):
        return str(json.dumps({'first_name': self.user.first_name, 'email': self.user.email,
            'user_id': self.users_id, 'verified_account': self.verified_account, 'picture': self.profile_picture}))

    class Meta:
        db_table = 'professional'


class CorporateUser(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Corporate')
    company_name = models.TextField()
    profile_picture = URLField(max_length=256, null=True)
    corporate_link = CharField(max_length=200)
    verified = CharField(max_length=10, default='False', editable=True, blank=True)
    users_id = CharField(max_length=20, unique=True, blank=True, null=True)

    facebook = TextField(blank=True, null=True, default='{}')
    instagram = TextField(blank=True, null=True, default='{}')
    tiktok = TextField(blank=True, null=True, default='{}')
    twitter = TextField(blank=True, null=True, default='{}')
    youtube = TextField(blank=True, null=True, default='{}')
    snapchat = TextField(blank=True, null=True, default='{}')

    def __str__(self):
        return str(json.dumps({'company_name': self.company_name, 'email': self.user.email,
            'user_id': self.users_id, 'corporate_link': self.corporate_link, 'picture': self.profile_picture}))

    class Meta:
        db_table = 'corporate'
