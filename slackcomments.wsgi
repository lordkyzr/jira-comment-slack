import json
import requests
import datetime
import requests

def unicodetobytes(unicodeitem):
	if isinstance(unicodeitem, dict):
		return {unicodetobytes(key):unicodetobytes(value) for key,value in unicodeitem.iteritems()}
	elif isinstance(unicodeitem, list):
		return [unicodetobytes(element) for element in unicodeitem]
	elif isinstance(unicodeitem, unicode):
		return unicodeitem.encode('utf-8')
	else:
		return unicodeitem

def application(environ, start_response):

	#Define slack_channel, slack_url, Jira API Connection auth
	slack_url = 'https://hooks.slack.com/services/EXAMPLE/TEST/EXAMPLE'
	slack_channel = "#mychannel"

	jira_username = 'testuser'
	jira_password = 'foobar'

	#True will post the request, False will not. Allows for conditionals if needed.
	slack_post = True

	try:
		#Get the size of the posted data
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
	except (ValueError):
		request_body_size = 0

	#Read the posted data
	request_body = environ['wsgi.input'].read(request_body_size)

	#Encode it in JSON
	jsonencodedpost = json.loads(request_body)

	#Get rid of Unicode formatting
	jsonrequest = unicodetobytes(jsonencodedpost)

	#Comment properties
	comment_body = jsonrequest['comment']['body']
	comment_author = jsonrequest['comment']['updateAuthor']['displayName']
	comment_id = jsonrequest['comment']['id']

	#Created vs updated conditional
	if jsonrequest['comment']['created'] == jsonrequest['comment']['updated']:
		comment_type = 'created'
		slack_color = '#439FE0'
	else:
		#uncomment if you only want new comments not updated comments.
		#slack_post =  False
		comment_type = 'updated'
		slack_color = '#7CD197'

	###Gotta dip the JIRA API ourselves###
	#Get the URL of the JIRA instance
	jira_api_destination = str(jsonrequest['comment']['self']).replace('comment/','')
	jira_api_destination = jira_api_destination.replace(jsonrequest['comment']['id'],'')

	#Send request to JIRA instance
	response = requests.get(jira_api_destination, auth=(jira_username,jira_password))
	if response.status_code == 200:
		jira_response = json.loads(response.text)
		jira_response = unicodetobytes(jira_response)
		task_key = jira_response['key']
		task_id = jira_response['id']
		task_link = str(jsonrequest['comment']['self']).replace('rest/api/2/issue', 'browse').replace(task_id, task_key)
		task_summary = jira_response['fields']['summary']
	else:
		task_key = 'FOOBAR-1'
                task_id = '1'
                task_link = ''
                task_summary = 'Failed to retrieve the data. I am no longer your bot overlord T--T'


        comment_link = ('%(task_link)s?focusedCommentId=%(comment_id)s&'
                            'page=com.atlassian.jira.plugin.system.issuetabpanels:'
                            'comment-tabpanel#comment-%(comment_id)s') % {
                'task_link': task_link,
                'comment_id': comment_id,
            }

	slack_pretext = comment_author + ' ' + comment_type + ' comment'
	slack_title = task_key + ' : ' + task_summary
	slack_data = {
                'username': 'Your Comment Bot Overlord',
                'channel': slack_channel,
                'attachments': [
                    {
                        'fallback': slack_pretext + ' - ' + slack_title + ' - ' + comment_link,
                        'pretext': slack_pretext,
                        'title': slack_title,
                        'title_link': comment_link,
                        'text': comment_body,
                        'color': slack_color
                    }
                ]
            }
	if slack_post == True:
		response = requests.post(
                    slack_url, data=json.dumps(slack_data),
                    headers={'Content-Type': 'application/json'}
                )
		if response.status_code != 200:
                	raise ValueError(
                        'Request to slack returned an error %s, the response is:\n%s'
                        % (response.status_code, response.text)
                    )

	status = '200 OK'
	slackresponse = ''
        #---------------USE THIS BLOCK TO RETURN DATA-------------------------#
        clength = 0                                                           #
        clength = len(slackresponse)                                          #
        response_headers = [('Content-type', 'text/html'),                    #
                        ('Content-Length', str(clength))]                     #
        start_response(status, response_headers)                              #
        return slackresponse                                                  #
        #---------------------------------------------------------------------#


