from django.contrib import admin
from apps.skillw.models import *

admin.site.index_title = "SGP 4436 ZHIMMA"
admin.site.site_header = "SKILLWAVE"

admin.site.index_title = "SKILLWAVE"

admin.site.register(Check_Pass)
admin.site.register(Create_User_Check)
admin.site.register(User_Info)
admin.site.register(Courses)
admin.site.register(Napravlenii)
admin.site.register(Zapis)
admin.site.register(Courses_Of_User)
admin.site.register(Themes)
admin.site.register(Progress)
admin.site.register(Files)
# admin.site.register(Chat)
# admin.site.register(Messengers)
admin.site.register(Message)
admin.site.register(Mentors)
admin.site.register(ZapisMentors)