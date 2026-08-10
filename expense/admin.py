from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import (
    Category,
    Budget,
    Income,
    Expense,
)


# =====================================================
# CATEGORY ADMIN
# =====================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "owner",
        "is_default",
        "created_at",
    )

    list_filter = (
        "is_default",
        "created_at",
    )

    search_fields = (
        "name",
        "owner__username",
    )

    ordering = (
        "name",
    )

    list_per_page = 20


# =====================================================
# BUDGET ADMIN
# =====================================================

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "user",
        "amount",
        "period",
        "start_date",
        "end_date",
        "is_active",
    )

    list_filter = (
        "period",
        "is_active",
        "start_date",
    )

    search_fields = (
        "name",
        "user__username",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20


# =====================================================
# INCOME ADMIN
# =====================================================

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):

    list_display = (
        "source",
        "user",
        
        "amount",
        "income_date",
    )

    list_filter = (
        "user",
        "income_date",
    )

    search_fields = (
        "source",
        "user__username",
    )

    ordering = (
        "-income_date",
    )

    list_per_page = 20


# =====================================================
# EXPENSE ADMIN
# =====================================================

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):

    list_display = (
        "description",
        "user",
        "category",
        "budget",
        "amount",
        "expense_date",
    )

    list_filter = (
        "expense_date",
        "category",
        "budget",
    )

    search_fields = (
        "description",
        "user__username",
    )

    ordering = (
        "-expense_date",
    )

    list_per_page = 20