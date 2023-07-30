from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import CCA
from .models import Student
from .models import Membership
from .models import Payment
from .models import Venue
from .models import Event
from .models import Attendance
from django.contrib.auth.models import Group

admin.site.register(CCA)
admin.site.register(Student)
admin.site.register(Membership)
admin.site.register(Payment)
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(Attendance)
admin.site.unregister(Group)


