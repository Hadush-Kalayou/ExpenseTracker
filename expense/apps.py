from django.apps import AppConfig


class ExpenseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "expense"

    def ready(self):
        from .models import Category

        default_categories = [
            "Food",
            "Transport",
            "Shopping",
            "Rent",
            "Utilities",
            "Entertainment",
            "Health",
            "Education",
            "Salary",
            "Freelance",
            "Business",
            "Other",
        ]

        for name in default_categories:
            Category.objects.get_or_create(
                name=name,
                owner=None,
                is_default=True,
            )
