from django.contrib import admin
from .models import Country, Race, State, Delegate, Delegation, Registry, School, Team, Advisor

# Register your models here.
admin.site.register(School)
admin.site.register(Country)
admin.site.register(Race)
admin.site.register(State)
admin.site.register(Delegate)
admin.site.register(Delegation)
admin.site.register(Registry)
admin.site.register(Team)
admin.site.register(Advisor)
