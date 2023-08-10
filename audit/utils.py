from audit.models import Audit

def create_audit(instance, user):
    Audit.objects.create(
        action='CREATE',
        user=user,
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.id,
        content_object=instance
    )

def update_audit(instance, user):
    Audit.objects.create(
        action='UPDATE',
        user=user,
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.id,
        content_object=instance
    )

def delete_audit(instance, user):
    Audit.objects.create(
        action='DELETE',
        user=user,
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.id,
        content_object=instance
    )