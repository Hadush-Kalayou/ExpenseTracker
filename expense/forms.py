from django import forms
from django.db.models import Q

from .models import Category, Expense, Budget, Income


# =====================================================
# EXPENSE FORM
# =====================================================

class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense

        fields = [
            "payment_source",
            "budget",
            "category",
            "description",
            "amount",
            "expense_date",
        ]

        widgets = {
            "payment_source": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "budget": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "expense_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        if user:

            self.fields["category"].queryset = Category.objects.filter(
                Q(owner=user) |
                Q(owner__isnull=True)
            )

            self.fields["budget"].queryset = Budget.objects.filter(
                user=user,
                is_active=True
            )


# =====================================================
# CATEGORY FORM
# =====================================================

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = [
            "name",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter category name",
                }
            ),
        }


# =====================================================
# BUDGET FORM
# =====================================================

class BudgetForm(forms.ModelForm):

    class Meta:
        model = Budget

        exclude = [
            "user",
            "created_at",
            "updated_at",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter budget name",
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter budget amount",
                    "step": "0.01",
                }
            ),

            "period": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "start_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Optional description",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }


# =====================================================
# INCOME FORM
# =====================================================

# =====================================================
# INCOME FORM
# =====================================================

class IncomeForm(forms.ModelForm):

    class Meta:
        model = Income

        exclude = [
            "user",
            "category",
            "created_at",
            "updated_at",
        ]

        widgets = {
            "source": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter income source",
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter income amount",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "income_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Optional description",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        kwargs.pop("user", None)

        super().__init__(*args, **kwargs)