from django.contrib import admin

from .models import Enquiry, Project, ProjectImage, Testimonial


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "property_type", "status", "price_from", "is_featured")
    list_filter = ("status", "property_type", "location", "is_featured")
    search_fields = ("name", "location", "overview")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProjectImageInline]


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "project", "phone", "email", "status", "created_at")
    list_filter = ("kind", "status", "created_at")
    search_fields = ("name", "phone", "email", "message", "project__name")
    readonly_fields = ("created_at",)
    list_editable = ("status",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "context", "is_published", "created_at")
    list_filter = ("is_published", "created_at")
    search_fields = ("customer_name", "quote", "context")
    list_editable = ("is_published",)
    readonly_fields = ("created_at",)
