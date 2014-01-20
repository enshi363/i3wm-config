from time import time
import requests
import logging

logger = logging.getLogger('mylogger') 
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler() 
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.addHandler(ch)
ch.setFormatter(formatter)
http = urllib3.PoolManager()

class Py3status:
	def __init__(self):
		self.cache_timeout = 1800
		"""
		city_code from http://www.weather.com.cn
		"""
		self.city_code = '101020100'
		self.request_timeout = 10
	def _get_forecast(self):
		r = requests.get(
            'http://m.weather.com.cn/data/%s.html' % self.city_code,
            timeout=self.request_timeout
		)
		result = r.json()
		status = r.status_code
		forecast = {}
		
		if status == 200:
			forecast = result['weatherinfo']['weather1'] + result['weatherinfo']['temp1']
		else:
			raise Exception('got status {}'.format(status))
		return forecast

	def weather_cn(self, json, i3status_config):
		response = {
			'cached_until': time() + self.cache_timeout,
			'full_text': '',
			'name': 'weather_cn'
			}
		forecasts = self._get_forecast()
		response['full_text'] = forecasts
		return (0, response)

def main():
	py3 = Py3status()
	py3._get_forecast()


if __name__ == '__main__':
    main()
