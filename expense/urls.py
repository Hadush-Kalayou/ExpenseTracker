from django.urls import path

from . import views

app_name = "expense"

urlpatterns = [

    # =====================================================
    # CATEGORY
    # =====================================================

    path(
        "categories/",
        views.category_list,
        name="category_list"
    ),

    path(
        "categories/add/",
        views.category_create,
        name="category_add"
    ),

       path(
        "category/create/",
        views.category_create,
        name="category_create"
    ),

    path(
        "categories/<int:pk>/edit/",
        views.category_update,
        name="category_edit"
    ),

    path(
        "categories/<int:pk>/delete/",
        views.category_delete,
        name="category_delete"
    ),

    # =====================================================
    # BUDGET
    # =====================================================

    path(
        "budgets/",
        views.budget_list,
        name="budget_list"
    ),

    path(
        "budgets/add/",
        views.budget_create,
        name="budget_add"
    ),

    path(
        "budgets/<int:pk>/edit/",
        views.budget_update,
        name="budget_edit"
    ),

    path(
        "budgets/<int:pk>/delete/",
        views.budget_delete,
        name="budget_delete"
    ),

    # =====================================================
    # INCOME
    # =====================================================

    path(
        "income/",
        views.income_list,
        name="income_list"
    ),

    path(
        "income/add/",
        views.income_create,
        name="income_add"
    ),

    path(
        "income/<int:pk>/edit/",
        views.income_update,
        name="income_edit"
    ),

    path(
        "income/<int:pk>/delete/",
        views.income_delete,
        name="income_delete"
    ),

    # =====================================================
    # EXPENSE
    # =====================================================

    path(
        "expenses/",
        views.expense_list,
        name="expense_list"
    ),

    path(
        "expenses/add/",
        views.expense_create,
        name="expense_add"
    ),

    path(
        "expenses/<int:pk>/edit/",
        views.expense_update,
        name="expense_edit"
    ),

    path(
        "expenses/<int:pk>/delete/",
        views.expense_delete,
        name="expense_delete"
    ),

    # =====================================================
    # REPORTS
    # =====================================================

    path(
        "reports/",
        views.report_dashboard,
        name="reports"
    ),

   path(
    "report-dashboard/",
    views.report_dashboard,
    name="report_dashboard",
),
    path(
        "reports/export/pdf/",
        views.export_pdf,
        name="export_pdf"
    ),

    path(
        "reports/export/excel/",
        views.export_excel,
        name="export_excel"
    ),

    path(
        "reports/export/csv/",
        views.export_csv,
        name="export_csv"
    ),

    
]