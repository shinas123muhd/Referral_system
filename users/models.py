from django.db import models
import random
import string

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    referral_code = models.CharField(max_length=255, blank=True, null=True)
    reffered_by = models.CharField(max_length=20,blank=True,null=True)
    points = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
        super().save(*args, **kwargs)

    def generate_referral_code(self):
        letters_and_digits = string.ascii_letters + string.digits
        code = ''.join(random.choice(letters_and_digits) for i in range(10))
        return code
class Referral(models.Model):
    referring_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_by')
    timestamp = models.DateTimeField(auto_now_add=True)


