from django.contrib import admin
from .models import Category, Expense, Receipt, RecurringExpenseTracker

admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(Receipt)
admin.site.register(RecurringExpenseTracker)
