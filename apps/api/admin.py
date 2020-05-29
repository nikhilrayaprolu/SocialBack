from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Organization)
admin.site.register(School)
admin.site.register(Class)
admin.site.register(Section)
admin.site.register(Course)
admin.site.register(UserMiniProfile)
admin.site.register(UserSectionMapping)
admin.site.register(Page)
admin.site.register(FeedModerator)
admin.site.register(GlobalGroup)
admin.site.register(SchoolGroup)
admin.site.register(Follow)

