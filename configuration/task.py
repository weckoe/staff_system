from celery import shared_task

from django.apps import apps
from django.db.models import F

from configuration.celery import app




@app.task
def add_salary_to_staff():
    model = apps.get_model(app_label='api', model_name='User')
    model.objects.filter(is_staff=True).update(salary_information=F('salary_information') + F('salary'))


@shared_task
def delete_salary_information_async(users_id):
    print(users_id)
    for pk in users_id:
        model = apps.get_model(app_label='api', model_name='User')
        model.objects.filter(id=pk).update(salary_information=None)
