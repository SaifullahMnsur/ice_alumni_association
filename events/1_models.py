import os
from django.db import models
from django.core.validators import RegexValidator
from tinymce.models import HTMLField
from django.core.exceptions import ValidationError
from django.utils.text import slugify

def event_media_upload_to(instance, filename):
    """Generate file path for the event media file using event_id."""
    
    file_extension = os.path.splitext(filename)[1]
    return os.path.join('event_media', instance.event_id + file_extension)

class Event(models.Model):
    event_id = models.SlugField(
        max_length=50,
        unique=True,
        primary_key=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9-]+$',
                message="Event ID can only contain letters, numbers, and hyphens.",
            )
        ],
        verbose_name="Event ID"
    )
    title = models.CharField(max_length=200, verbose_name="Event Title")
    description = HTMLField(help_text="Rich HTML content for the event description.")
    
    start_time = models.DateTimeField(help_text="The start time of the event.")
    end_time = models.DateTimeField(help_text="The end time of the event.")
    location = models.CharField(max_length=255, blank=True, help_text="Location where the event will take place.")
    status = models.CharField(
        max_length=20,
        choices=[
            ('upcoming', 'Upcoming'),
            ('ongoing', 'Ongoing'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='upcoming',
        help_text="The current status of the event."
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="The time when the event was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The last time the event was updated.")

    # Media file field
    media_file = models.FileField(
        upload_to=event_media_upload_to, null=True, blank=True, 
        help_text="Upload an image, gif, or video for the event."
    )
    
    amount_per_person = models.PositiveIntegerField(default=0, help_text="The amount per person for the event.")
    amount_per_adult_guest = models.PositiveIntegerField(default=0, help_text="The amount per person for the event.")
    amount_per_child_guest = models.PositiveIntegerField(default=0, help_text="The amount per person for the event.")

    def rename_media_files(self, old_event_id):
        """Rename the media file to the new event ID if applicable."""
        if self.media_file:
            old_media_path = self.media_file.path
            # Check if the old event ID is part of the filename
            if old_event_id in old_media_path:
                new_file_name = old_media_path.replace(old_event_id, self.event_id)
                new_media_path = os.path.join(os.path.dirname(old_media_path), os.path.basename(new_file_name))
                
                # Rename the file on the filesystem
                os.rename(old_media_path, new_media_path)
                
                # Update the media file field with the new path
                self.media_file.name = os.path.relpath(new_media_path, start=os.path.dirname(self.media_file.storage.location))

    def save(self, *args, **kwargs):
        """Override save to handle renaming the event and its media file."""
        if not self.event_id:
            self.event_id = slugify(self.title)  # Ensure event_id is created if not set
        
        # If the event_id is changed, rename the media file associated with the event
        if self.pk:  # Check if this is an update (not a new instance)
            old_event = Event.objects.get(pk=self.pk)
            old_event_id = old_event.event_id
            if old_event_id != self.event_id:
                # Rename the media files
                self.rename_media_files(old_event_id)
        
        # Save the event object
        super().save(*args, **kwargs)
        
    def clean(self):
        # Validate file type (image, gif, video)
        if self.media_file:
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi', '.webm']
            file_extension = os.path.splitext(self.media_file.name)[1].lower()
            if file_extension not in valid_extensions:
                raise ValidationError(f"Invalid file format. Allowed formats: {', '.join(valid_extensions)}")

    def __str__(self):
        return self.title


from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
import os
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

def transaction_upload_to(instance, filename):
    """Generate file path for the transaction document using student_id."""
    file_extension = os.path.splitext(filename)[1]
    return os.path.join('transactions_documents', instance.student_id + file_extension)

def profile_picture_upload_to(instance, filename):
    """Generate file path for the profile picture using student_id."""
    file_extension = os.path.splitext(filename)[1]
    return os.path.join('profile_picture', instance.student_id + file_extension)

def compress_image(image):
    """
    Compress the uploaded image before saving.
    """
    # Open the image file using Pillow
    img = Image.open(image)
    
    # # Perform the compression: reduce the quality to 85%
    # img = img.convert('RGB')  # Ensure the image is in RGB mode (useful for PNG to JPEG conversion)
    
    # Get original dimensions
    original_width, original_height = img.size
    
    target_height = 900
    # Calculate new width maintaining the aspect ratio
    target_width = int((target_height / original_height) * original_width)
    
    # Resize image with the new width and height
    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # Save the image to a BytesIO object
    img_io = BytesIO()
    img.save(img_io, format='JPEG', quality=50)
    img_io.seek(0)

    # Create an InMemoryUploadedFile to replace the original image
    return InMemoryUploadedFile(img_io, None, image.name, 'image/jpeg', img_io.tell(), None)

class Registration(models.Model):
    student_id = models.CharField(max_length=50, unique=True, blank=False)
    full_name = models.CharField(max_length=255, blank=False)
    date_of_birth = models.DateField(blank=False)
    batch = models.CharField(max_length=50, blank=False)
    session = models.CharField(max_length=50, blank=False)
    email = models.EmailField(blank=False)
    contact_number = models.CharField(max_length=15, blank=False)
    whatsapp_number = models.CharField(max_length=15, blank=False)
    adult_guests = models.PositiveIntegerField(blank=False)
    child_guests = models.PositiveIntegerField(blank=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=False)
    payment_method = models.CharField(max_length=100, blank=False)
    transaction_id = models.CharField(max_length=255, blank=False)
    
    # Media files should be saved under student_id
    transaction_document = models.FileField(upload_to=transaction_upload_to, null=False, blank=False)
    profile_picture = models.ImageField(upload_to=profile_picture_upload_to, null=False, blank=False)
    
    registration_datetime = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=255, blank=False)  # Store hashed password
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False)
    approved = models.BooleanField(default=False)

    def calculate_total_amount(self):
        """Calculate total amount based on number of guests and event price."""
        if self.event:
            total = self.event.amount_per_person + self.adult_guests * self.event.amount_per_adult_guest + self.child_guests * self.event.amount_per_child_guest
            return total
        return 0

    def save(self, *args, **kwargs):
        """Override save to calculate total amount and hash password."""
        if not self.total_amount:
            self.total_amount = self.calculate_total_amount()

        # Hash the password before saving
        if self.password:
            self.password = make_password(self.password)
        
        if self.profile_picture:
            # Compress the profile picture before saving
            self.profile_picture = compress_image(self.profile_picture)

        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """Check if the provided password matches the stored hashed password."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"Registration for {self.full_name} - {self.event.title}"
