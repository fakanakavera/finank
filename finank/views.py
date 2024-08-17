from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense, Receipt

from datetime import datetime
from django.db.models import Sum


# make a view that returns a test page DO NOT USE HTML FILE, MAKE THE HTML IN THE VIEW
def test(request):
    return render(request, 'test.html', {})



def expenses_overview(request):
    # Get the current month and year (or get from request parameters if needed)
    selected_month = request.GET.get('month', datetime.now().month)
    selected_year = request.GET.get('year', datetime.now().year)

    # Convert to integers
    selected_month = int(selected_month)
    selected_year = int(selected_year)

    # Filter expenses for the selected month and year
    expenses = Expense.objects.filter(date__year=selected_year, date__month=selected_month)

    # Initialize lists for paid and unpaid expenses
    paid_expenses = []
    unpaid_expenses = []

    # Iterate over expenses and check if they have been fully paid
    for expense in expenses:
        # Sum up all receipts related to this expense
        total_paid = Receipt.objects.filter(expense=expense).aggregate(Sum('amount'))['amount__sum'] or 0

        if total_paid >= expense.amount:
            paid_expenses.append({
                'expense': expense,
                'total_paid': total_paid,
                'receipts': Receipt.objects.filter(expense=expense)
            })
        else:
            unpaid_expenses.append({
                'expense': expense,
                'total_paid': total_paid,
                'remaining': expense.amount - total_paid,
                'receipts': Receipt.objects.filter(expense=expense)
            })

    context = {
        'paid_expenses': paid_expenses,
        'unpaid_expenses': unpaid_expenses,
        'selected_month': selected_month,
        'selected_year': selected_year,
    }

    return render(request, 'expenses_overview.html', context)

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
        Receipt.objects.create(expense=expense, 
                               image=receipt_file if receipt_file else None, 
                               amount=receipt_amount)

        # Redirect to a success page or back to the form
        return redirect('upload_receipt')

    # Retrieve all expenses (or a specific subset depending on your needs)
    expenses = Expense.objects.all()
    return render(request, 'upload_receipt.html', {'expenses': expenses})