from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from scholar.api import views

router = routers.SimpleRouter()
router.register(r"c", views.CardViewSet)
router.register(r"t", views.TopicViewSet)
router.register(r"source", views.SourceViewSet)
router.register(r"tag", views.TagViewSet)

urlpatterns = [
    path("api/login/", obtain_auth_token),
    path("api/", include(router.urls)),
]
