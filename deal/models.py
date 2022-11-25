from django.db import models
from unft.models import Unft
from users.models import User

class Deal(models.Model):
    unft = models.ForeignKey(Unft, on_delete = models.CASCADE, related_name="unft_deals")
    from_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="from_user_deals")
    to_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="to_user_deals")
    price = models.IntegerField(default=0)
    status = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)