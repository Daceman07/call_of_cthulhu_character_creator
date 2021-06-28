from django.contrib import admin
from .models import CharBasicInfo, Characteristics, BackStory, Skills, Equipment, Weapons, CashAndAssets

# Register your models here.
admin.site.register(CharBasicInfo)
admin.site.register(Characteristics)
admin.site.register(BackStory)
admin.site.register(Skills)
admin.site.register(Equipment)
admin.site.register(Weapons)
admin.site.register(CashAndAssets)
