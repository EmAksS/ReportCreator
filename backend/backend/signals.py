from django.db.models.signals import post_save
from django.dispatch import receiver
from models.company import CompanyAbstract
from models.user import User

@receiver(post_save, sender=CompanyAbstract)
def create_company_superuser(sender, instance, created, **kwargs):
    if created:
        # В реальном коде пароль должен генерироваться и отправляться по email
        superuser = User.objects.create(
            username=f'super_{instance.name.lower()}',
            company=instance,
            is_superuser_of_company=True,
            is_staff=True  # если нужно доступ к админке
        )
        superuser.set_password('admin')
        superuser.save()