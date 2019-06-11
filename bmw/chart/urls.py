from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from . import views
from rest_framework.authtoken import views as authviews

# Create a router and register our viewsets with it.

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^getRecentChargerRecords$', views.RecentChargerRecordView.as_view()),  # 总电量变化
    url(r'^getAllRecentChargerRecords$', views.AllRecentChargerRecordView.as_view()),  # 总电量变化
]
