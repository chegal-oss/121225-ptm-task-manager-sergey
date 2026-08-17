from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0005_rename_deadline_subtask_dead_line_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="category",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
    ]
