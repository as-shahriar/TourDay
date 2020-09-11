from django.contrib import admin
from .models import Event, Transactions


class TransactionsConf(admin.ModelAdmin):
    list_display = ('id', 'user', 'tr', 'status')


admin.site.register(Event)
admin.site.register(Transactions, TransactionsConf)
# Register your models here.
