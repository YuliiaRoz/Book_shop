from django.contrib import admin

import user_management.models

# Register your models here.
admin.site.register(user_management.models.DeliveryAddress)
admin.site.register(user_management.models.LastView)