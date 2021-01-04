from django.contrib import admin
from .models import Event, Transactions


class TransactionsConf(admin.ModelAdmin):
    list_display = ('id', 'user', 'tr', 'status')
    
class EventConf(admin.ModelAdmin):
    list_display = ('title', 'host','id')




admin.site.register(Event,EventConf)
admin.site.register(Transactions, TransactionsConf)
# Register your models here.
