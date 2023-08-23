from django.shortcuts import reverse
from django.test import TestCase

# Create your tests here.

class LandingPageTest(TestCase):
    def test_get(self):
        response = self.client.get(reverse("lading-page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="landing.html")
    
