import unittest
import cv2
from main import RGB, cap, class_list, calculate_rotation_angle, straighten_image, convert_to_binary, output_dir
import preProcessor
from preProcessor import detect_numberplate

class TestIntegration(unittest.TestCase):

    def test_mouse_event(self):
        # Test RGB mouse event
        event = cv2.EVENT_MOUSEMOVE
        x = 100
        y = 200
        flags = None
        param = None
        result = RGB(event, x, y, flags, param)
        self.assertIsNone(result)

    def test_calculate_rotation_angle(self):
        # Test calculate_rotation_angle function
        region = cv2.imread('violator\\test.jpg')
        angle = calculate_rotation_angle(region)
        self.assertIsInstance(angle, float)

    def test_straighten_image(self):
        # Test straighten_image function
        region = cv2.imread('violator\\test.jpg')
        straightened_image = straighten_image(region)
        self.assertIsNotNone(straightened_image)

    def test_convert_to_binary(self):
        # Test convert_to_binary function
        region = cv2.imread('violator\\test.jpg')
        binary_image = convert_to_binary(region)
        self.assertIsNotNone(binary_image)

    def test_detect_numberplate(self):
        # Test detect_numberplate function
        image_path = 'violator\\test.jpg'
        result = detect_numberplate(image_path)
        self.assertIsInstance(result, str)

    def test_preProcessor(self):
        # Test preProcessor module functions
        image_path = 'violator\\test.jpg'
        result = preProcessor.detect_numberplate(image_path)
        self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main()