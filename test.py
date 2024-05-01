import unittest
from preProcessor import detect_numberplate
from myEmail import get_email_by_vehicle_number, sendEmail
from unittest.mock import patch
from unittest.mock import patch, MagicMock

class TestNumberplateDetection(unittest.TestCase):
    def test_numberplate_detection(self):

        image_path = 'violator\\test.jpg'

        preprocessed_image = (image_path)

        predicted_numberplate = detect_numberplate(preprocessed_image)
        
        expected_numberplate = 'ABC1234'
        print(f"Expected numberplate: {expected_numberplate}")
        print(f"Detected numberplate: {predicted_numberplate}")

        self.assertEqual(predicted_numberplate, expected_numberplate)


class TestSendEmail(unittest.TestCase):

    def test_sendEmail(self):
        sendEmail('shenalorlof@gmail.com')

class TestReceivemail(unittest.TestCase):

    def test_get_email_by_vehicle_number(self):
        email = get_email_by_vehicle_number("KO8021")
        self.assertEqual(email, "shenalorlof@gmail.com")

if __name__ == '__main__':
    unittest.main()
