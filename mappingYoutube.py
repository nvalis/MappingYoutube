#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from lxml import etree
from pprint import pprint
from queue import Queue
import threading
from urllib.parse import urlparse, urlunsplit
import time, hashlib

from gephistreamer import graph
from gephistreamer import streamer

'''
TODO:
 - logging
 - configParser
 - docstrings
'''

class Channel:
	def __init__(self, url, name):
		self.url = url
		self.id = self._generate_id(url)
		self.name = self._clean_name(name)

	def scrape(self):
		self.get_content()
		self.parse_infos()

	def get_content(self):
		r = requests.get(self.url)
		self.tree = etree.HTML(r.content)

	def _generate_id(self, url):
		return hashlib.md5(url.encode('utf-8')).hexdigest()

	def _clean_name(self, name):
		cleaned = ''.join([i if ord(i) < 128 else ' ' for i in name])
		return cleaned.replace('\t', '').replace('\n', '')

	def parse_infos(self):
		# get channel infos
		stats = [int(s.replace('.', '').replace(',', '')) for s in self.tree.xpath('//div[@class="about-stats"]/span/b/text()')]
		if len(stats) == 2:
			self.subscriptions, self.views = stats

			# clamping to prevent gephi crash ;-)
			max_int = 2**31 - 1
			if self.subscriptions > max_int: self.subscriptions = max_int
			if self.views > max_int: self.views = max_int
		else:
			print('Subscriptions or views hidden!')
			self.subscriptions = 0
			self.views = 0

		# get related channels
		related_urls  = self.tree.xpath('//h2[contains(text(),"hnliche Kan") or contains(text(),"Related Channels")]/../ul/li/span/div/h3/a/@href')
		related_names = self.tree.xpath('//h2[contains(text(),"hnliche Kan") or contains(text(),"Related Channels")]/../ul/li/span/div/h3/a/@title')
		url = urlparse(self.url)
		self.related_channels = [Channel(urlunsplit((url.scheme, url.netloc, related_urls[i]+'/about', '', '')), related_names[i]) for i in range(len(related_urls))]

	def __repr__(self):
		if 'name' in dir(self): return '<Channel \'{}\'>'.format(self.name)
		return '<Channel \'{}\'>'.format(self.url)


def scraper(queue, history):
	web_sock = streamer.GephiWS(workspace='workspace1')
	stream = streamer.Streamer(web_sock)

	def add_to_graph(origin, related):
		o_node = graph.Node(origin.id, label=origin.name, url=origin.url, subscriptions=origin.subscriptions, views=origin.views)
		stream.change_node(o_node)

		for ch in related:
			node = graph.Node(ch.id, label=ch.name, url=ch.url, subscriptions=0, views=0)
			stream.add_node(node)

			edge = graph.Edge(o_node, node)
			stream.add_edge(edge)
		stream.commit()

	while True:
		try:
			channel = queue.pop()
		except KeyError:
			continue

		print('Working on: {}'.format(channel))

		history.append(channel.id)

		channel.scrape()
		for ch in channel.related_channels:
			if ch.id in history:
				continue
			if len(queue) < 500: # limit queue size
				queue.add(ch)

		add_to_graph(channel, channel.related_channels)

def main():
	queue = set()
	history = open('nodes.csv').read().splitlines()[1:-1]
	print('Read {} history items'.format(len(history)))

	start = Channel('https://www.youtube.com/user/BuzzFeedVideo/about', 'BuzzFeedVideo') # from experience rather central node
	queue.add(start)

	for i in range(5):
	    t = threading.Thread(target=scraper, args=(queue, history))
	    t.start()

if __name__ == '__main__':
	main()