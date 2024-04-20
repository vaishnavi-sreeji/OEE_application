from django.test import TestCase
from .models import Machines, ProductionLog
import .views
from datetime import datetime, timedelta

class OEECalculationTestCase(TestCase):
    def setUp(self):
        self.machine = Machines.objects.create(
            machine_name='Test Machine',
            machine_serial_no='12345'
        )
        
        # Create production logs
        ProductionLog.objects.create(
            cycle_no='CN001',
            unique_id='P001',
            material_name='Material1',
            machine=self.machine,
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(minutes=5),
            duration=0.08333  # 5 minutes in hours
        )
        
        ProductionLog.objects.create(
            cycle_no='CN002',
            unique_id='P002',
            material_name='Material1',
            machine=self.machine,
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(minutes=10),
            duration=0.16667  # 10 minutes in hours
        )
    
    def test_calculate_oee(self):
        # Call the calculate_oee function and verify the output
        oee = calculate_oee(self.machine)
        self.assertIsNotNone(oee)
        self.assertTrue(0 <= oee <= 1)

