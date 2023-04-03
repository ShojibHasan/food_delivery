from django.db import models
from accounts.models import User,UserProfile
from accounts.utils import send_notification
# Create your models here.


class Restaurant(models.Model):
    user = models.OneToOneField(User, related_name='user',on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='user_profile',on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=100)
    restaurant_license = models.ImageField(upload_to='restaurant/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.restaurant_name
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orginal = Restaurant.objects.get(pk=self.pk)
            if orginal.is_approved != self.is_approved:
                email_subject = "Congratulation! Your restaurant approve"
                email_template = "accounts/emails/admin_approve.html"
                context={
                    'user': self.user,
                    'is_approved':self.is_approved
                }
                send_notification(email_subject,email_template,context)
                ...
            else:
                email_subject = "We are sorry! You are not eligible now. "
                email_template = "accounts/emails/admin_approve.html"
                context={
                    'user': self.user,
                    'is_approved':self.is_approved
                }
                send_notification(email_subject,email_template,context)
        return super(Restaurant,self).save(*args, **kwargs)