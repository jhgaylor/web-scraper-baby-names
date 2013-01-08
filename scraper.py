from BabyNamer import settings
from django.core.management import setup_environ
setup_environ(settings)

from Namer.models import Name, NameUsage
from bs4 import BeautifulSoup
import requests
import json

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
sub_alphabet = ['i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# #print get_soup(gen_url('a')).prettify()
# f = open('output.html')
# soup = BeautifulSoup(f.read())
# result_rows =  soup.select('.result_row2') + soup.select('.result_row1') 
# name_rows = []
# names = []
# for r in result_rows:
#   tmp = r.select('.r_name')
# 	if tmp:
# 		name_rows.append(r)

# for r in name_rows:
# 	row_data = {
# 		'name':r.select('.r_name a')[0].get_text().strip(), #text
# 		'gender':r.select('.r_gender')[0].get_text().strip(),#text
# 		'meaning':r.select('.r_meaning')[0].get_text().strip(),#text
# 		'origin':r.select('.r_origin')[0].get_text().strip(),#text
# 		'more_url':"http://babynamesworld.parentsconnect.com/" + r.select('.r_name a')[0].get('href'), #use the href of this link
# 	}
# 	names.append(row_data)
# print name_rows
# #print soup


# for letter in alphabet:
# 	print gen_url(letter)
def removeNonAscii(s): 
	return "".join(i for i in s if ord(i)<128)

class BNW(object):
	def __init__(self, search_term, page=1):
		"""" Construct my crazy object """
		self.search_term = search_term
		self.current_page = int(page)
		self.max_page = None
		self.names = []

	def run(self):
		self.make_url()
		self.make_soup()
		self.get_last_page_number()
		print self.search_term
		while self.current_page <= self.max_page:
			self.get_names()
			self.current_page += 1
			print "Current:"
			print self.current_page
			print "Max:"
			print self.max_page
			self.make_url()
			self.make_soup()
		return self.names


	def make_url(self):
		self.url = "http://babynamesworld.parentsconnect.com/search.php?p=qsearch&s_gender=1&s_copt=2&i_search="+self.search_term+"&s_filter=14&page="+str(self.current_page)		


	def make_soup(self):
		""" put html of url into memory """
		resp = requests.get(self.url)
		html = removeNonAscii(resp.text)
		soup = BeautifulSoup(html)
		self.soup = soup


	def get_last_page_number(self):
		""" get the max page number """
		#print self.soup.prettify()
		try:
			self.max_page = int(self.soup.select('#divNav_1 > a')[-1].get_text().strip())
		except:
			self.max_page = int(raw_input('How many pages for the search term '+self.search_term+ '? '))


	def get_names(self):
		#get name rows
		result_rows = self.soup.select('.result_row1') + self.soup.select('.result_row2')
		name_rows = []

		for r in result_rows:
			tmp = r.select('.r_name')
			if tmp:
				name_rows.append(r)

		for r in name_rows:
			row_data = {
				'name':r.select('.r_name a')[0].get_text().strip(), #text
				'gender':r.select('.r_gender')[0].get_text().strip(),#text
				'meaning':r.select('.r_meaning')[0].get_text().strip(),#text
				'origin':r.select('.r_origin')[0].get_text().strip(),#text
				'more_url':"http://babynamesworld.parentsconnect.com/" + r.select('.r_name a')[0].get('href'), #use the href of this link
			}
			self.names.append(row_data)


#names = Name.objects.all().order_by('name')


####general idea
# url = "http://babynamesworld.parentsconnect.com/meaning_of_jacob.html"
# resp = requests.get(url)
# html_text = resp.text
# soup = BeautifulSoup(html_text)
# print soup.prettify()

for letter in sub_alphabet:	
	api = BNW(letter, 1)
	names = api.run()
	f_name = ''.join(['name_data_', letter, '.json'])
	print "opening a file"
	print f_name

	f = open(f_name, 'w')
	f.write(json.dumps(names))
	f.close()
	print "wrote a file\n"
	print f_name
