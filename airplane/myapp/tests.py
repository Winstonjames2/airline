from ast import Pass
from django.test import Client, TestCase
from myapp.models import *
from django.db.models import Max
# Create your tests here.
class Tests(TestCase):

    def setUp(self):
        a1=Airport.objects.create(code="AAA",city="City A")
        a2=Airport.objects.create(code="BBB",city="City B")
        p=Passenger.objects.create(first="Alice",second="Brown")
        f1=Flight.objects.create(origin=a1,destination=a2,duration=100)
        Flight.objects.create(origin=a1,destination=a1,duration=200)
        Flight.objects.create(origin=a1,destination=a2,duration=-100)
        
        p.flights.add(f1)
    
    def test_depatures_count(self):
        a=Airport.objects.get(code="AAA")
        self.assertEqual(a.depatures.count(),3)

    def test_arrivals_count(self):
        a=Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(),1)

    def test_valid_flight(self):
        a1=Airport.objects.get(code="AAA")
        a2=Airport.objects.get(code="BBB")

        f=Flight.objects.get(origin=a1,destination=a2,duration=100)
        self.assertTrue(f.is_valid_flight())

    def test_index(self):
        """Testing Index function from views"""
        c=Client()
        response=c.get("/")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context["flights"].count(),3)
    
    def test_flight_exist(self):
        """Testing Flight Exists, this is testing the flight function from views"""
        a1=Airport.objects.get(code="AAA")
        f=Flight.objects.get(origin=a1,destination=a1)
        c=Client()
        response=c.get(f"/{f.id}")
        self.assertEqual(response.status_code,200)

    def test_flight_exist2(self):
        """Testing Flight Exists, this is testing the flight function from views this is for invalid Page"""
        max_id=Flight.objects.all().aggregate(Max("id"))["id__max"]
        c=Client()
        response=c.get(f"/{max_id+1}")
        self.assertEqual(response.status_code,404)
    
    def test_passenger_content(self):
        """Testing Passengers Info Correction"""
        a1=Airport.objects.get(code="AAA")
        f=Flight.objects.get(origin=a1,destination=a1)
        c=Client()
        response=c.get(f"/{f.id}")
        self.assertEqual(response.context["passengers"].count(),1)