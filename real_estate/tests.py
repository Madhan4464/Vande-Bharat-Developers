from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Enquiry, Project, Testimonial


@override_settings(SECURE_SSL_REDIRECT=False)
class PublicSiteTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="South Future City",
            location="South India",
            overview="A thoughtfully planned residential project.",
            plot_sizes="150–300 sq. yd.",
            price_from=2500000,
        )

    def test_featured_project_appears_on_homepage(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "South Future City")
        self.assertContains(response, "Building Your Dreams")

    def test_only_published_customer_testimonials_are_displayed(self):
        Testimonial.objects.create(
            customer_name="Asha Rao",
            quote="A clear and thoughtful conversation.",
            is_published=True,
        )
        Testimonial.objects.create(
            customer_name="Unpublished Customer",
            quote="This review is not ready to share.",
            is_published=False,
        )
        response = self.client.get(reverse("home"))
        self.assertContains(response, "A clear and thoughtful conversation.")
        self.assertNotContains(response, "This review is not ready to share.")

    def test_project_filters_and_detail_page_work(self):
        response = self.client.get(reverse("projects"), {"q": "South Future"})
        self.assertContains(response, "South Future City")
        self.assertEqual(self.client.get(self.project.get_absolute_url()).status_code, 200)

    def test_project_detail_renders_admin_managed_features_and_availability(self):
        self.project.highlights = "Tree-lined avenues\nThoughtful layout"
        self.project.amenities = "Walking paths\nLandscaped greens"
        self.project.nearby_landmarks = "Regional transport hub"
        self.project.status = Project.Status.AVAILABLE
        self.project.save()
        response = self.client.get(self.project.get_absolute_url())
        self.assertContains(response, "Tree-lined avenues")
        self.assertContains(response, "Walking paths")
        self.assertContains(response, "Regional transport hub")
        self.assertContains(response, "Ask about availability")

    def test_project_enquiry_is_saved_against_project(self):
        response = self.client.post(
            self.project.get_absolute_url(),
            {
                "name": "Asha Rao",
                "phone": "9876543210",
                "email": "asha@example.com",
                "message": "Please share available plot details.",
            },
        )
        self.assertRedirects(response, self.project.get_absolute_url() + "#enquiry")
        enquiry = Enquiry.objects.get()
        self.assertEqual(enquiry.project, self.project)
        self.assertEqual(enquiry.kind, Enquiry.Kind.PROJECT)

    def test_contact_form_persists_valid_enquiry(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Asha Rao",
                "phone": "+91 98765 43210",
                "email": "asha@example.com",
                "message": "Please share more about your projects.",
            },
        )
        self.assertRedirects(response, reverse("contact"))
        enquiry = Enquiry.objects.get()
        self.assertEqual(enquiry.name, "Asha Rao")
        self.assertEqual(enquiry.phone, "919876543210")
        self.assertEqual(enquiry.kind, Enquiry.Kind.GENERAL)

    def test_invalid_phone_does_not_create_enquiry(self):
        self.client.post(
            reverse("contact"),
            {
                "name": "Asha Rao",
                "phone": "not-a-number",
                "email": "asha@example.com",
                "message": "Please call me.",
            },
        )
        self.assertFalse(Enquiry.objects.exists())

    def test_admin_requires_authentication(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])
