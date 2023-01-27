from django.db.models.signals import post_save,m2m_changed,post_delete

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import *

from .helpers import get_random_alphanumeric_string

from django.conf import settings

from django.core.mail import send_mail



# https://techincent.com/how-to-delete-file-when-models-instance-is-delete-or-update-in-django/
# or
# https://djangosnippets.org/snippets/10638/
def auto_clear_files_on_delete(sender,instance,*args,**kwargs):
    print("file handler signal is running")
    # delete filtered and sized cache images
    instance.image.delete_all_created_images()
    try:
        # delete original image
        instance.image.delete(save=False)
    except:
        pass


post_delete.connect(auto_clear_files_on_delete,sender=PostMedia,dispatch_uid="unique")

