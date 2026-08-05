from django.db import models
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

from django.db.models import Sum

from django.core.exceptions import ValidationError


# =====================================================
# CATEGORY MODEL
# =====================================================

class Category(models.Model):

    CATEGORY_TYPE = [
        ("Income", "Income"),
        ("Expense", "Expense"),
    ]

    name = models.CharField(max_length=100)

    category_type = models.CharField(
        max_length=20,
        choices=CATEGORY_TYPE
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="categories"
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    color = models.CharField(
        max_length=20,
        default="#0d6efd"
    )

    icon = models.CharField(
        max_length=100,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):

        if self.owner:
            return f"{self.name} ({self.owner.username})"

        return f"{self.name} (System)"

# Create your models here.
# =====================================================
# BUDGET MODEL
# =====================================================

# =====================================================
# BUDGET MODEL
# =====================================================

class Budget(models.Model):

    PERIOD_CHOICES = [

        ("Daily", "Daily"),
        ("Weekly", "Weekly"),
        ("Monthly", "Monthly"),
        ("Yearly", "Yearly"),
        ("Custom", "Custom"),

    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="budgets"
    )

    name = models.CharField(
        max_length=100
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    period = models.CharField(
        max_length=20,
        choices=PERIOD_CHOICES
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    # =====================================================
    # CALCULATED PROPERTIES
    # =====================================================

    @property
    def spent_budget(self):
        """
        Total amount spent from this budget.
        """
        total = self.expenses.aggregate(
            total=Sum("amount")
        )["total"]

        return total or 0

    @property
    def remaining_budget(self):
        """
        Remaining budget after expenses.
        """
        return self.amount - self.spent_budget

    @property
    def budget_percentage(self):
        """
        Percentage of the budget that has been used.
        """
        if self.amount == 0:
            return 0

        return round(
            (self.spent_budget / self.amount) * 100,
            2
        )

    # =====================================================
# INCOME MODEL
# =====================================================

class Income(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="incomes"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )

    source = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    income_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-income_date"]

    def __str__(self):
        return self.source


    # =====================================================
# EXPENSE MODEL
# =====================================================

# =====================================================
# EXPENSE MODEL
# =====================================================

class Expense(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenses"
    )

    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        related_name="expenses"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )

    description = models.TextField()

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    expense_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-expense_date"]


    # =====================================================
    # VALIDATE EXPENSE AGAINST BUDGET
    # =====================================================

    def clean(self):

        if self.budget:

            remaining = self.budget.remaining_budget

            # Exclude this expense when editing
            if self.pk:
                remaining += self.amount

            if self.amount > remaining:

                raise ValidationError({

                    "amount":
                    "Expense exceeds the remaining budget."

                })


    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)


    def __str__(self):

        return self.description