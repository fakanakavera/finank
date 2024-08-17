from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense, Receipt



# make a view that returns a test page DO NOT USE HTML FILE, MAKE THE HTML IN THE VIEW
def test(request):
    return render(request, 'test.html', {})

def upload_receipt(request):
    if request.method == 'POST':
        expense_id = request.POST.get('selected_expense_id')
        receipt_file = request.FILES.get('receipt')
        expense = get_object_or_404(Expense, id=expense_id)
        
        # Check if the expense amount is -1 (variable)
        if expense.amount == -1:
            variable_amount = request.POST.get('variable_amount')
            if variable_amount:
                expense.amount = float(variable_amount)
                expense.save()

        # Save the receipt linked to the selected expense
        Receipt.objects.create(expense=expense, image=receipt_file)

        # Redirect to a success page or back to the form
        return redirect('upload_receipt')

    # Retrieve all expenses (or a specific subset depending on your needs)
    expenses = Expense.objects.all()
    return render(request, 'upload_receipt.html', {'expenses': expenses})