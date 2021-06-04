import requests as r
import webbrowser
import json

class YooMoney:
	client_id = None	# Client ID (register an app - get its token)
	headers = {"Content-Type": "application/x-www-form-urlencoded"}	# Headers
	api_url = 'https://yoomoney.ru'	# Main URL

	def __init__(self, client_id, token = None, redirect_url = None, proxy=None):
		self.proxy = {"https" : proxy}
		if client_id is None:
			raise Exception("Client_ID not set") 
		self.client_id = client_id
		if token is None:	# No token given - get it
			if redirect_url is None:
				raise Exception("Redirect URL not set")
			token = self.getToken(client_id, redirect_url)
			if token['error']:
				raise Exception(token['error_message'])
			token = token['data']
			print('YOUR ACCESS TOKEN (valid for 3 years): {}'.format(token))
		self.headers['Authorization'] = "Bearer {}".format(token)	# Add authorization token to headers


	def getToken(self, client_id, redirect_url):	# Get token using Client ID (Redirect URL MUST be the same as in the app description)
		if redirect_url is None:
			return {'error': 1, 'error_message': 'Redirect URL not set'}
		code_req = r.post(f'{self.api_url}/oauth/authorize', data=f'client_id={client_id}&response_type=code&redirect_uri={redirect_url}&scope=account-info operation-history payment-p2p operation-details', allow_redirects=False, headers=self.headers, proxies = self.proxy)
		#webbrowser.open(code_req.headers.get('Location'), new=2)	# Open recieved URL and let user submit
		print(code_req.headers.get('Location'))
		code = input('Token (after redirect in URL panel as parameter): ')	# After the user gets redirected, there will be a parameter 'code', which has to be put here
		token_req = r.post(f'{self.api_url}/oauth/token', data=f'code={code}&client_id={client_id}&grant_type=authorization_code&redirect_uri={redirect_url}&client_secret=642FA9AD15C1C90E06EA07795E7DF9190A1DD6E631C326E92BFB047BF71B5457B52350F3B59FA805D89999150752889295BED6D7D3601E82D91FD01C177770A8', headers=self.headers, proxies = self.proxy)	# Fetch final toke using app ID and recieved temp-token
		if token_req.status_code != 200:
			print({'error': 1, 'error_message': f'Status code: {token_req.status_code}'})
			return {'error': 1, 'error_message': f'Status code: {token_req.status_code}'}
		print({'error': 0, 'data': token_req.json()['access_token']})
		return	{'error': 0, 'data': token_req.json()['access_token']}

	def getAccInfo(self):	# Get account info (balance, payment methods...)
		self.headers["Content-Length"] = '0'
		if not 'Authorization' in self.headers.keys():
			return {'error': 1, 'error_message': 'Token not set'}
		acc = r.post(f'{self.api_url}/api/account-info', headers=self.headers, proxies=self.proxy)
		if acc.status_code != 200:
			return {'error': 1, 'error_message': f'Status code: {acc.status_code}'}
		return {'error': 0, 'data': acc.json()}

	def getHistory(self, operation_type=1, records=10):	# Get full details about specified amount of records (amount, comment, in/out...)
		if not 'Authorization' in self.headers.keys():
			return {'error': 1, 'error_message': 'Token not set'}
		oper_type = ''	# Fetch specified operations (empty for all; type = 1 - deposit; type = 2 - payment)
		if operation_type == 1:
			oper_type = 'deposition'
		elif operation_type == 2:
			oper_type = 'payment'
		data = f'type={oper_type}&records={int(records)}&details=true'
		payments = r.post(f'{self.api_url}/api/operation-history', data=data, headers=self.headers, proxies=self.proxy)
		if payments.status_code != 200:
			return {'error': 1, 'error_message': f'Status code: {payments.status_code}'}
		return {'error': 0, 'data': payments.json()}

	def makePayment(self, to, amount, message=''):	# Make payment to account/phone associated with it (ThIs MeThOd WaS NoT TeStEd BeCaUsE I dOnT HavE aNy MoNeY)
		if not 'Authorization' in self.headers.keys():
			return {'error': 1, 'error_message': 'Token not set'}
		if to is None:
			return {'error': 1, 'error_message': 'Получатель не был установлен'}
		if amount is None:
			return {'error': 1, 'error_message': 'Сумма не была установленна'}
		status = r.post(f'{self.api_url}/api/request-payment', data=f'pattern_id=p2p&to={to}&amount_due={amount}&message={message}', headers=self.headers, proxies=self.proxy)	# Create a payment with user creds and amount
		if status.status_code != 200:
			return {'error': 1, 'error_message': f'Status code: {status.status_code}'}
		status = status.json()
		print(status)
		if status["status"] == "refused":	# Check if the payment is allowed (yandex checks, if there is enough balance)
			return {'error': 1, 'error_message': status["error"]}
		confirm = r.post(f'{self.api_url}/api/process-payment', data='request_id={}'.format(status['request_id']), headers=self.headers, proxies=self.proxy)	# Confirm payment
		if confirm.status_code != 200:
			return {'error': 1, 'error_message': f'Status code: {confirm.status_code}'}
		return {'error': 0, 'data': confirm.json()}

