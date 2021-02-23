try:
	import sys
	from drf_yasg import openapi
	from api.views import MainView
	from django.contrib import admin
	from django.urls import path, include
	from drf_yasg.views import get_schema_view
	from rest_framework.permissions import AllowAny
	from rest_framework_swagger.views import get_swagger_view
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(0)


schema_view = get_schema_view(
    openapi.Info(
        title="Scheduliser API",
        default_version='v1',
        description="Version 1.0",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
		path('', MainView, name='main'),
		path('admin/', admin.site.urls),
		path('auth/', include('users.urls')),
		path('api/', include(('api.urls', 'api'))),
    	path('swagger/', schema_view.as_view(), name='swagger'),
]
