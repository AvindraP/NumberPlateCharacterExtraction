import unittest
import preProcessor
from myEmail import searchVehicleNumber, saveViolator,get_email_by_vehicle_number, sendEmail

class TestIntegration(unittest.TestCase):

    def test_currectlydetecting(self):
        image_path = 'violator\\test.jpg'
        result = preProcessor.detect_numberplate(image_path)
        self.assertIsInstance(result, str)

    def test_email_and_saveviolator(self):
        vehicle_number = "KO8021"
        searchVehicleNumber(vehicle_number)
        result = saveViolator(vehicle_number)
        self.assertIsNone(result)

    def test_get_email_by_vehicle_number(self):
        email = get_email_by_vehicle_number("KO8021")
        self.assertEqual(email, "shenalorlof@gmail.com")

if __name__ == '__main__':
    unittest.main()