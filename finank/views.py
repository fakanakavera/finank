from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense, Receipt

from datetime import datetime
from django.db.models import Q, Sum


# make a view that returns a test page DO NOT USE HTML FILE, MAKE THE HTML IN THE VIEW
def test(request):
    return render(request, 'test.html', {})

def expenses_overview(request):
    selected_month = request.GET.get('month', datetime.now().month)
    selected_year = request.GET.get('year', datetime.now().year)

    selected_month = int(selected_month)
    selected_year = int(selected_year)

    expenses = Expense.objects.filter(
        Q(date__year=selected_year, date__month=selected_month) |
        Q(is_recurring=True, date__year__lte=selected_year, date__month__lte=selected_month)
    )

    paid_expenses = []
    unpaid_expenses = []

    for expense in expenses:
        total_paid = Receipt.objects.filter(
            expense=expense,
            payment_year=selected_year,
            payment_month=selected_month
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        if total_paid >= expense.amount:
            paid_expenses.append({
                'expense': expense,
                'total_paid': total_paid,
                'receipts': Receipt.objects.filter(
                    expense=expense,
                    payment_year=selected_year,
                    payment_month=selected_month
                )
            })
        else:
            unpaid_expenses.append({
                'expense': expense,
                'total_paid': total_paid,
                'remaining': expense.amount - total_paid,
                'receipts': Receipt.objects.filter(
                    expense=expense,
                    payment_year=selected_year,
                    payment_month=selected_month
                )
            })

    context = {
        'paid_expenses': paid_expenses,
        'unpaid_expenses': unpaid_expenses,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'months': range(1, 13),
    }

    return render(request, 'expenses_overview.html', context)

def upload_receipt(request):
    current_month = datetime.now().month
    current_year = datetime.now().year

    if request.method == 'POST':
        expense_id = request.POST.get('selected_expense_id')
        receipt_file = request.FILES.get('receipt')
        expense = get_object_or_404(Expense, id=expense_id)
        
        # Determine the amount to save in the receipt
        if expense.amount == -1:
            variable_amount = request.POST.get('variable_amount')
            if not variable_amount:
                return render(request, 'upload_receipt.html', {
                    'expenses': Expense.objects.all(),
                    'error': 'Please enter the amount for the selected expense.',
                    'months': range(1, 13),  # Pass months to template
                    'current_month': current_month,
                    'current_year': current_year
                })
            receipt_amount = float(variable_amount)
        else:
            receipt_amount = expense.amount

        # Get the payment month and year from the form, or use the current values
        payment_month = int(request.POST.get('payment_month', current_month))
        payment_year = int(request.POST.get('payment_year', current_year))

        # Create the receipt object with the payment month and year
        Receipt.objects.create(
            expense=expense,
            image=receipt_file if receipt_file else None,
            amount=receipt_amount,
            payment_month=payment_month,
            payment_year=payment_year
        )

        return redirect('upload_receipt')

    expenses = Expense.objects.all()
    return render(request, 'upload_receipt.html', {
        'expenses': expenses,
        'months': range(1, 13),  # Pass months to template
        'current_month': current_month,
        'current_year': current_year
    })