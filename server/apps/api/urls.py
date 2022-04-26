from django.urls import include, path, re_path
from rest_framework import routers
from server.apps.api.views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'submission_vote', SubmissionVoteViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Hacker News API",
      default_version='v1',
      description="Rest API of Hacker News Web App",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="alex.moa@estudiantat.upc.edu"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('test', Post_APIView.as_view(), name='test'),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
