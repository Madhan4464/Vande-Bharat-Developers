from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EnquiryForm
from .models import Enquiry, Project, Testimonial


def home(request):
    featured = Project.objects.exclude(status=Project.Status.SOLD_OUT)[:3]
    testimonials = Testimonial.objects.filter(is_published=True)[:3]
    return render(
        request,
        "real_estate/home.html",
        {"featured_projects": featured, "testimonials": testimonials},
    )


def about(request):
    return render(request, "real_estate/about.html")


def projects(request):
    queryset = Project.objects.all()
    query = request.GET.get("q", "").strip()
    location = request.GET.get("location", "").strip()
    property_type = request.GET.get("type", "").strip()
    budget = request.GET.get("budget", "").strip()

    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) | Q(location__icontains=query) | Q(overview__icontains=query)
        )
    if location:
        queryset = queryset.filter(location__icontains=location)
    if property_type in Project.PropertyType.values:
        queryset = queryset.filter(property_type=property_type)
    if budget == "under-50":
        queryset = queryset.filter(price_from__lte=5000000)
    elif budget == "50-100":
        queryset = queryset.filter(price_from__gte=5000000, price_from__lte=10000000)
    elif budget == "over-100":
        queryset = queryset.filter(price_from__gt=10000000)

    locations = (
        Project.objects.exclude(location="")
        .order_by("location")
        .values_list("location", flat=True)
        .distinct()
    )
    return render(
        request,
        "real_estate/projects.html",
        {
            "projects": queryset,
            "locations": locations,
            "property_types": Project.PropertyType.choices,
        },
    )


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    form = EnquiryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        enquiry = form.save(commit=False)
        enquiry.project = project
        enquiry.kind = Enquiry.Kind.PROJECT
        enquiry.save()
        messages.success(request, "Thank you. Your project enquiry has been sent to our team.")
        return redirect(project.get_absolute_url() + "#enquiry")
    return render(request, "real_estate/project_detail.html", {"project": project, "form": form})


def contact(request):
    form = EnquiryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        enquiry = form.save(commit=False)
        enquiry.kind = Enquiry.Kind.GENERAL
        enquiry.save()
        messages.success(request, "Thank you. Your message has been received.")
        return redirect("contact")
    return render(request, "real_estate/contact.html", {"form": form})


def robots_txt(request):
    return HttpResponse("User-agent: *\nAllow: /\nDisallow: /admin/\n", content_type="text/plain")
