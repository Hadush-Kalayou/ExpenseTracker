
from django.db import migrations


def create_default_categories(apps, schema_editor):

    Category = apps.get_model("expense", "Category")

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


def remove_default_categories(apps, schema_editor):

    Category = apps.get_model("expense", "Category")

    Category.objects.filter(
        owner=None,
        is_default=True,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        (
            "expense",
            "0004_alter_income_options_remove_income_category_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(
            create_default_categories,
            remove_default_categories,
        ),
    ]