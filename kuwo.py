__author__ = 'jxcjxcjzx'
#coding:utf-8
import os
import re
import time
import codecs
import requests
import simplejson
from bs4 import BeautifulSoup
import string
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def analyze_single_page_with_artistId_pnIndex(artistId,pnIndex):
	''' analysis one single page of a singer , extract the songs '''
	baseUrl= "http://www.kuwo.cn/artist/contentMusicsAjax?"	
	artistIdFragment = "artistId="+artistId
	pnFragment = "pn="+pnIndex
	rnFragment = "rn=15"
	url = baseUrl+artistIdFragment+"&"+pnFragment+"&"+rnFragment
	html = requests.get(url,timeout=20).text
	soup = BeautifulSoup(html)
	li_url_list = []
	ul_level_list = soup.find_all('ul', class_='listMusic')	
	[li_url_list.extend(item.find_all('li')) for item in ul_level_list]
	total_singer_set =set()
	for li_str in li_url_list:
		if not li_str.find('a'):
			continue
		total_singer_set.add( li_str.find_all("div",{"class":"name"})[0].text   + " : " + li_str.find_all("div",{"class":"artist"})[0].text + " : " +  li_str.a['href'])
	print "grab : "
	print total_singer_set
	print " songs \n"
	codecs.open('total_singer_url.txt', mode='ab', encoding='utf-8').writelines([ item+'\n' for item in total_singer_set])

def get_pnIndex_of_single_artist(artistId):
	baseUrl= "http://www.kuwo.cn/artist/contentMusicsAjax?"
        artistIdFragment = "artistId="+artistId
	rnFragment = "rn=15"
	url = baseUrl+artistIdFragment+"&"+rnFragment
	html = requests.get(url,timeout=20).text
	soup = BeautifulSoup(html)
	pnIndex = soup.find_all('ul', class_='listMusic')[0].attrs['data-page']		
	return pnIndex

def get_pnIndex_of_single_prefix(prefix):
	baseUrl= "http://www.kuwo.cn/artist/indexAjax?"
	categoryFragment = "category=0"
	prefixFragment = "prefix="+prefix
	url = baseUrl+categoryFragment+"&"+prefixFragment
	html = requests.get(url,timeout=20).text
	soup = BeautifulSoup(html)
	pnIndex = soup.find_all("div",{"class":"page"})[0].attrs['data-page'] 
	return  pnIndex


def getartistIds_with_prefix_pnIndex(prefix,pnIndex):
	# the category id is default 0 , means including home and overseas 	
	baseUrl= "http://www.kuwo.cn/artist/indexAjax?"
	categoryFragment = "category=0"
	prefixFragment = "prefix="+prefix
	pnIndexFragment = "pn="+pnIndex
	url = baseUrl+categoryFragment+"&"+prefixFragment+"&"+pnIndexFragment
	html = requests.get(url,timeout=20).text
	soup = BeautifulSoup(html)
	li_url_list = []
	if(len(soup.find_all('ul',class_="artistBox"))<1):
		return set()
	ul_level_list = soup.find_all('ul', class_='artistBox')[0]
	li_url_list.extend(ul_level_list.find_all("div",{"class":"artistTop"}))
        total_singer_set =set()
	#print  len(li_url_list)
        for li_str in li_url_list:
		if not li_str.find('a'):
			continue
		url =  "http://www.kuwo.cn"  +  li_str.a['href']
		html = requests.get(url,timeout=20).text
		soup = BeautifulSoup(html)
		# add length check first
		if(len(soup.find_all("div",{"class":"artistTop"}))>0):
			print soup.find_all("div",{"class":"artistTop"})[0].attrs['data-artistid']	
			total_singer_set.add(soup.find_all("div",{"class":"artistTop"})[0].attrs['data-artistid'])		
	# the total_singer_set   to be return.
	return total_singer_set	


def run():
	prefix = "Z"
	pnIndex_top = get_pnIndex_of_single_prefix(prefix)
	pnIndex_top = int(pnIndex_top)
	arr = range(pnIndex_top)
	str_arr = map(str,arr)
	for pnIndex in str_arr:
		artistId_arr = getartistIds_with_prefix_pnIndex(prefix,pnIndex)
		for artistId in artistId_arr:
			artist_pnIndex_top = get_pnIndex_of_single_artist(artistId)
			if(artist_pnIndex_top == ''): 
				continue
			artist_pnIndex_top = int(artist_pnIndex_top)
			index_arr = range(artist_pnIndex_top)
			str_index_arr = map(str,index_arr)
			for index in str_index_arr:
				analyze_single_page_with_artistId_pnIndex(artistId,index)


if __name__ == "__main__":
	run()
