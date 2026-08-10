from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db.models import Sum
from django.core.exceptions import ValidationError
# =====================================================
# CATEGORY MODEL
# =====================================================


class Category(models.Model):
    name = models.CharField(max_length=100)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="categories"
    )

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
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

    source = models.CharField(
        max_length=200
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    income_date = models.DateField()

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.source} - {self.amount}"

    # =====================================================
# EXPENSE MODEL
# =====================================================

# =====================================================
# EXPENSE MODEL
# =====================================================

# =====================================================
# EXPENSE MODEL
# =====================================================

class Expense(models.Model):

    # ==========================================
    # PAYMENT SOURCE
    # ==========================================

    PAYMENT_SOURCE = [

        ("Budget", "Budget"),

        ("Income", "Income"),

    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenses"
    )

    # Optional because Income expenses do not require a budget
    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        related_name="expenses",
        null=True,
        blank=True
    )

    payment_source = models.CharField(
        max_length=20,
        choices=PAYMENT_SOURCE,
        default="Budget"
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
   # =====================================================
# VALIDATION
# =====================================================

def clean(self):
   

    # -----------------------------------------
    # BUDGET EXPENSE
    # -----------------------------------------
    if self.payment_source == "Budget":

        # Budget is required
        if not self.budget:
            raise ValidationError({
                "budget": "Please select a budget."
            })

        # Get remaining budget
        remaining = self.budget.remaining_budget

        # When editing an existing expense,
        # add its current amount back before checking.
        if self.pk:
            remaining += self.amount

        # Expense cannot exceed remaining budget
        if self.amount > remaining:
            raise ValidationError({
                "amount": "Expense exceeds the remaining budget."
            })

    # -----------------------------------------
    # INCOME EXPENSE
    # -----------------------------------------
    elif self.payment_source == "Income":

        # Income expenses must not have a budget
        self.budget = None


# =====================================================
# SAVE
# =====================================================

def save(self, *args, **kwargs):

    self.full_clean()

    super().save(*args, **kwargs)


# =====================================================
# STRING
# =====================================================

def __str__(self):

    return f"{self.description} ({self.payment_source})"