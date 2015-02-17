from django.contrib import admin
from item.models import * #BrandName,Tag,Photo,Item,Profile

# Register your models here.
admin.site.register(BrandName)
admin.site.register(Tag)
admin.site.register(Photo)
admin.site.register(Item)
admin.site.register(UserProfile)
admin.site.register(CodeCpa)
admin.site.register(ProductPlacement)
admin.site.register(GetMoney)