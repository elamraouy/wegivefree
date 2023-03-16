from django.db import models
from django.contrib.auth.models import User


DOMAINE_CHOICE = (
    ('Vêtements', 'Vêtements'),
    ('Aides budgétaires', 'Aides budgétaires'),
    ('Apprentissage des langues', 'Apprentissage des langues'),
    ('Cours en photos', 'Cours en photos'),
    ('Education et enseigement', 'Education et enseigement'),
    ('Services sociaux', 'Services sociaux'),
    ('Services medicaux', 'Services medicaux')
)
CITIES = (
    ('Safi', 'Safi'), ('Essaouira', 'Essaouira'),
    ('Rabat', 'Rabat'),
    ('Agadir', 'Agadir'),
    ('Casablanca', 'Casablanca'),
    ('Marrakech', 'Marrakech'),
    ('Beni mellal', 'Beni mellal'),
    ('Oujda', 'Oujda'),
    ('Asilah', 'Asilah'),
    ('Tanger', 'Tanger'),
    ('Layoune', 'Layoune'),
)


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=55, blank=True, default='')
    user_image = models.CharField(max_length=256, blank=True, null=True)


class Mygifts(BaseModel):
    gived_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    domaine = models.CharField(max_length=55, choices=DOMAINE_CHOICE)
    city = models.CharField(max_length=55, choices=CITIES, blank=True, default='')
    title = models.CharField(max_length=250)
    body = models.TextField(max_length=2500)
    image = models.ImageField(upload_to='', blank=True, null=True)
    user_name = models.CharField(max_length=80, default='')
    user_image = models.CharField(max_length=256, blank=True, null=True)
    date_add = models.DateTimeField(auto_now=True)
    is_given = models.CharField(max_length=3, default='no', blank=True)

    class Meta:
        ordering = ['-date_add']

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class GiftRequest(BaseModel):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    gift = models.ForeignKey(Mygifts, on_delete=models.CASCADE)
    owner = models.CharField(max_length=250, default='', blank=True, null=True)
    user_name = models.CharField(max_length=250, default='', blank=True, null=True)
    user_city = models.CharField(max_length=55, choices=CITIES, blank=True, null=True, default='')
    user_message = models.TextField(max_length=1000, default='', null=True, blank=True)
    user_email = models.CharField(max_length=250, default='', blank=True, null=True)
    user_phone = models.CharField(max_length=250, blank=True, null=True, default='')
    date_add = models.DateTimeField(auto_now=True)
    stats = models.CharField(max_length=10, default='waiting', blank=True)

    class Meta:
        ordering = ['-date_add']


class Conversation(BaseModel):
    gift = models.ForeignKey(Mygifts, default='', on_delete=models.CASCADE)
    request = models.ForeignKey(GiftRequest, default='', null=True, on_delete=models.CASCADE)
    c_host = models.ForeignKey(User, null=True, related_name='c_host', on_delete=models.CASCADE)
    c_guest = models.ForeignKey(User, null=True, related_name='c_guest', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    date_start = models.DateTimeField(auto_now=True)
    date_close = models.DateTimeField(default=None, null=True, blank=True)

    class Meta:
        ordering = ['-date_start']


class Messages(BaseModel):
    conversation = models.ForeignKey(Conversation, default='', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, null=True, related_name='message_sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, null=True, related_name='message_receiver', on_delete=models.CASCADE)
    message = models.TextField(max_length=1000, default='', null=True, blank=True)
    date_send = models.DateTimeField(auto_now=True)
    date_read = models.DateTimeField(default=None, null=True, blank=True)
    is_seen = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['date_send']

    def __str__(self):
        return self.conversation


class Notifictaion(BaseModel):
    sender = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='receiver')
    target = models.IntegerField(max_length=55, null=True, blank=True)
    type = models.CharField(max_length=55, blank=True, default='notice')
    level = models.CharField(max_length=55, blank=True, default='info')
    verb = models.TextField(max_length=500)
    unread = models.BooleanField(default=True)
    absolute_url = models.CharField(max_length=250, blank=True, null=True)
    date_send = models.DateTimeField(auto_now=True)
