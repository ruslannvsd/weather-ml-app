import unittest
from app import app

class TestAppSmoke(unittest.TestCase):
	def setUp(self):
		app.testing = True
		self.client = app.test_client()

	# Complete the function below to test a success in running the application
	def test_prediction_route_success(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200, 'GET / should return HTTP 200')

	# Complete the function below to test a form is rendered
	def test_get_form(self):
		response = self.client.get('/')
		html = response.get_data(as_text=True)
		self.assertIn('<form method="POST" action="/">', html, 'Expected a form posting to /')
		for field in ('temperature', 'pressure', 'humidity', 'wind_speed', 'wind_deg',
		              'rain_1h', 'rain_3h', 'snow', 'clouds'):
			with self.subTest(field=field):
				self.assertIn(f'name="{field}"', html, f'Form is missing the {field} field')
		self.assertIn('type="submit"', html, 'Form should include a submit button')

if __name__ == '__main__':
	unittest.main()
