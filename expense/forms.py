from django import forms

from .models import (
    Category,
    Budget,
    Income,
    Expense,
)
from django.db.models import Q


# =====================================================
# Base Bootstrap Form
# =====================================================

class BootstrapFormMixin:

    def apply_bootstrap(self):

        for field in self.fields.values():

            field.widget.attrs["class"] = "form-control"


# =====================================================
# Category Form
# =====================================================

class CategoryForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:

        model = Category

        fields = [

            "name",
            "category_type",
            "description",
            "color",
            "icon",
            "is_active",

        ]

        widgets = {

            "description": forms.Textarea(
                attrs={
                    "rows": 3
                }
            ),

            "color": forms.TextInput(
                attrs={
                    "type": "color"
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.apply_bootstrap()


# =====================================================
# Budget Form
# =====================================================

class BudgetForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:

        model = Budget

        exclude = [

            "user",
            "created_at",
            "updated_at",

        ]

        widgets = {

            "start_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "end_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 3
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.apply_bootstrap()


# =====================================================
# Income Form
# =====================================================

# =====================================================
# Income Form
# =====================================================

# =====================================================
# Income Form
# =====================================================

class IncomeForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:

        model = Income

        exclude = [

            "user",
            "category",
            "created_at",
            "updated_at",

        ]

        widgets = {

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
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        self.apply_bootstrap()
# =====================================================
# Expense Form
# =====================================================

class ExpenseForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:

        model = Expense

        exclude = [
            "user",
            "created_at",
            "updated_at",
        ]

        widgets = {

            "payment_source": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "expense_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        self.apply_bootstrap()

        if user:

            self.fields["budget"].queryset = Budget.objects.filter(
                user=user,
                is_active=True
            )

            self.fields["category"].queryset = Category.objects.filter(
                Q(owner=user) | Q(owner__isnull=True),
                category_type="Expense",
                is_active=True
            )

        self.fields["budget"].required = False

    def clean(self):

        cleaned_data = super().clean()

        payment_source = cleaned_data.get("payment_source")
        budget = cleaned_data.get("budget")

        if payment_source == "Budget" and not budget:

            self.add_error(
                "budget",
                "Please select a budget."
            )

        if payment_source == "Income":

            cleaned_data["budget"] = None

        return cleaned_data