try:
    import sys
    from django.urls import path
    from rest_framework_simplejwt import views as jwt_views
    from .views import user_register, signup_verification, reset_password, user_login, user_logout
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(0)

urlpatterns = [path('login/', user_login, name='login'),
               path('logout/', user_logout, name='logout'),
               path('reset-password/', reset_password, name='reset'),
               path('register/<int:num>/', user_register, name='acount_create'),
               path('signup-verification/', signup_verification, name='signup_verification'),
               path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
               path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),]
