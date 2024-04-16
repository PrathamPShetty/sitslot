from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Existing URL patterns
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),  # Added trailing slash
    path('event/', views.event, name='event'),  # Renamed URL name to 'event'
    path('contact', views.contact, name='contact'),  # Added trailing slash
    path('book/<int:myuser_id>/', views.book, name='book'),
    path('login/', views.login, name='login'),
    path('handlelogout/', views.handlelogout, name='handlelogout'),
    path('signup/', views.signup, name='signup'),
    path('update/<int:myuser_id>/', views.update, name='update'),
    path('deleteit/<int:event_id>/', views.deleteit, name='deleteit'),  # Updated URL pattern
    path('do_update/<int:event_id>/', views.do_update, name='do_update'),  # Updated URL pattern
    path('gallery/<int:place_id>/', views.gallery, name='gallery'),
    path('display/<int:event_id>/', views.display, name='display'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
