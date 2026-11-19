import re
import unittest
from app import app  # Import your Flask app instance

class TestModelAppIntegration(unittest.TestCase):

	def setUp(self):
		app.testing = True
		self.client = app.test_client()

	def test_model_app_integration(self):
		# Valid test input that should work with the trained model
		form_data = {
			'temperature': '275.15',   # Kelvin
			'pressure': '1013',        # hPa
			'humidity': '85',          # %
			'wind_speed': '3.6',       # m/s
			'wind_deg': '180',         # degrees
			'rain_1h': '0',            # mm
			'rain_3h': '0',            # mm
			'snow': '0',               # mm
			'clouds': '20'             # %
		}

		response = self.client.post('/', data=form_data)

		self.assertEqual(response.status_code, 200, 'Valid input should return HTTP 200')
		html_text = response.get_data(as_text=True).lower()
		self.assertIn('<h1>prediction result</h1>', html_text, 'Expected the result page')
		prediction = re.search(r'the weather is:</strong>\s*([^<]+)</p>', html_text)
		self.assertIsNotNone(prediction, 'Result page should display a weather prediction')
		self.assertRegex(
			html_text, r'prediction time:</strong>\s*\d+(?:\.\d+)?\s*ms',
			'Result page should show a numeric prediction time in milliseconds',
		)
		valid_classes = [
			'clear', 'cloudy', 'drizzly', 'foggy', 'hazey',
			'misty', 'rainy', 'smokey', 'thunderstorm'
		]
		self.assertIn(
			prediction.group(1).strip(), valid_classes,
			'Displayed prediction should be one of the supported weather classes',
		)

if __name__ == '__main__':
	unittest.main()
