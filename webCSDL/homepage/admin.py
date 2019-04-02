from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Main)
admin.site.register(Main_image)

admin.site.register(Member)

admin.site.register(ResearchArea)
admin.site.register(Research)
admin.site.register(Project)

admin.site.register(Journal)
admin.site.register(Conference)
admin.site.register(Patent)

admin.site.register(Notice)
admin.site.register(Seminar)
admin.site.register(Album)

admin.site.register(Contact)