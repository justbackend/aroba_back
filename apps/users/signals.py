from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from  . import models
from utils.utility import clear_users_perms


# Signals to clear cache api routes

@receiver(m2m_changed, sender=models.Role.actions.through)
def role_action_change(sender, instance, **kwargs):
    users = instance.users.all()
    clear_users_perms(users)


@receiver(m2m_changed, sender=models.Action.apis.through)
def action_apis_change(sender, instance, **kwargs):
    users = instance.users.all()
    clear_users_perms(users)


@receiver(m2m_changed, sender=models.User.actions.through)
def user_action_change(sender, instance, **kwargs):
    clear_users_perms((instance,))


@receiver(m2m_changed, sender=models.User.roles.through)
def user_action_change(sender, instance, action, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        related_actions = models.Action.objects.filter(roles__in=instance.roles.all()).distinct()
        instance.actions.set(related_actions)

        clear_users_perms((instance,))


@receiver(pre_save, sender=models.User)
def cleared_users(sender, instance, **kwargs):
    if instance.pk:
        clear_user_profile_data(users=(instance.id,))


@receiver(pre_save, sender=models.APIRoute)
def clear_user_profile_data(sender, instance, **kwargs):
    if instance.pk:
        users = models.User.objects.filter(actions__apis=instance)
        clear_users_perms(users)

