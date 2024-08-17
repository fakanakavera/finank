from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense, Receipt

from django.utils.text import slugify
from datetime import datetime
import os

# make a view that returns a test page DO NOT USE HTML FILE, MAKE THE HTML IN THE VIEW
def test(request):
    return render(request, 'test.html', {})

def receipt_upload_to(instance, filename):
    # Get the original extension of the uploaded file
    extension = filename.split('.')[-1]
    
    # Create a slugified version of the expense name
    expense_name_slug = slugify(instance.expense.description)
    
    # Get the current date and time
    current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Combine the slug, datetime, and extension to form the new filename
    new_filename = f"{expense_name_slug}_{current_datetime}.{extension}"
    
    # Return the path where the file will be saved
    return os.path.join('receipts', new_filename)

def upload_receipt(request):
    if request.method == 'POST':
        expense_id = request.POST.get('selected_expense_id')
        receipt_file = request.FILES.get('receipt')
        expense = get_object_or_404(Expense, id=expense_id)

        # Save the receipt linked to the selected expense
        Receipt.objects.create(expense=expense, image=receipt_file)

        # Redirect to a success page or back to the form
        return redirect('upload_receipt')

    # Retrieve all expenses (or a specific subset depending on your needs)
    expenses = Expense.objects.all()
    return render(request, 'upload_receipt.html', {'expenses': expenses})