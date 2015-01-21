import csv
import requests
import pprint


base_url = "https://cgp.mydonedone.com/issuetracker/api/v2"
project_id = xxxx
user = 'xxxxx'
token = "xxxxxxxx"

def read_rows(file):
	ctr = 0
	issues_created = 0

	with open(file, 'rb') as csvfile:
		for row in csv.reader(csvfile.read().splitlines()):

			#dont read from first row -- which contains column titles
			if ctr > 0:
				role = row[1]
				can_statement = row[2]
				title = "As a %s, I can %s" %(role, can_statement)
				priority_level_id = row[3]
				fixer_id = row[4]
				tester_id = row[5]
				comp_url = row[6]
				wire_url = row[7]

				description = "As seen in the %s section.  \n\nComp here: %s  \n\nWire here: %s  \n\n " \
				"Please verify that this requirement has been met before assigning this ticket to the next" \
				"person in the workflow." % (row[0], comp_url, wire_url)
				
				try:
					post_request(title,description,priority_level_id,fixer_id,tester_id)
					issues_created += 1
				except:
					print "failed to create issue '%s'" % title

			ctr += 1
		print "%s issues have been created" % issues_created


def match_and_post_tags(file):
	ctr = 0
	issues_tagged = 0

	with open(file, 'rb') as csvfile:
		for row in csv.reader(csvfile.read().splitlines()):

			#dont read from first row -- which contains column titles
			if ctr > 0 :
				can_statement = row[2]
				tags = [item for item in row[8].split(',')]
				print tags
				#item_number = match_issue(can_statement)

				convert_tags_to_ids(tags)

					#post_tags(item_number, tags)
				issues_tagged += 1


			ctr += 1


def convert_tags_to_ids(tags):

	endpoint = base_url+"/projects/%s.json" % (project_id)

	response = requests.get(endpoint,auth=(user,token))
	response_tags = response.json()['tags']
	tag_ids = []

	for item in tags:
		for tag in response_tags:

			if tag['name'] in item:
				tag_ids.append(tag['id'])

	return tag_ids



def post_tags(item_number, *tags):
	ctr = 0
	issues_tagged = 0
	endpoint = base_url+"/projects/%s/issues/%s.json" % (project_id, item_number)
	data = {
		'tag_ids':tags,
		}

	#requests.post(endpoint,auth=(user,token),data=data)
	print "issue '%s' has been created" % title


def post_request(title, description, priority_level_id, fixer_id, tester_id):
	base_url = "https://cgp.mydonedone.com/issuetracker/api/v2"
	project_id = 32143
	user = 'paraserry'
	token = "231F84AAE9D3020529DD664FE08E6EE0"

	endpoint = base_url+"/projects/%s/issues.json" % project_id
	data = {
		'title':title,
		'description':description,
		'priority_level_id':priority_level_id,
		'fixer_id':fixer_id,
		'tester_id':tester_id
		}

	requests.post(endpoint,auth=(user,token),data=data)
	print "issue '%s' has been created" % title


def match_issue(can_statement):

	endpoint = base_url+"/projects/%s/issues/all.json" % (project_id)

	response = requests.get(endpoint,auth=(user,token), params={'take':300})
	for item in response.json()['issues']:
		title = item['title']

		if can_statement in title:
			return item['order_number']
		else:
			return None



if __name__ == '__main__':
    match_and_post_tags('donedone_test.csv')




