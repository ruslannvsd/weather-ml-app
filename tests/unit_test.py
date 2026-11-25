import unittest
from app import app, classify_weather, load_model, weather_classes
import numpy as np

class TestUnit(unittest.TestCase):
	def setUp(self):
		app.testing = True
		self.client = app.test_client()

	# Complete this function to test proper handling of missing input field in the input
	def test_post_missing_field(self):
		form_data = {
			'temperature': '270.277',
			'pressure': '1006',
			'humidity': '84',
			# 'wind_speed' is missing
			'wind_deg': '274',
			'rain_1h': '0',
			'rain_3h': '0',
			'snow': '0',
			'clouds': '9'
		}
		response = self.client.post('/', data=form_data)
		html = response.get_data(as_text=True)
		self.assertIn('Error processing input:', html, 'Missing wind speed should display an error')
		self.assertIn('<form', html, 'The input form should be shown again')
		self.assertNotIn('Prediction Result', html, 'Incomplete input should not show a prediction')

	# Complete this function to test that the model can be loaded correctly
	def test_model_can_be_loaded(self):
		model = load_model()
		self.assertIsNotNone(model, 'Expected the trained model to load')
		self.assertTrue(callable(getattr(model, 'predict', None)), 'Loaded model should support predict')

	# Test model classification is within the 9 classes, each time for a different class with three different inputs
	def test_clear_classification_output(self):
		test_input = np.array([269.686,1002,78,0,23,0,0,0,0]).reshape(1,-1)
		class_result, _ = classify_weather(test_input)
		# Ensure that 'clear' class is returned
		self.assertEqual(class_result, 'clear', 'Expected clear for the supplied clear-weather input')

	def test_rainy_classification_output(self):
		test_input = np.array([279.626,998,99,1,314,0.3,0,0,88]).reshape(1,-1)
		class_result, _ = classify_weather(test_input)
		# Ensure that the rain class is returned (read from the app, so 'rainy' -> 'rain' still passes)
		self.assertEqual(class_result, weather_classes[6], 'Expected the rain class for the supplied rainy-weather input')

	def test_cloudy_classification_output(self):

		test_input = np.array([289.47,1015,88,2,300,0,0,0,20]).reshape(1,-1)
		class_result, _ = classify_weather(test_input)

		# The Valencia observation is labelled 'clouds' (few clouds) in weather_features.csv.
		self.assertEqual(class_result, 'cloudy', 'Expected cloudy for the Valencia observation labelled clouds')

if __name__ == '__main__':
	unittest.main()
