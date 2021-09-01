from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from scholar.api import views

router = routers.SimpleRouter()
router.register(r"card", views.CardViewSet)
router.register(r"topic", views.TopicViewSet)
router.register(r"source", views.SourceViewSet)
router.register(r"tag", views.TagViewSet)

urlpatterns = [
    path("api/login/", obtain_auth_token),
    path("api/search/", views.search),
    path("api/", include(router.urls)),
]
