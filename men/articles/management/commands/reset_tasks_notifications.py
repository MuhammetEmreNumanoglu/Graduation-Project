"""
Management command: reset_tasks_notifications

Tüm Task ve Notification kayıtlarını siler.
Kullanım: python manage.py reset_tasks_notifications
"""
from django.core.management.base import BaseCommand
from articles.models import Task, Notification


class Command(BaseCommand):
    help = 'Tüm Task ve Notification kayıtlarını siler (temiz başlangıç için).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--yes',
            action='store_true',
            help='Onay istemeden sil (CI/CD için).',
        )

    def handle(self, *args, **options):
        task_count = Task.objects.count()
        notif_count = Notification.objects.count()

        self.stdout.write(
            self.style.WARNING(
                f'\n[WARN] Bu islem kalici ve geri alinamaz!\n'
                f'   Silinecek: {task_count} gorev, {notif_count} bildirim.\n'
            )
        )

        if not options['yes']:
            confirm = input('Devam etmek istiyor musunuz? [evet/hayir]: ').strip().lower()
            if confirm not in ('evet', 'yes', 'e', 'y'):
                self.stdout.write(self.style.NOTICE('Islem iptal edildi.'))
                return

        Task.objects.all().delete()
        Notification.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                f'[OK] {task_count} gorev ve {notif_count} bildirim basariyla silindi.'
            )
        )
