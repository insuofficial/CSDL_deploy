from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

import datetime


############################
#           Main           #
############################
class Main(models.Model):
    introduction = RichTextUploadingField()

    def __str__(self):
        return 'main'

class Main_image(models.Model):
    image_url = models.URLField(max_length=400, blank=True, null=True)
    image = models.ImageField(upload_to='main_images/', default='homepage/img/no-image-icon.png')

    def __str__(self):
        return '[{}] Main-image'.format(self.pk)

#############################
#           People          #
#############################
class Member(models.Model):
    positions = (('professor', 'professor'), ('member-MS', 'member-MS'), ('member-PHD', 'member-PHD'),
                 ('member-INTERN', 'member-INTERN'), ('alumni-MS', 'alumni-MS'), ('alumni-PHD', 'alumni-PHD'))
    position = models.CharField(max_length=16, choices=positions, default='member-MS')
    position_num = models.IntegerField(default=0)
    name_en = models.CharField(max_length=32, primary_key=True)
    name_ko = models.CharField(max_length=32)
    course = models.CharField(max_length=64, blank=True, null=True)
    research = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(max_length=32)
    tel = models.CharField(max_length=32, blank=True, null=True)
    office = models.CharField(max_length=128, blank=True, null=True)
    affiliation = models.CharField(max_length=64, blank=True, null=True)
    image_url = models.URLField(max_length=400, blank=True, null=True)
    image = models.ImageField(upload_to='member_images/', default='homepage/img/no-image-icon.png')
    detail = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return '[{}] {}'.format(self.position, self.name_ko)



#################################
#           Reasearch           #
#################################
class ResearchArea(models.Model):
    research_area = models.CharField(max_length=15, primary_key=True)

    def __str__(self):
        return '{}'.format(self.research_area)

class Research(models.Model):
    research_area = models.ForeignKey(ResearchArea, on_delete=models.CASCADE)
    research_name = models.CharField(max_length=128, primary_key=True)
    research_detail = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return '[{}] {}'.format(self.research_area, self.research_name)

class Project(models.Model):
    project = models.CharField(max_length=128, primary_key=True)
    institute = models.CharField(max_length=64, blank=True, null=True)
    business = models.CharField(max_length=64, blank=True, null=True)
    term_start = models.DateField(blank=True, null=True)
    term_end = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.project)


####################################
#           Publication            #
####################################
class Journal(models.Model):
    current_year = datetime.date.today().year
    year_choices = [(r, r) for r in range(2009, current_year + 1)]

    submitted = models.BooleanField(default=False)
    year = models.IntegerField(choices=year_choices, default=current_year)
    summary = models.CharField(max_length=144)
    journal = models.CharField(max_length=255, primary_key=True)
    detail = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return '[{}] {}'.format(self.year, self.journal)

class Conference(models.Model):
    conference = RichTextUploadingField()

    def __str__(self):
        return 'Conference'

class Patent(models.Model):
    current_year = datetime.date.today().year
    year_choices = [(r, r) for r in range(2008, current_year + 1)]
    location_choices = [('International Patent', 'International Patent'), ('Korean Patent', 'Korean Patent')]

    location = models.CharField(choices=location_choices, default='International Patent', max_length=128)
    year = models.IntegerField(choices=year_choices, default=current_year)
    patent = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return '[{}] {}'.format(self.location, self.year)

#############################
#           Board           #
#############################
class Notice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=144, primary_key=True)
    content = RichTextUploadingField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return '[{}]-{}'.format(self.user.username, self.title)


class Seminar(models.Model):
    seminar = models.CharField(max_length=255, primary_key=True)
    lecturer = models.CharField(max_length=64)
    institute = models.CharField(max_length=64, blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return '[{}] {}'.format(self.date, self.seminar)

class Album(models.Model):
    title = models.CharField(max_length=128, primary_key=True)
    image_url = models.URLField(max_length=400, blank=True, null=True)
    thumbnail = models.ImageField(upload_to='Album/',  default='homepage/img/no-image-icon.png')
    detail = RichTextUploadingField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return '[{}] {}'.format(self.date, self.title)



################################
#           contact            #
################################
class Contact(models.Model):
    tel_professor_en = models.CharField(max_length=32, blank=True, null=True)
    tel_lab_en = models.CharField(max_length=32, blank=True, null=True)
    tel_professor_ko = models.CharField(max_length=32, blank=True, null=True)
    tel_lab_ko = models.CharField(max_length=32, blank=True, null=True)
    address_en = models.CharField(max_length=128, blank=True, null=True)
    address_professor_en = models.CharField(max_length=64, blank=True, null=True)
    address_lab_en = models.CharField(max_length=64, blank=True, null=True)
    address_ko = models.CharField(max_length=128, blank=True, null=True)
    address_professor_ko = models.CharField(max_length=64, blank=True, null=True)
    address_lab_ko = models.CharField(max_length=64, blank=True, null=True)
    email_professor = models.EmailField(max_length=32, blank=True, null=True)

    location = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.address_ko)