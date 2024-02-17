from django.contrib import admin
from .models import Assembly, Membership, Participation, Tag, Voting, Option, Vote

# Register your models here.
class OptionInLine(admin.TabularInline):
    model = Option
    extra = 2

class VotingAdmin(admin.ModelAdmin):
    inlines = [OptionInLine]

admin.site.register(Voting, VotingAdmin)
admin.site.register(Vote)
admin.site.register(Participation)
admin.site.register(Tag)
admin.site.register(Assembly)
admin.site.register(Membership)