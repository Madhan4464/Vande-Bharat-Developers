from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Project(models.Model):
    class PropertyType(models.TextChoices):
        PLOT = "plot", "Residential plot"
        OPEN_PLOT = "open_plot", "Open plot"
        VILLA = "villa", "Villa"
        APARTMENT = "apartment", "Apartment"

    class Status(models.TextChoices):
        COMING_SOON = "coming_soon", "Coming soon"
        AVAILABLE = "available", "Available"
        SELLING_FAST = "selling_fast", "Selling fast"
        SOLD_OUT = "sold_out", "Sold out"

    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    location = models.CharField(max_length=180, blank=True)
    property_type = models.CharField(
        max_length=24, choices=PropertyType.choices, default=PropertyType.PLOT
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    overview = models.TextField()
    image = models.ImageField(upload_to="projects/covers/", blank=True)
    plot_sizes = models.CharField(max_length=180, blank=True, help_text="For example: 150–300 sq. yd.")
    price_from = models.DecimalField(
        max_digits=14, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)]
    )
    price_to = models.DecimalField(
        max_digits=14, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)]
    )
    highlights = models.TextField(blank=True, help_text="One highlight per line.")
    amenities = models.TextField(blank=True, help_text="One amenity per line.")
    nearby_landmarks = models.TextField(blank=True, help_text="One landmark per line.")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "project"
            candidate = base_slug
            suffix = 2
            while Project.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"slug": self.slug})


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=160, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "pk"]

    def __str__(self):
        return self.caption or f"{self.project.name} gallery image"


class Enquiry(models.Model):
    class Kind(models.TextChoices):
        GENERAL = "general", "General contact"
        PROJECT = "project", "Project enquiry"

    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        CLOSED = "closed", "Closed"

    kind = models.CharField(max_length=12, choices=Kind.choices, default=Kind.GENERAL)
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, related_name="enquiries", blank=True, null=True
    )
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField(max_length=2000)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.get_kind_display()}"


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    quote = models.TextField(max_length=800)
    context = models.CharField(max_length=120, blank=True, help_text="For example: Homeowner or Investor.")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "customer testimonial"
        verbose_name_plural = "customer testimonials"

    def __str__(self):
        return f"{self.customer_name}'s testimonial"
