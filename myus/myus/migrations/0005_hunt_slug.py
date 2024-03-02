# Generated by Django 5.0.2 on 2024-02-14 20:37

from django.db import migrations, models
from django.utils.text import slugify


def set_slug_field(apps, schema_editor):
    """ Set the new slug field on the Hunt and Puzzle models based on the object's name field """
    Hunt = apps.get_model("myus", "Hunt")
    for hunt in Hunt.objects.all():
        hunt.slug = slugify(hunt.name)
        hunt.save()

    Puzzle = apps.get_model("myus", "Puzzle")
    for puzzle in Puzzle.objects.all():
        puzzle.slug = slugify(puzzle.name)
        puzzle.save()


class Migration(migrations.Migration):

    dependencies = [
        ('myus', '0004_alter_user_first_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='hunt',
            name='slug',
            field=models.SlugField(null=True, help_text='A short, unique identifier for the hunt.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='puzzle',
            name='slug',
            field=models.SlugField(null=True, help_text='A short, unique identifier for the puzzle.'),
            preserve_default=False,
        ),
        migrations.RunPython(set_slug_field, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='hunt',
            name='slug',
            field=models.SlugField(null=False, help_text='A short, unique identifier for the hunt.')
        ),
        migrations.AlterField(
            model_name='puzzle',
            name='slug',
            field=models.SlugField(null=False, help_text='A short, unique identifier for the puzzle.')
        ),
    ]