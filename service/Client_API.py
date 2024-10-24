import requests

from settings.config import Config


class APIClient:

	def __init__(self):
		self.__api_url = Config.FLASK_API_URL

	def send_data(self, data):
		try:
			response = requests.post(self.__api_url, json=data)
			response.raise_for_status()
		except requests.exceptions.RequestException as e:
			raise Exception("Falha ao enviar os dados.")
