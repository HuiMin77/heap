from django.contrib import admin
import import_export
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import CCA
from .models import Student
from .models import Membership
from .models import Payment
from .models import Venue
from .models import Event
from .models import Attendance
from .models import PaymentPoll
from .models import PaymentDetails, Tracking_Payment
from django.contrib.auth.models import Group

admin.site.register(CCA)
admin.site.register(Student)
admin.site.register(Membership)
admin.site.register(Payment)
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(Attendance)
admin.site.register(PaymentPoll)
admin.site.register(PaymentDetails)
admin.site.register(Tracking_Payment)
admin.site.unregister(Group)


