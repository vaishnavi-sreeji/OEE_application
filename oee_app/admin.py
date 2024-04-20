from django.contrib import admin
from .models import Machines, ProductionLog

admin.site.register(Machines)
admin.site.register(ProductionLog)
