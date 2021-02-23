try:
	import sys
	from django.urls import path
	from rest_framework.routers import DefaultRouter
	from .views import upload_profile_picture, api_root, create_userid, save_userid, get_user_properties
	from .views import search_users, profile, edit_profile, connect_accounts, show_feed
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(0)


app_name = 'api'

__all__ = ['urlpatterns']

urlpatterns = [path('', api_root, name='api-root'),
			   path('search/', search_users, name='search'),
               path('show-profile/', profile, name='profile'),
			   path('save-userid/', save_userid, name='save_userid'),
               path('show-feed/<int:page>/', show_feed, name='show_feed'),
			   path('create-feed/', connect_accounts, name='feed_creation'),
               path('create-userid/<int:num>/', create_userid, name='userid'),
			   path('user-properties/', get_user_properties, name='user_info'),
               path('settings/edit-profile/', edit_profile, name='settings_edit_profile'),
               path('upload-profile-picture/', upload_profile_picture, name='upload_prof_pic'),
               path('settings/connect_accounts/', connect_accounts, name='settings_connect_accounts'),]

router = DefaultRouter(trailing_slash=False)

urlpatterns += router.urls
