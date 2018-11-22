from django.contrib import admin
from .models import UserStats, L4d2MapStats, GmodMapStats, UserSettings

    
admin.site.register(UserStats, admin.ModelAdmin)
admin.site.register(L4d2MapStats, admin.ModelAdmin)
admin.site.register(GmodMapStats, admin.ModelAdmin)
admin.site.register(UserSettings, admin.ModelAdmin)
