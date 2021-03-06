# MappingYoutube

This python script generates a graph of [Youtube](https://www.youtube.com) by scraping the related channels from the "about" page using `requests` and `lxml` because unfortunately this data is not provided by the Youtube API.
The gathered data is streamed to [Gephi](https://github.com/gephi/gephi) for visualization using the [gephistreamer](https://github.com/totetmatt/GephiStreamer) library.

The scraping is coordinated by a size limited, thread-safe python `set` as the queue to keep track of the channels to explore. It makes use of multithreading and a simple history to accelerate the exploration.

![Screenshot](/MappingYoutube.png "Screenshot")

Example map created in about 14 min of scraping consisting of about 10000 channels. With the ForceAtlas 2 layout in LinLog mode one can observe different youtube communities mostly grouped around one or more central hubs (node color shows its in-degree, red is higher).

## Requirements

For data streaming to Gephi you need the [`Graph Streaming`](https://marketplace.gephi.org/plugin/graph-streaming/) plugin available in Gephis plugin manager. When installed you will need to rightclick -> start the streaming master server.