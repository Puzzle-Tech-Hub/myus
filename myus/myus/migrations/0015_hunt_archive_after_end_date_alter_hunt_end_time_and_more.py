# Generated by Django 5.0.2 on 2025-01-04 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "myus",
            "0012_hunt_solution_style_puzzle_solution_url_squashed_0014_alter_puzzle_solution_url",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="hunt",
            name="archive_after_end_date",
            field=models.BooleanField(
                default=False,
                help_text="Set hunt to archive mode after end date (teams can still be created and progress, but leaderboard is frozen and all puzzles are unlocked).",
            ),
        ),
        migrations.AlterField(
            model_name="hunt",
            name="end_time",
            field=models.DateTimeField(
                blank=True,
                help_text="End date of the hunt. If <b>Archive after end date</b> is checked, hunt will be put in archive mode after this date.",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="hunt",
            name="solution_style",
            field=models.CharField(
                choices=[
                    ("VIS", "Solutions are always visible"),
                    ("HID", "Solutions are always hidden"),
                    (
                        "SOL",
                        "Solution displayed after puzzle is solved (or when hunt is in archive mode)",
                    ),
                ],
                default="HID",
                max_length=3,
            ),
        ),
    ]
