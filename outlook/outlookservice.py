import requests
import uuid
import json
import time
import datetime
graph_endpoint="http://graph.microsoft.com/v1.0{0}"

#Generic API query function

def make_api_call(method, url, token, user_email, payload=None, parameters=None):
	#Send these headers with the API call
	headers = {'User-Agent': 'pyathon_tutorial/1.0',
	'Authorization':'Bearer{0}'.format(token),
	'Accept':'application/json',
	'X-AnchorMailbox':user_email}

	#use these headers to instrument calls
	#make it easier to correlate requests and responses in case of problems

	request_id=str(uuid.uuid4())
	instrumentation={'client-request-id':request_id,
	'return-client-request-id':'true'}

	headers.update(instrumentation)

	response=None


	if(method.upper()=='GET'):
		response=requests.get(url, headers=headers, params=parameters)
	elif(method.upper()=='DELETE'):
		response=requests.delete(url, headers=headers, params=parameters)
	elif(method.upper()=='PATCH'):
		headers.update({'Content-Type':'application/json'})
		response=requests.patch(url, headers=headers, data=json.dumps(payload), params=parameters)
	elif(method.upper()=='POST'):
		headers.update({'Content-Type':'application/json'})
		response=requests.post(url, headers=headers, data=json.dump(payload), params=parameters)

	return response

def get_me(access_token):
	get_me_url=graph_endpoint.format('/me')

	#Use oData query parameters to control the results
	#- only return the display name and mail fields

	query_parameters={'$select':'displayName,mail'}
	r=make_api_call('GET', get_me_url, access_token,"",parameters=query_parameters)

	if (r.status_code==requests.codes.ok):
		return r.json()
	else:
		return "{0}: {1}".format(r.status_code, r.text)


def get_my_messages(access_token, user_email):
	get_messages_url=graph_endpoint.format('/me/mailfolders/inbox/messages')
	#use odata querys to control the results
	#only first 10 results found
	#only return received datetime,subject and from fields
	#sort the results by received datetime in descending order
	query_parameters={'$top':10,
					'$select':'receivedDateTime, subject, from',
					'$orderby':'receivedDateTime DESC'}

	r=make_api_call('GET', get_messages_url,access_token,user_email,parameters=query_parameters)

	if (r.status_code==requests.codes.ok):
		return r.json()
	else:
		return "{0}: {1}".format(r.status_code, r.text)


def get_my_events(access_token, user_email):
	get_events_url=graph_endpoint.format('/me/events')
	startDateString=datetime.datetime.now()
	endDateString=datetime.datetime.now() + datetime.timedelta(days=3*365)
	query_parameters={'$top':10, 
						'$select':'subject,start,end, attendees',
						'$orderby':'start/dateTime desc',
						'$filter': "Start/DateTime ge '" + str(startDateString) + "' and Start/DateTime le '" + str(endDateString) + "'"
						
						}

	r=make_api_call('GET', get_events_url, access_token, user_email, parameters=query_parameters)

	if (r.status_code == requests.codes.ok):
		return r.json()
		print(r)
	else:
		return "{0}: {1}".format(r.status_code, r.text)