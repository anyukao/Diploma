from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from .views import *

urlpatterns = [
    path("", home, name='home'),
    path("accounts/login/", home, name='loghome'),
    path("homepage/", homepage, name='homepage'),
    path("check_code/<email>", check_code, name='check_code'),
    path("check_code_regist/<int:id>", check_code_regist, name='check_code_regist'),
    path("logout/", user_logout, name='logout'),
    path("personal/", personal, name='personal'),
    path("directions/", directions, name='directions'),
    path("calendar/", calendar, name='calendar'),
    path("courses/", courses, name='courses'),
    path("courses/<int:id>", courses_info, name='courses_info'),
    path("notifications/", notifications, name='notifications'),
    path("allcourses/", allcourses, name='allcourses'),
    path("themes/<int:id>/",themes, name='themes'),
    path("lesson/<int:id>/",lesson, name='lesson'),
    path('documents/download/<int:document_id>/',  download_document, name='download_document'),
    path('doc/',  doc, name='doc'),
    path('coursesofmentor/',  coursesofmentor, name='coursesofmentor'),
    path('tableofmentor/<int:id>/',  tableofmentor, name='tableofmentor'),
    path('themesmentor/<int:id>/',  themesmentor, name='themesmentor'),
    # path('chat/',  lobby, name='chat'),
    # path('chat/<str:room_name>/',  room, name='room'),



    #   path('theme/<int:theme_id>/chat/', theme_chat, name='theme_chat'),
    # path('', include('apps.skillw.urls')),
]

urlpatterns += static(settings.STATIC_URL,
                              document_root=settings.STATIC_URL)
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)