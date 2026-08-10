from django.shortcuts import render
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.db.models import Q

from .models import (
    Category,
    Budget,
    Income,
    Expense,
)

from .forms import (
    CategoryForm,
    BudgetForm,
    IncomeForm,
    ExpenseForm,
)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect




# Create your views here.



@login_required
def category_list(request):
    search = request.GET.get("search", "").strip()

    # Default categories
    default_categories = Category.objects.filter(
        is_default=True
    ).order_by("name")

    # User-created categories
    user_categories = Category.objects.filter(
        owner=request.user,
        is_default=False
    ).order_by("name")

    # Search
    if search:
        default_categories = default_categories.filter(
            name__icontains=search
        )

        user_categories = user_categories.filter(
            name__icontains=search
        )

    context = {
        "default_categories": default_categories,
        "user_categories": user_categories,
        "search": search,
    }

    return render(
        request,
        "expense/category/category_list.html",
        context
    )
@login_required
def category_create(request):

    if request.method == "POST":

        form = CategoryForm(request.POST)

        if form.is_valid():

            category = form.save(commit=False)

            category.owner = request.user
            category.is_default = False

            category.save()

            return redirect("expense:category_list")

    else:

        form = CategoryForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "expense/category/category_form.html",
        context
    )
@login_required
def category_update(request, pk):

    category = get_object_or_404(

        Category,

        pk=pk,

        owner=request.user,

    )

    if request.method == "POST":

        form = CategoryForm(

            request.POST,

            instance=category,

        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Category updated successfully."
            )

            return redirect("expense:category_list")

    else:

        form = CategoryForm(
            instance=category
        )

    return render(

        request,

        "expense/category/category_form.html",

        {

            "form": form,

            "title": "Edit Category",

        }

    )


@login_required
def category_delete(request, pk):

    category = get_object_or_404(

        Category,

        pk=pk,

        owner=request.user,

    )

    if request.method == "POST":

        category.delete()

        messages.success(

            request,

            "Category deleted successfully."

        )

        return redirect(
            "expense:category_list"
        )

    return render(

        request,

        "expense/category/category_confirm_delete.html",

        {

            "category": category,

        }

    )


# =====================================================
# BUDGET LIST
# =====================================================

@login_required
def budget_list(request):

    search = request.GET.get("search")

    budgets = Budget.objects.filter(
        user=request.user
    )

    if search:

        budgets = budgets.filter(
            name__icontains=search
        )

    context = {

        "budgets": budgets,
        "search": search,

    }

    return render(
        request,
        "expense/budget/budget_list.html",
        context
    )


# =====================================================
# ADD BUDGET
# =====================================================

@login_required
def budget_create(request):

    if request.method == "POST":

        form = BudgetForm(request.POST)

        if form.is_valid():

            budget = form.save(commit=False)

            budget.user = request.user

            budget.save()

            messages.success(
                request,
                "Budget created successfully."
            )

            return redirect("expense:budget_list")

    else:

        form = BudgetForm()

    return render(

        request,

        "expense/budget/budget_form.html",

        {

            "form": form,

            "title": "Add Budget",

        }

    )


# =====================================================
# EDIT BUDGET
# =====================================================

@login_required
def budget_update(request, pk):

    budget = get_object_or_404(

        Budget,

        pk=pk,

        user=request.user,

    )

    if request.method == "POST":

        form = BudgetForm(

            request.POST,

            instance=budget,

        )

        if form.is_valid():

            form.save()

            messages.success(

                request,

                "Budget updated successfully."

            )

            return redirect("expense:budget_list")

    else:

        form = BudgetForm(
            instance=budget
        )

    return render(

        request,

        "expense/budget/budget_form.html",

        {

            "form": form,

            "title": "Edit Budget",

        }

    )


# =====================================================
# DELETE BUDGET
# =====================================================

@login_required
def budget_delete(request, pk):

    budget = get_object_or_404(

        Budget,

        pk=pk,

        user=request.user,

    )

    if request.method == "POST":

        budget.delete()

        messages.success(

            request,

            "Budget deleted successfully."

        )

        return redirect(
            "expense:budget_list"
        )

    return render(

        request,

        "expense/budget/budget_confirm_delete.html",

        {

            "budget": budget,

        }

    )


# =====================================================
# INCOME LIST
# =====================================================

@login_required
def income_list(request):

    search = request.GET.get("search")

    incomes = Income.objects.filter(
        user=request.user
    )

    if search:

        incomes = incomes.filter(

            Q(source__icontains=search) |
            Q(description__icontains=search)

        )

    context = {

        "incomes": incomes,

        "search": search,

    }

    return render(

        request,

        "expense/income/income_list.html",

        context

    )


# =====================================================
# ADD INCOME
# =====================================================

@login_required
def income_create(request):

    if request.method == "POST":

        form = IncomeForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():

            income = form.save(commit=False)

            income.user = request.user

            income.save()

            messages.success(
                request,
                "Income added successfully."
            )

            return redirect(
                "expense:income_list"
            )

    else:

        form = IncomeForm(
            user=request.user
        )

    return render(
        request,
        "expense/income/income_form.html",
        {
            "form": form,
            "title": "Add Income",
        }
    )
# =====================================================
# EDIT INCOME
# =====================================================

@login_required
def income_update(request, pk):

    income = get_object_or_404(
        Income,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":

        form = IncomeForm(
            request.POST,
            instance=income,
            user=request.user,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Income updated successfully."
            )

            return redirect(
                "expense:income_list"
            )

    else:

        form = IncomeForm(
            instance=income,
            user=request.user,
        )

    return render(
        request,
        "expense/income/income_form.html",
        {
            "form": form,
            "title": "Edit Income",
        }
    )

# =====================================================
# DELETE INCOME
# =====================================================

@login_required
def income_delete(request, pk):

    income = get_object_or_404(

        Income,

        pk=pk,

        user=request.user,

    )

    if request.method == "POST":

        income.delete()

        messages.success(

            request,

            "Income deleted successfully."

        )

        return redirect("expense:income_list")

    return render(

        request,

        "expense/income/income_confirm_delete.html",

        {

            "income": income,

        }

    )

# =====================================================
# EXPENSE LIST
# =====================================================

@login_required
def expense_list(request):

    search = request.GET.get("search")

    expenses = Expense.objects.filter(
        user=request.user
    )

    if search:

        expenses = expenses.filter(

            Q(description__icontains=search) |
            Q(category__name__icontains=search)

        )

    context = {

        "expenses": expenses,

        "search": search,

    }

    return render(

        request,

        "expense/expense/expense_list.html",

        context

    )

# =====================================================
# ADD EXPENSE
# =====================================================




@login_required
def expense_create(request):

    if request.method == "POST":

        form = ExpenseForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():

            expense = form.save(commit=False)

            expense.user = request.user

            expense.save()

            return redirect("expense:expense_list")

    else:

        form = ExpenseForm(
            user=request.user
        )

    context = {
        "form": form,
    }

    return render(
        request,
        "expense/expense/expense_form.html",
        context
    )


# =====================================================
# EDIT EXPENSE
# =====================================================

@login_required
def expense_update(request, pk):

    expense = get_object_or_404(
        Expense,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        form = ExpenseForm(
            request.POST,
            instance=expense,
            user=request.user
        )

        if form.is_valid():

            expense = form.save(commit=False)

            expense.user = request.user
            expense.save()

            return redirect("expense:expense_list")

    else:

        form = ExpenseForm(
            instance=expense,
            user=request.user
        )

    context = {
        "form": form,
        "expense": expense,
    }

    return render(
        request,
        "expense/expense/expense_form.html",
        context
    )

# =====================================================
# DELETE EXPENSE
# =====================================================

@login_required
def expense_delete(request, pk):

    expense = get_object_or_404(

        Expense,

        pk=pk,

        user=request.user

    )

    if request.method == "POST":

        expense.delete()

        messages.success(

            request,

            "Expense deleted successfully."

        )

        return redirect("expense:expense_list")

    return render(

        request,

        "expense/expense/expense_confirm_delete.html",

        {

            "expense": expense,

        }

    )



@login_required
def report_dashboard(request):
    return render(request, "expense/report_dashboard.html")


@login_required
def export_pdf(request):
    return HttpResponse("PDF export will be implemented soon.")




# =====================================================
# REPORTS
# =====================================================

@login_required
def report_dashboard(request):
    return render(request, "expense/report_dashboard.html")


# =====================================================
# EXPORTS
# =====================================================

@login_required
def export_csv(request):
    return HttpResponse(
        "CSV Export Coming Soon",
        content_type="text/plain"
    )


@login_required
def export_excel(request):
    return HttpResponse(
        "Excel Export Coming Soon",
        content_type="text/plain"
    )


@login_required
def export_pdf(request):
    return HttpResponse(
        "PDF Export Coming Soon",
        content_type="text/plain"
    )


# =====================================================
# CHARTS
# =====================================================

@login_required
def expense_chart(request):
    return render(request, "expense/expense_chart.html")


@login_required
def income_chart(request):
    return render(request, "expense/income_chart.html")


@login_required
def budget_chart(request):
    return render(request, "expense/budget_chart.html")


# =====================================================
# SEARCH
# =====================================================

@login_required
def search(request):
    return render(request, "expense/search_results.html")


# =====================================================
# FILTERS
# =====================================================

@login_required
def filter_expenses(request):
    return render(request, "expense/filter_expenses.html")


@login_required
def filter_income(request):
    return render(request, "expense/filter_income.html")