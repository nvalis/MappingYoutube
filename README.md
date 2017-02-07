# MappingYoutube

This python script generates a graph of youtube by scraping the related channels about pages using `requests` and `lxml`.
The gathered data is streamed to [Gephi](https://github.com/gephi/gephi) using the [gephistreamer](https://github.com/totetmatt/GephiStreamer) library.

The scraping makes use of multithreading and uses a channel history to accelerate the exploration. The scraping is coordinated by a size limited, thread-safe python `set` as the queue to keep track of the channels to explore.

