from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
import os
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from .Event import Event

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
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False)
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
