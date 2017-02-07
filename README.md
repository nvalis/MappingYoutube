# MappingYoutube

This python script generates a graph of [Youtube](https://www.youtube.com) by scraping the related channels from the "about" page using `requests` and `lxml`.
The gathered data is streamed to [Gephi](https://github.com/gephi/gephi) using the [gephistreamer](https://github.com/totetmatt/GephiStreamer) library.

The scraping is coordinated by a size limited, thread-safe python `set` as the queue to keep track of the channels to explore. It makes use of multithreading and a simple history to accelerate the exploration.

![Screenshot](/MappingYoutube.png "Screenshot")
