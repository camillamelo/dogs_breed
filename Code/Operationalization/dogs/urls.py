"""dogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import  url
from django.urls import include, path
from rest_framework import routers
from get_breed import views

router = routers.DefaultRouter()
router.register(r'pictures', views.PicturesViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    url(r'^classifybreed/', views.ClassifyBreed.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('pictures_classifier/', views.PicturesAPIView.as_view()),
    path('dash/', views.dashboard_home, name="dashboard"),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]
