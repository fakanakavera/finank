from django.db import models
from django.conf import settings
from django.utils.text import slugify
from datetime import datetime
import os

def receipt_upload_to(instance, filename):
    # Get the original extension of the uploaded file
    extension = filename.split('.')[-1]
    
    # Create a slugified version of the expense name
    expense_name_slug = slugify(instance.expense.name)
    
    # Get the current date and time
    current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Combine the slug, datetime, and extension to form the new filename
    new_filename = f"{expense_name_slug}_{current_datetime}.{extension}"
    
    # Return the path where the file will be saved
    return os.path.join('receipts', new_filename)

class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(max_length=50, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    number_of_payments = models.IntegerField(blank=True, null=True)
    payments_made = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.amount}"

class Receipt(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='receipts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=receipt_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    payment_month = models.IntegerField(default=datetime.now().month)
    payment_year = models.IntegerField(default=datetime.now().year)

    def __str__(self):
        return f"Receipt for {self.expense.category.name} on {self.uploaded_at}"

class RecurringExpenseTracker(models.Model):
    expense = models.OneToOneField(Expense, on_delete=models.CASCADE)
    next_payment_date = models.DateField()
    last_payment_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Recurring for {self.expense.category.name}"
