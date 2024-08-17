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
        
        # Determine the amount to save in the receipt
        if expense.amount == -1:
            # If the expense is variable, get the amount from the user input
            variable_amount = request.POST.get('variable_amount')
            if not variable_amount:
                # Handle the case where no amount is provided
                return render(request, 'upload_receipt.html', {
                    'expenses': Expense.objects.all(),
                    'error': 'Please enter the amount for the selected expense.'
                })
            receipt_amount = float(variable_amount)
        else:
            # If the expense is fixed, use the amount from the expense
            receipt_amount = expense.amount

        # Save the receipt with the amount
        Receipt.objects.create(expense=expense, image=receipt_file, amount=receipt_amount)

        # Redirect to a success page or back to the form
        return redirect('upload_receipt')

    # Retrieve all expenses (or a specific subset depending on your needs)
    expenses = Expense.objects.all()
    return render(request, 'upload_receipt.html', {'expenses': expenses})