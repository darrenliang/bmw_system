from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from . import views
from .admin import admin
from rest_framework.authtoken import views as authviews

# Create a router and register our viewsets with it.

admin.site.site_header = 'BMW Admin Portal'
admin.site.index_title = 'Features area'
admin.site.site_title = 'BMW from adminsitration'

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-token-auth/', authviews.obtain_auth_token),
    url(r'^api/basic/settings/$', views.BasicSettingsView.as_view()),  # json api
    url(r'^api/charger/details/$', views.ChargerDetails.as_view()),  # json api
    url(r'^api/charging/record/details/$', views.ChargingRecordDetails.as_view()),  # json api
    url(r'^$', views.login, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^overview/$', views.overview, name='overview'),
    url(r'^devices/$', views.devices, name='devices'),
    url(r'^charts/$', views.charts, name='charts'),
    url(r'^details/$', views.details, name='details'),
    url(r'^settings/$', views.setting, name='settings'),
    url(r'^audit_logs/$', views.audit_logs, name='audit_logs'),
    url(r'^web_socket/$', views.web_socket, name='web_socket'),
    url(r'^remote/$', views.remote, name='remote'),
    url(r'^test/$', views.test, name='test'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
