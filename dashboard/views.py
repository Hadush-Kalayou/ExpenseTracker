from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from expense.models import Budget, Income, Expense
from expense.models import Category


# ==========================================
# USER DASHBOARD
# ==========================================

@login_required
def user_dashboard(request):

    if request.user.is_staff:
        return redirect("admin_dashboard")

    budgets = Budget.objects.filter(
        user=request.user
    )

    incomes = Income.objects.filter(
        user=request.user
    )

    expenses = Expense.objects.filter(
        user=request.user
    )

    total_budget = budgets.aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_income = incomes.aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_expense = expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0

    # Budget Remaining
    remaining_budget = total_budget - total_expense

    # Income Remaining
    remaining_income = total_income - total_expense

    # Current Balance
    current_balance = remaining_budget + remaining_income

    recent_expenses = expenses.order_by(
        "-expense_date"
    )[:5]

    recent_incomes = incomes.order_by(
        "-income_date"
    )[:5]

    context = {

        "total_budget": total_budget,

        "total_income": total_income,

        "total_expense": total_expense,

        "remaining_budget": remaining_budget,

        "remaining_income": remaining_income,

        "current_balance": current_balance,

        "recent_expenses": recent_expenses,

        "recent_incomes": recent_incomes,

    }

    return render(
        request,
        "dashboard/user/dashboard.html",
        context
    )


# ==========================================
# ADMIN DASHBOARD
# ==========================================

@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect("user_dashboard")

    from django.contrib.auth import get_user_model

    User = get_user_model()

    context = {

        "total_users": User.objects.count(),

        "active_users": User.objects.filter(
            is_active=True
        ).count(),

        "staff_users": User.objects.filter(
            is_staff=True
        ).count(),

        "total_categories": Category.objects.count(),

        "total_budgets": Budget.objects.count(),

        "total_incomes": Income.objects.count(),

        "total_expenses": Expense.objects.count(),

        "recent_users": User.objects.order_by(
            "-date_joined"
        )[:5],

    }

    return render(
        request,
        "dashboard/admin/dashboard.html",
        context
    )