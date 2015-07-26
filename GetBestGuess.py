import pycurl
import re
import py4chan
from StringIO import StringIO

# Search image for testing
searchImage_1 = 'http://i.4cdn.org/a/1419119790448.jpg'

# Search image that doesn't have best guess
searchImage_2 = 'http://i.4cdn.org/a/1419089215532.jpg'

# GetBestGuess takes image url and returns Google Image Search's Best Guess
def GetBestGuess(searchImage):
	# String variable to storing html output
	storage = StringIO()
	# cURL 
	curl = pycurl.Curl()
	curl.setopt(pycurl.URL, "https://www.google.com/searchbyimage?&image_url="+searchImage)
	curl.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:8.0) Gecko/20100101 Firefox/8.0')
	# Writes cURL output to storage instead of to stdout
	curl.setopt(curl.WRITEFUNCTION, storage.write)
	curl.setopt(pycurl.FOLLOWLOCATION, True)
	# Returns raw html. Not readable
	curl.perform()
	curl.close()

	response = re.search(re.escape("italic\">")+"(.*?)"+re.escape("</a>"),storage.getvalue())
	if response:
		return response.group(1)
	else:
		return "No Guess"

def GetBoardContents(inputBoard):
	board = py4chan.Board(inputBoard)
	threadList = []
	# 4chan Boards 404 after 19 getThread iterations, due to 4chan Boards only holding
	#	up to 274 threads in a given Board. 

	# A suggested method to keep the memory usage down on this script would be to
	# read in only recent posts. Defining "recent" may be a bit tricky, as 4chan
	# boards are all different, but some common number should work.
	for x in range(2,12):
		if not threadList:
			threadList = board.getThreads(x)
		else:
			threadList = threadList + board.getThreads(x)

	threadSubjectList = []
	# Thread's first posts are known as "subjects". The subjects sometimes contain
	# a file(often picture related) or some text in an attempt to create a conversation.
	# This conversation starter is excellent to use when getting an idea of what a Thread
	# may be about.
	for thread in threadList:
		threadSubjectList.append(str(thread.topic.FileUrl))

	for index, thread in enumerate(threadSubjectList):
		threadSubjectList[index] = GetBestGuess(thread)
		print threadSubjectList[index], thread

	return threadSubjectList

def main():
	GetBoardContents('a')
	

#print GetBestGuess(searchImage_1)
#print GetBoardContents('a')
main()