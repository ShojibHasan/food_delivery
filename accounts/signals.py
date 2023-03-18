from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import User,UserProfile


@receiver(post_save,sender=User)
def post_save_create_profile_receiver(sender,instance,created,**kwargs):
    print("This is created: ",created)
    if created:
        UserProfile.objects.create(user=instance)
        print("User Profile Created")
    else:
        try:
            print("Else")
            profile = UserProfile.objects.get(user = instance)
            profile.save()
        
        except:
            UserProfile.objects.create(user=instance)
            print("Profile Not exist, but create a new one")
            
@receiver(pre_save,sender=User)
def pre_save_create_profile_reciver(sender,instance,**kwargs):
    print(instance.username,"This user is being saved")