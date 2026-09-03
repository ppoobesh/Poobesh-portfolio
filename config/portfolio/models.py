from django.db import models
from pathlib import Path
from django.core.exceptions import ValidationError
# Create your models here.
from django.core.validators import MinValueValidator, MaxValueValidator


def validate_image_size(file):
    max_size = 5 * 1024 * 1024  # 5 MB

    if file.size > max_size:
        raise ValidationError(
            "Image file size cannot exceed 5 MB."
        )


def validate_resume_file(file):
    extension = Path(file.name).suffix.lower()

    if extension != ".pdf":
        raise ValidationError(
            "Resume must be uploaded as a PDF file."
        )

    max_size = 10 * 1024 * 1024  # 10 MB

    if file.size > max_size:
        raise ValidationError(
            "Resume file size cannot exceed 10 MB."
        )
        

class Profile(models.Model):
    full_name = models.CharField(max_length=150)
    professional_title = models.CharField(max_length=200)
    short_intro = models.TextField(blank=True)
    professional_summary = models.TextField(blank=True)
    
    profile_image = models.ImageField(upload_to= 'profile/',
                                      blank=True,null=True,
                                      validators = [validate_image_size],)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50,blank=True)
    location = models.CharField(max_length=200,blank=True)
    is_active = models.BooleanField(default= True)
    updated_at = models.DateTimeField(auto_now=True)    
    def __str__(self):
        return self.full_name
    
class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('github', "GitHub"),
        ('linkedin', "LinkedIn"),
        ('website', "Website"),
    ]
    platform = models.CharField(max_length=100, choices= PLATFORM_CHOICES)
    display_name= models.CharField(max_length=100,blank=True)
    url=models.URLField(max_length=1000)
    icon = models.CharField(max_length=100,blank=True,
                            help_text='Optional icon class such as bi bi-github')
    display_order = models.PositiveBigIntegerField(default=0)
    is_active = models.BooleanField(default= True)
    def __str__(self):
        return self.display_name or self.get_platform_display()
    
    class Meta:
        ordering = ['display_order','id']
    
class Experience(models.Model):
    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200,blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True,null=True)
    currently_working = models.BooleanField(default=False)
    description = models.TextField()
    display_order = models.PositiveBigIntegerField(default=0)
    is_active = models.BooleanField(default= True)
    def __str__(self):
        return f'{self.job_title} - {self.company_name}'
    class Meta:
        ordering = ['display_order', '-start_date']
        
class Project(models.Model):
    title= models.CharField(max_length=200)
    short_description = models.TextField()
    full_description = models.TextField(blank=True)
    technologies = models.CharField(max_length=1000,
                                    blank=True,
                                    help_text = 'Example: Python,Django, OracleDB etc.,')
    image = models.ImageField(upload_to='projects/',
                              blank=True,null=True,
                              validators=[validate_image_size],)
    github_url = models.URLField(max_length=1000,blank=True)

    demo_url = models.URLField(max_length=1000, blank=True)
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['display_order', '-created_at']
        
class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("programming", "Programming"),
        ("web", "Web Development"),
        ("database", "Database"),
        ("ai_ml", "AI / Machine Learning"),
        ("embedded", "Embedded Systems"),
        ("tools", "Tools"),
        ("other", "Other"),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    proficiency = models.PositiveIntegerField(default=80,validators=[MinValueValidator(0),MaxValueValidator(100)],
                                              help_text="Enter value between 0 and 100")
    icon = models.CharField(max_length=100,blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['category', 'display_order', 'name']
        
class Education(models.Model):
    institution = models.CharField(max_length=250)
    degree = models.CharField(max_length=250)
    field_of_study = models.CharField(max_length=250,blank=True)
    institution_url = models.URLField(max_length=1000,blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True,null=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.degree} - {self.institution}"

    class Meta:
        ordering = ["display_order", "-start_date"]
        
class Resume(models.Model):
    title = models.CharField(max_length=150, default="Resume")   
    resume_file = models.FileField(upload_to = 'resume/',
                                    validators=[validate_resume_file],)
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-uploaded_at"]
    
class ContactMessage(models.Model):
    sender_name = models.CharField(max_length=200)
    sender_email = models.EmailField()
    subject = models.CharField(max_length=300,blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    telegram_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender_name} - {self.subject or 'No Subject'}"

    class Meta:
        ordering = ["-created_at"]