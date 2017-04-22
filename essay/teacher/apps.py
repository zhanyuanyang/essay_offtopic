from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models.signals import post_migrate


def do_stuff(sender, **kwargs):
    mymodel = sender.get_model('Essay')
    mymodel.objects.get()

class TeacherConfig(AppConfig):
    name = 'teacher'

    def ready(self):
        post_migrate.connect(do_stuff, sender=self)

