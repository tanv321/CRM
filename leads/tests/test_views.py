from django.test import TestCase
from django.shortcuts import reverse
# Create your tests here for views.py
class LandingPageTest(TestCase): #will check to make sure everything in "leads/views.LandingPageView" is working accordingly.
    def test_get_code(self):#if you create a method with test_ then it will execute this method as a single test
        response = self.client.get(reverse("landing-page"))
        self.assertEqual(response.status_code, 200) #compares the response.status_code with the value 200(200 stands for status response code succession)
        self.assertTemplateUsed(response, "landing.html")
    

