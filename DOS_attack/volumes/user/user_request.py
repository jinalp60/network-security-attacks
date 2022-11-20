'''
    author: jinal (kapatelj@uwindsor.ca)
'''
# user request code to get API response from the server
import requests

serverIP = '10.9.0.5'
serverPort = '8000'

response = requests.get('http://' + serverIP + ':' + serverPort + '/')
print(response.status_code)
print(response.text)