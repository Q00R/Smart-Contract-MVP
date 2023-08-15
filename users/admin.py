from django.contrib import admin
from .models import Users, Document_shared, Documents,OneTimePassword

# Register your models here.
admin.site.register(Users)
admin.site.register(Documents)
admin.site.register(Document_shared)
admin.site.register(OneTimePassword)
