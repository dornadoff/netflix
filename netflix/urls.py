from django.contrib import admin
from django.urls import path, include
from film.views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register("kinolar", KinoViewSet)
router.register("izoh", IzohViewSet)
# router.register("aktyor", AktyorViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(router.urls)),
    path("hello/", HelloAPIView.as_view()),
    path("aktyorlar/", AktyorAPIView.as_view()),
    path("aktyor/<int:pk>/", AktyorDetailView.as_view()),
    path("tariflar/", TarifAPIView.as_view()),
    path("tariflar/ochirish/<int:pk>/", TarifOchirishAPIView.as_view()),
    path("tarif/<int:pk>/", TarifDetailView.as_view()),
    # path("kinolar/", KinoAPIViews.as_view()),
    # path("kinolar/<int:pk>/", KinoDetailAPIView.as_view()),
    path("get_token/", obtain_auth_token)

]
