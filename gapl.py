import csv
from datetime import datetime
import urllib.request
import requests
from bs4 import BeautifulSoup

def get_name(body):
    return body.find('span', {'class':'jcn'}).a.string

def get_phone_number(body):
    try:
        return body.find('p', {'class':'contact-info'}).span.a.string
    except AttributeError:
        return ''

def get_rating(body):
    rating = 0.0
    text = body.find('span', {'class':'star_m'})
    if text is not None:
        for item in text:
            rating += float(item['class'][0][1:])/10

    return rating

def get_rating_count(body):
    text = body.find('span', {'class':'rt_count'}).string

    rating_count =''.join(i for i in text if i.isdigit())
    return rating_count

def get_address(body):
    return body.find('span', {'class':'mrehover'}).text.strip()

def get_location(body):
    text = body.find('a', {'class':'rsmap'})
    if text == None:
        return
    text_list = text['onclick'].split(",")
    
    latitutde = text_list[3].strip().replace("'", "")
    longitude = text_list[4].strip().replace("'", "")
    
    return latitutde + ", " + longitude
def get_article(url_string):
	user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	headers={'User-Agent':user_agent,} 
	while(True):
		try:
			req = urllib.request.Request(url_string,None,headers)
			response = urllib.request.urlopen(req)
			break
		except urllib.error.HTTPError as e:
			if e.code == 404:
				return 'Invalid'
			else:
				pass
		except:
			pass
	return response.read()
page_number=1
details_count=1


fields = ['Name', 'Phone', 'Rating', 'Rating Count', 'Address', 'Location']
out_file = open('customer_details.csv','w')
csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)

while True:

    if page_number>50:
        break
    print("here")
    url="https://www.justdial.com/Bangalore/Automobile-Part-Manufacturers/nct-10028195/page-%s"%(page_number)
    text = get_article(url)
    soup = BeautifulSoup(text, "html.parser")
    details = soup.find_all('li', {'class': 'cntanr'})


    for i in details:
        dictionary_details={}
        name=get_name(i)
        phone=get_phone_number(i)
        rating=get_rating(i)
        count=get_rating_count(i)
        address=get_address(i)
        location=get_location(i)

        if name != None:
            dictionary_details['Name'] = name
        if phone != None:
            print('getting phone number')
            dictionary_details['Phone'] = phone
        if rating != None:
            dictionary_details['Rating'] = rating
        if count != None:
            dictionary_details['Rating Count'] = count
        if address != None:
            dictionary_details['Address'] = address
        if location != None:
            dictionary_details['Address'] = location

        csvwriter.writerow(dictionary_details)
        print("#" + str(details_count) + " " , dictionary_details)
        details_count += 1

    
    page_number += 1
out_file.close()
