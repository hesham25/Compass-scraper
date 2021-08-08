import pandas
import requests
from bs4 import BeautifulSoup
from time import sleep

results = []

def datails(url, region):
	r = requests.get(url, headers=headers)
	soup = BeautifulSoup(r.text, 'html.parser')
	agents = soup.select('div[class="agentCard"]')
	x = 1
	for s in agents:
		name = s.select_one('div[class="textIntent-headline1 agentCard-name"]').text.strip()
		link = 'https://www.compass.com' + s.select_one('a[class="agentCard-imageWrapper"]')['href']
		office_phone_tag = s.select_one('a[aria-label^="Call Office:"]')
		if office_phone_tag : office_phone = office_phone_tag.text.replace('O:','').strip()
		else: office_phone = '-'
		mobile_phone_tag = s.select_one('a[aria-label^="Call Mobile:"]')
		if mobile_phone_tag : mobile_phone = mobile_phone_tag.text.replace('M:','').strip()
		else: mobile_phone = '-'
		mail_tag = s.select_one('a[class="textIntent-body agentCard-email"]')
		if mail_tag : mail = mail_tag.text.strip()
		else: mail = '-'
		data = {
				'Region':region, 'Name': name, 'Mobile Phone':mobile_phone,
				'Office Phone':office_phone,
				 'E-mail':mail,'Link':link,
				}
		results.append(data)
		print(x,'of', len(agents),len(results))
		x += 1
		sleep(.15)
	df = pandas.DataFrame(results)
	df.to_excel('Finall Agents.xlsx', index=False)


headers = {
    'authority': 'www.compass.com',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://www.compass.com',
    'referer': 'https://www.compass.com/agents/',
}

urls  = pandas.read_excel('linksforcompass.xlsx')['links'].tolist()[:-1]
links = [link.replace('&referrer=omnibox','&page={}') for link in urls]
#print(links)
for link in links:
        for i in range(1,1000):
                url = link.format(i)
                r = requests.get(url, headers=headers)
                soup = BeautifulSoup(r.text, 'html.parser')
                title = soup.select_one('div[class="searchResults-header u-alignCenterLeft"]>div').text.strip().split('Agents Found in')[-1]
                city = title.split('-')[0]
                try: state = title.split('-')[1]
                except IndexError:    state = ''
                try: county = title.split('-')[2]
                except IndexError:    county = ''
                row = {'link':link,'City':city.strip(),'State':state.strip(),'County':county.strip()}
                results.append(row)
                print(row)
                #datails(region_link, region_name)
                sleep(1)
                
                if soup.select_one('button[title="Next Page"]') == None:
                        break

        df = pandas.DataFrame(results)
        df.to_excel('states.xlsx', index=False)
