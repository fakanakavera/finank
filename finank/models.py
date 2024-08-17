from django.db import models
from django.conf import settings
from .views import receipt_upload_to

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
    amount = models.DecimalField(max_digits=10, decimal_places=2)
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
    image = models.ImageField(upload_to=receipt_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt for {self.expense.category.name} on {self.uploaded_at}"

class RecurringExpenseTracker(models.Model):
    expense = models.OneToOneField(Expense, on_delete=models.CASCADE)
    next_payment_date = models.DateField()
    last_payment_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Recurring for {self.expense.category.name}"
