# Generated by Django 4.1.5 on 2023-06-20 04:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_comments_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_link', models.URLField()),
                ('title', models.CharField(max_length=200)),
                ('video_file', models.FileField(upload_to='videos/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('duration', models.CharField(blank=True, default='00:00:00', max_length=8)),
                ('audio_file', models.FileField(blank=True, null=True, upload_to='audios')),
                ('audio_fileName', models.CharField(blank=True, max_length=200)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
            ],
        ),
    ]
