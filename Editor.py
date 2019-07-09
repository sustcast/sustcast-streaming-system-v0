from PyLyrics import *
import random
import os , sys
import shutil
import re
from tinytag import TinyTag
import time
import _thread
import socket
import re
import sqlite3
from datetime import datetime

#things for clarification
	#cla--classical etr--electronic fok--folk met--metal pop--pop rap--rap rck--rock scl--semi-Classical
	#EM4-8 MM8-12 EA12-16 EV16-20 NT20-24 LN0-4
	# Request status 0 -> recieved the request
	#				 1 -> prepared the song
	#				 2 -> request fulfilled 

#variables
##Environment Setup
basePath = "/home/meow-one/sustcast-streamming-system/"
##genre list
path_genre = [basePath+"music/cla/",basePath+"music/etr/",basePath+"music/fok/",basePath+"music/met/",basePath+"music/pop/",basePath+"music/rap/",basePath+"music/rck/",basePath+"music/scl/"]
numGenre = 8
genreName = ["classical","electronic" , "folk" , "metal" , "pop" , "rap" , "rock", "semi-classical"]
##NEWS
newsPath = basePath+'news/'

##streamer
icecastPass = 'alchemist'
streamName = 'sustcast'
streamDescription = 'SUSTcast is the campus radio for Shahjalal University of Science and Technology which is powered by RADIO MEOW PROJECT created by Meow Labs'
streamMountName = 'testcast'
playlistFile = 'testplaylist.txt'
icecastIP = '103.84.159.230'

#rj profiles
alphaMeow = ["en","Octavia Meow"]
betaMeow = ["en-au","Persephone Meow"]
gammaMeow = ["en-us","Genesis Meow"]
deltaMeow = ["en-uk","Aurora Meow"]
RJ = [alphaMeow,betaMeow,gammaMeow,deltaMeow]

#functions
def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()
	#replace_line('stats.txt', 0, 'Mage')

#ices -h 103.84.159.230 -P alchemist -F playlist.txt -m sustcast -d 'SUSTcast is the campus radio for Shahjalal University of Science and Technology which is powered by RADIO MEOW PROJECT created by Meow Labs' -n SUSTcast
def ices():
	cmd = 'ices -h '+icecastIP+' -P '+icecastPass+' -F '+playlistFile+' -m '+streamMountName+' -d '+streamDescription+' -n '+streamName
	#print(cmd)
	os.system(cmd)

def newsFetcher():

	global newsPath

	print "News Fetcher ==> News Fetcher alive" 
	
	var = 1
	while var == 1:
		M = int(datetime.now().strftime("%M")) #M means minute
		S = int(datetime.now().strftime("%S")) #S means second

		#print t
		#print name

		if M == 0 :
			name = datetime.now().strftime("News_%d_%m_%Y_%H.mp3")
			print ("News Fetcher ==> recording start @" + name)

			os.system ("streamripper http://bbcwssc.ic.llnwd.net/stream/bbcwssc_mp1_ws-einws -l 420 -s")

			os.system ("mv 'incomplete/ - .mp3' '"+newsPath+name+"'")

			lastNews = newsPath + name

			os.system ("cp '"+newsPath+name+"'" + " news/news.mp3")

			print ("News Fetcher ==> News recording sucessfull")

		
		M = int(datetime.now().strftime("%M"))
		S = int(datetime.now().strftime("%S"))

		slp = (60-M)*60 - S

		print ("News Fetcher ==> news fetcher Will Sleep for " + str(slp) + " Seconds")

		time.sleep(slp)

def requestFetcher():
	print "Request Fetcher ==> Request fetcher alive"

	var = 1
	while var == 1:
		try:
			rowNum = 0
			ID = -1
			song = ""
			artist = ""
			name = ""
			timeStamp = ""
			status = -1
			path = ""

			conn = sqlite3.connect('DB/request.db')
			#print "Opened request database successfully";

			cursor = conn.execute("SELECT * from REQ where STATUS = 0")
			for row in cursor:
				ID = row[0]
				name = row[1]
				song = row[2]
				artist = row[3]
				timeStamp = row[4]
				status =  row[6]

				path = searchMusicFile(song,artist)

				print "Request Fetcher ==> Got a request from "+name+" for "+artist +" " +song

				if len(path) == 0:

					print "Request Fetcher ==> Did not find requested music in Music Collection"
					print "Request Fetcher ==> Downloading....."

					music = artist + " " +song

					os.system("instantmusic -p -q -s '"+ music + "'")

					fileList = os.listdir(mainPath)
					musicFile = ""
					l = len(fileList)
					j = 0

					while j < l:

						if fileList[j].find(".mp3") > -1:
							musicFile = fileList[j]
							break

						j = j + 1

					
					path = "/home/rb101/Music/RoboFM/request/"+artist+ "-" + song+".mp3"

					os.system("sox '"+mainPath+fileList[j]+"' -C 128 -r 44100 -c 2 '"+path+"'")
					os.remove(mainPath+fileList[j])

					print "Request Fetcher ==> Downloading Completed"

				else:
					print "Request Fetcher ==> Found Requested Music in Music Collection"


				command = "UPDATE REQ set PATH = '"+path+"' where ID = "+str(ID)
				conn.execute(command)
				conn.commit()

				command = "UPDATE REQ set STATUS = 1 where ID = "+str(ID)
				conn.execute(command)
				conn.commit()


			conn.close()
			time.sleep(60)

		except Exception as ex:
			print "request fetcher == > System Down"
			print ex

		
# 		def searchMusicFile(songName,artistName):
			
# 			global numGenre
# 			global path_genre

# 			artistName = artistName.lower()
# 			songName = songName.lower()

# 			g = 0

# 			while g < numGenre:

# 				mus_list = os.listdir(path_genre[g])

# 				l = len(mus_list)

# 				i = 0

# 				while i < l:
# 					music = getMusicName(mus_list[i])

# 					art = music[0].lower()
# 					son = music[1].lower()

# 					if art == artistName and son == songName :

# 						return (path_genre[g] +"/"+ mus_list[i])

# 					i = i + 1

# 				g = g + 1


# 			mus_list = os.listdir("/home/rb101/Music/RoboFM/request/")

# 			l = len(mus_list)

# 			i = 0

# 			while i < l:
# 				music = getMusicName(mus_list[i])

# 				art = music[0].lower()
# 				son = music[1].lower()

# 				if art == artistName and son == songName :

# 					return ("/home/rb101/Music/RoboFM/request/"+ mus_list[i])

# 				i = i + 1

# 			return ""



# 		def ret_time():
# 			localtime = time.asctime(time.localtime(time.time()))
# 			hour = 0;
# 			hour = int(localtime[11]+localtime[12])
# 			return hour

# 		##text file start

# 		def user_data(tim):

# 			EM = []
# 			MM = []
# 			EA = []
# 			EV = []
# 			NT = []
# 			LN = []

# 			EMi = []
# 			MMi = []
# 			EAi = []
# 			EVi = []
# 			NTi = []
# 			LNi = []

# 			global numGenre

# 			if tim >= 0 and tim < 4:
# 				i = 0
# 				s = open("LN_data.txt")

# 				for m in s:
# 					LN.append(m.strip())

# 				while i < numGenre:	
# 					LNi.append(int(LN[i]))
# 					i = i + 1
# 				return LNi

# 			if tim >= 4 and tim < 8:
# 				i = 0
# 				s = open("EM_data.txt")

# 				for m in s:
# 					EM.append(m.strip())

# 				while i < numGenre:	
# 					EMi.append(int(EM[i]))
# 					i = i + 1
# 				return EMi
		    
# 			if tim >= 8 and tim < 12:
# 				i = 0
# 				s = open("MM_data.txt")

# 				for m in s:
# 					MM.append(m.strip())

# 				while i < numGenre:	
# 					MMi.append(int(MM[i]))
# 					i = i + 1
# 				return MMi
		    
# 			if tim >= 12 and tim < 16:
# 				i = 0
# 				s = open("EA_data.txt")

# 				for m in s:
# 					EA.append(m.strip())

# 				while i < numGenre:	
# 					EAi.append(int(EA[i]))
# 					i = i + 1
# 				return EAi
		    
# 			if tim >= 16 and tim < 20:
# 				i = 0
# 				s = open("EV_data.txt")

# 				for m in s:
# 					EV.append(m.strip())

# 				while i < numGenre:	
# 					EVi.append(int(EV[i]))
# 					i = i + 1
# 				return EVi
		    
# 			if tim >= 20 and tim <= 23:
# 				i = 0
# 				s = open("NT_data.txt")

# 				for m in s:
# 					NT.append(m.strip())

# 				while i < numGenre:	
# 					NTi.append(int(NT[i]))
# 					i = i + 1
# 				return NTi


# 		##text file end

# 		## roulette wheel genre

# 		def roulette(ls):
# 			i = 1
# 			l = numGenre

# 			while i < l :
# 				ls[i] = ls[i] + ls[i-1]
# 				i = i + 1
			
			
# 			r = random.randint(0,ls[l-1]-1)
			
# 			#print ls	

# 			i = 0
# 			while i < l:
# 				if r < ls[i]:
# 				  return i
				
# 				i = i + 1


# 		##

# 		def getStringFromFile(path):

# 			s = open(path)
# 			msg = ''
# 			flg = 0

# 			for m in s:
# 				if flg == 0:
# 					msg = msg+m.strip()
# 					flg = 1
# 				else:
# 					msg = msg+"\n"+m.strip()

# 			return msg

# 		def writeFile(string,path):
# 			file = open(path,'w')
# 			file.write(string)
# 			file.close

# 		def readNews(songSpeech,rj):

# 			global newsPath
# 			newsList = os.listdir(newsPath)

# 			l = len(newsList)

# 			while l > 0:

# 				l = l - 1

# 				if newsList[l] == "news.mp3":
# 					print "news preparing"

# 					speech = "Hello listeners, Its RJ MockingJay Meow. You are listening to Radio Meow one O one point five FM. Now you will listen to the latest bulletin from BBC World Services."

# 					os.system("gtts-cli '"+ speech +"' -l '"+rj[0]+"' -o /home/rb101/Music/RoboFM/buffer/rjTemp.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/rjTemp.mp3 -C 128 -r 44100 -c 2 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/silence5.mp3 -C 128 -r 44100 -c 2 /home/rb101/Music/RoboFM/buffer/silence55.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/silence55.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp2.mp3")

# 					os.system("sox /home/rb101/Music/RoboFM/news/news.mp3 -C 128 -r 44100 -c 2 /home/rb101/Music/RoboFM/news/newsTemp.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/rjTemp2.mp3 /home/rb101/Music/RoboFM/news/newsTemp.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp3.mp3")
					
# 					os.system("gtts-cli '"+ songSpeech +"' -l '"+rj[0]+"' -o /home/rb101/Music/RoboFM/buffer/rjTemp.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/rjTemp.mp3 -C 128 -r 44100 -c 2 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/silence5.mp3 -C 128 -r 44100 -c 2 /home/rb101/Music/RoboFM/buffer/silence55.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/silence55.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp2.mp3")

# 					os.system("sox /home/rb101/Music/RoboFM/buffer/rjTemp3.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp2.mp3 /home/rb101/Music/RoboFM/buffer/rj.mp3")

# 					os.remove("/home/rb101/Music/RoboFM/news/news.mp3")

# 					print "news prepared"

# 					return 1


# 			return 0

# 		def fulfilReq(songSpeech,rj):

# 			retRj = ["0","0","0","0"]

# 			conn = sqlite3.connect('/home/rb101/Dropbox/RadioMeow/DB/request.db')
# 					#print "Opened request database successfully";

# 			cursor = conn.execute("SELECT * from REQ where STATUS = 1")
# 			for row in cursor:
# 				ID = row[0]
# 				name = row[1]
# 				song = row[2]
# 				artist = row[3]
# 				timeStamp = row[4]
# 				path = row[5]
# 				status =  row[6]
# 				lyric = ""

# 				print "Got a unfulfiled Request and the requested song is already downloaded"

# 				speech = "Hello listeners, Its RJ MockingJay Meow. You are listening to Radio Meow one O one point five FM. We just recieved a song request from " + name +" with love. Now you will listen to " +song+" by "+ artist+"."

# 				os.system("gtts-cli '"+ speech +"' -l '"+rj[0]+"' -o /home/rb101/Music/RoboFM/buffer/rjTemp.mp3")
# 				os.system("sox /home/rb101/Music/RoboFM/buffer/rjTemp.mp3 -C 128 -r 44100 -c 2 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3")
# 				os.system("sox /home/rb101/Music/RoboFM/buffer/silence5.mp3 -C 128 -r 44100 -c 2 /home/rb101/Music/RoboFM/buffer/silence55.mp3")
# 				os.system("sox /home/rb101/Music/RoboFM/buffer/silence55.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp2.mp3")

# 				os.system("sox /home/rb101/Music/RoboFM/buffer/rjTemp2.mp3 '"+path+"' /home/rb101/Music/RoboFM/buffer/rjTemp3.mp3")
				
# 				os.system("gtts-cli '"+ songSpeech +"' -l '"+rj[0]+"' -o /home/rb101/Music/RoboFM/buffer/rjTemp.mp3")
# 				os.system("sox /home/rb101/Music/RoboFM/buffer/rjTemp.mp3 -C 128 -r 44100 -c 2 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3")
# 				os.system("sox /home/rb101/Music/RoboFM/buffer/silence5.mp3 -C 128 -r 44100 -c 2 /home/rb101/Music/RoboFM/buffer/silence55.mp3")
# 				os.system("sox /home/rb101/Music/RoboFM/buffer/silence55.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp2.mp3")

# 				os.system("sox /home/rb101/Music/RoboFM/buffer/rjTemp3.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp2.mp3 /home/rb101/Music/RoboFM/buffer/rj.mp3")

# 				print "REQ RJ prepared"

# 				try:
# 					lyric = PyLyrics.getLyrics(artist,song)
# 					lyric = lyric.replace("\n","$")
			
# 					if lyric.find("<") > -1:
# 						lyric = ""
# 					#print lyric

# 				except:
# 					print "no lyrics found"


# 				retRj[0] = "REQ"
# 				retRj[1] = artist
# 				retRj[2] = song
# 				retRj[3] = lyric

# 				command = "UPDATE REQ set STATUS = 2 where ID = "+str(ID)
# 				conn.execute(command)
# 				conn.commit()

# 				conn.close()

# 				return retRj

# 			return retRj





# 		def getMusicName(musicFileName):
			
# 			music = ["",""]
# 			musicName = musicFileName.replace(".mp3", "")


# 			#print musicName

# 			i = musicName.find("-")

# 			j = 0
# 			while j < i:
# 				music[0] = music[0] + musicName[j]
# 				j = j+1

# 			l = len(musicName)
# 			j = j+1
# 			while j < l:
# 				music[1] = music[1] + musicName[j]
# 				j = j+1

# 			#print music[0]
# 			#print music[1]

# 			return music

# 		def getSpeechOfRj(songName,artistName,rj):

# 			speech = "You are listening to Radio Meow one O one point Five FM. Hey, its RJ " + rj[1] +". Now, You will listen to "+songName+" by " + artistName 
# 			return speech

# 		def speechOfRj(musicFileName):
			
# 			global RJ

# 			music = getMusicName(musicFileName)
			
			
# 			songName = music[1]
# 			artistName = music[0]

# 			l = len(RJ)
# 			r = random.randint(0,l-1)
# 			rj = RJ[r]

# 			speech = getSpeechOfRj(songName,artistName,rj)

# 			flgNews = readNews(speech,rj)

# 			if flgNews == 0:

# 				rjReq = fulfilReq(speech,rj)

# 				if rjReq[0] == "0":

# 					os.system("gtts-cli '"+ speech +"' -l '"+rj[0]+"' -o /home/rb101/Music/RoboFM/buffer/rjTemp.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/rjTemp.mp3 -C 128 -r 44100 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/silence5.mp3 -C 128 -r 44100 /home/rb101/Music/RoboFM/buffer/silence55.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/silence55.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3 /home/rb101/Music/RoboFM/buffer/rj.mp3")

# 					return rj

# 				return rjReq

# 			rj = ["news","news"]

# 			return rj
			

# 			#gtts-cli "Hello" -l 'en' -o hello.mp3


# 		def getLyrics(musicFileName , genreName):
# 			music = getMusicName(musicFileName)
			
# 			rowNum = 0;
# 			songName = music[1]
# 			artistName = music[0]

# 			ID = -1
# 			song = ""
# 			artist = ""
# 			genre = ""
# 			lyric =  ""

# 			conn = sqlite3.connect('/home/rb101/Dropbox/RadioMeow/DB/music.db')
# 			print "Opened music database for lyrics successfully";

# 			cursor = conn.execute("SELECT * from MUSIC where song = '"+songName+"' AND artist = '" + artistName + "'")
# 			for row in cursor:
# 				ID = row[0]
# 				song = row[1]
# 				artist = row[2]
# 				genre = row[3]
# 				lyric =  row[4]

# 				rowNum = rowNum + 1

# 			if rowNum == 0:

# 				print "Did not found data in database. Searching....."
# 				try:
# 					lyric = PyLyrics.getLyrics(artistName,songName)
# 					lyric = lyric.replace("'","''")
# 					#print lyric

# 				except:
# 					print "no lyrics found"


# 				command = "INSERT INTO MUSIC (song,artist,genre,lyric) VALUES ('" + songName + "', '"+artistName+"','"+ genreName+"', '"+ lyric +"' )"
# 				#print command
# 				conn.execute(command);
# 				conn.commit()

# 			#time.sleep(20)
# 			if len(lyric) > 0:
# 				print "lyrics found"
				
# 			conn.close()
# 			return lyric

def mainGenjam():
	try:
		_thread.start_new_thread( ices, () )
	except:
		print ("Error: unable to start ices thread")
	time.sleep(100000)

mainGenjam()
# inf = 1
# while inf == 1:
# 	print ("Initiating EDITOR")
# 	print ("Initiating Communication With Ices 0.4")

# 	try:
# 		_thread.start_new_thread( ices, () )
		
# 	except:
# 		print ("Error: unable to start thread")
# while inf == 1:

# 	try:

# 		#cla--classical etr--electronic fok--folk met--metal pop--pop rap--rap rck--rock scl--semi-Classical

# 		#EM4-8 MM8-12 EA12-16 EV16-20 NT20-24 LN0-4 

# 		print "Initiating EDITOR"
# 		print "Initiating Communication With Streamer"

# 		#genre list
# 		path_genre = ["/home/rb101/Music/RoboFM/cla","/home/rb101/Music/RoboFM/etr","/home/rb101/Music/RoboFM/fok","/home/rb101/Music/RoboFM/met","/home/rb101/Music/RoboFM/pop","/home/rb101/Music/RoboFM/rap","/home/rb101/Music/RoboFM/rck","/home/rb101/Music/RoboFM/scl"]
# 		numGenre = 8
# 		genreName = ["classical","electronic" , "folk" , "metal" , "pop" , "rap" , "rock", "semi-classical"]
# 		#socket 

# 		token = "qa7sd98sa7dsj1878usdjljasidjoas89078907"
# 		streamerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 		host = socket.gethostname()
# 		port = 50000

# 		streamerSocket.connect((host,port))

# 		streamerSocket.sendall(token + '\n')
# 		inputStreamer = streamerSocket.recv(1024)
# 		print inputStreamer

# 		HDSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 		HDhost = socket.gethostname()
# 		HDport = 50003

# 		HDSocket.connect((HDhost,HDport))

# 		HDSocket.sendall(token + '\n')
# 		inputHD = HDSocket.recv(1024)
# 		print inputHD


# 		#rj profiles
# 		alphaMeow = ["en","Alpha Meow"]
# 		epsilonMeow = ["en-au","Epsilon Meow"]
# 		genesisMeow = ["en-us","Genesis Meow"]
# 		auroraMeow = ["en-uk","Aurora Meow"]

# 		RJ = [alphaMeow,epsilonMeow,genesisMeow,auroraMeow]

# 		#NEWS
# 		newsPath = "/home/rb101/Music/RoboFM/news/"
# 		##main


# 		def newsFetcher():

# 			global newsPath

# 			print "News Fetcher ==> News Fetcher alive" 
			
# 			var = 1
# 			while var == 1:
# 				M = int(datetime.now().strftime("%M"))
# 				S = int(datetime.now().strftime("%S"))

# 				#print t
# 				#print name

# 				if M == 0 :
# 					name = datetime.now().strftime("News_%d_%m_%Y_%H.mp3")
# 					print "News Fetcher ==> recording start @" + name

# 					os.system ("streamripper http://bbcwssc.ic.llnwd.net/stream/bbcwssc_mp1_ws-einws -l 420 -s")

# 					os.system ("mv '/home/rb101/Dropbox/RadioMeow/incomplete/ - .mp3' '"+newsPath+name+"'")

# 					lastNews = newsPath + name

# 					os.system ("cp '"+newsPath+name+"'" + " /home/rb101/Music/RoboFM/news/news.mp3")



# 					print "News Fetcher ==> News recording succesfull"

				
# 				M = int(datetime.now().strftime("%M"))
# 				S = int(datetime.now().strftime("%S"))

# 				slp = (60-M)*60 - S

# 				print "News Fetcher ==> news fetcher Will Sleep for " + str(slp) + " Seconds"

# 				time.sleep(slp)

		
# 		def requestFetcher():

# 			print "Request Fetcher ==> Request fetcher alive"

# 			var = 1

# 			while var == 1:

# 				try:

# 					rowNum = 0
# 					ID = -1
# 					song = ""
# 					artist = ""
# 					name = ""
# 					timeStamp = ""
# 					status = -1
# 					path = ""

# 					mainPath = "/home/rb101/Dropbox/RadioMeow/"

# 					conn = sqlite3.connect('/home/rb101/Dropbox/RadioMeow/DB/request.db')
# 					#print "Opened request database successfully";

# 					cursor = conn.execute("SELECT * from REQ where STATUS = 0")
# 					for row in cursor:
# 						ID = row[0]
# 						name = row[1]
# 						song = row[2]
# 						artist = row[3]
# 						timeStamp = row[4]
# 						status =  row[6]

# 						path = searchMusicFile(song,artist)

# 						print "Request Fetcher ==> Got a request from "+name+" for "+artist +" " +song

# 						if len(path) == 0:

# 							print "Request Fetcher ==> Did not find requested music in Music Collection"
# 							print "Request Fetcher ==> Downloading....."

# 							music = artist + " " +song

# 							os.system("instantmusic -p -q -s '"+ music + "'")

# 							fileList = os.listdir(mainPath)
# 							musicFile = ""
# 							l = len(fileList)
# 							j = 0

# 							while j < l:

# 								if fileList[j].find(".mp3") > -1:
# 									musicFile = fileList[j]
# 									break

# 								j = j + 1
		
							
# 							path = "/home/rb101/Music/RoboFM/request/"+artist+ "-" + song+".mp3"

# 							os.system("sox '"+mainPath+fileList[j]+"' -C 128 -r 44100 -c 2 '"+path+"'")
# 							os.remove(mainPath+fileList[j])

# 							print "Request Fetcher ==> Downloading Completed"

# 						else:
# 							print "Request Fetcher ==> Found Requested Music in Music Collection"


# 						command = "UPDATE REQ set PATH = '"+path+"' where ID = "+str(ID)
# 						conn.execute(command)
# 						conn.commit()

# 						command = "UPDATE REQ set STATUS = 1 where ID = "+str(ID)
# 						conn.execute(command)
# 						conn.commit()


# 					conn.close()
# 					time.sleep(60)

# 				except Exception as ex:
# 					print "request fetcher == > System Down"
# 					print ex

		
# 		def searchMusicFile(songName,artistName):
			
# 			global numGenre
# 			global path_genre

# 			artistName = artistName.lower()
# 			songName = songName.lower()

# 			g = 0

# 			while g < numGenre:

# 				mus_list = os.listdir(path_genre[g])

# 				l = len(mus_list)

# 				i = 0

# 				while i < l:
# 					music = getMusicName(mus_list[i])

# 					art = music[0].lower()
# 					son = music[1].lower()

# 					if art == artistName and son == songName :

# 						return (path_genre[g] +"/"+ mus_list[i])

# 					i = i + 1

# 				g = g + 1


# 			mus_list = os.listdir("/home/rb101/Music/RoboFM/request/")

# 			l = len(mus_list)

# 			i = 0

# 			while i < l:
# 				music = getMusicName(mus_list[i])

# 				art = music[0].lower()
# 				son = music[1].lower()

# 				if art == artistName and son == songName :

# 					return ("/home/rb101/Music/RoboFM/request/"+ mus_list[i])

# 				i = i + 1

# 			return ""



# 		def ret_time():
# 			localtime = time.asctime(time.localtime(time.time()))
# 			hour = 0;
# 			hour = int(localtime[11]+localtime[12])
# 			return hour

# 		##text file start

# 		def user_data(tim):

# 			EM = []
# 			MM = []
# 			EA = []
# 			EV = []
# 			NT = []
# 			LN = []

# 			EMi = []
# 			MMi = []
# 			EAi = []
# 			EVi = []
# 			NTi = []
# 			LNi = []

# 			global numGenre

# 			if tim >= 0 and tim < 4:
# 				i = 0
# 				s = open("LN_data.txt")

# 				for m in s:
# 					LN.append(m.strip())

# 				while i < numGenre:	
# 					LNi.append(int(LN[i]))
# 					i = i + 1
# 				return LNi

# 			if tim >= 4 and tim < 8:
# 				i = 0
# 				s = open("EM_data.txt")

# 				for m in s:
# 					EM.append(m.strip())

# 				while i < numGenre:	
# 					EMi.append(int(EM[i]))
# 					i = i + 1
# 				return EMi
		    
# 			if tim >= 8 and tim < 12:
# 				i = 0
# 				s = open("MM_data.txt")

# 				for m in s:
# 					MM.append(m.strip())

# 				while i < numGenre:	
# 					MMi.append(int(MM[i]))
# 					i = i + 1
# 				return MMi
		    
# 			if tim >= 12 and tim < 16:
# 				i = 0
# 				s = open("EA_data.txt")

# 				for m in s:
# 					EA.append(m.strip())

# 				while i < numGenre:	
# 					EAi.append(int(EA[i]))
# 					i = i + 1
# 				return EAi
		    
# 			if tim >= 16 and tim < 20:
# 				i = 0
# 				s = open("EV_data.txt")

# 				for m in s:
# 					EV.append(m.strip())

# 				while i < numGenre:	
# 					EVi.append(int(EV[i]))
# 					i = i + 1
# 				return EVi
		    
# 			if tim >= 20 and tim <= 23:
# 				i = 0
# 				s = open("NT_data.txt")

# 				for m in s:
# 					NT.append(m.strip())

# 				while i < numGenre:	
# 					NTi.append(int(NT[i]))
# 					i = i + 1
# 				return NTi


# 		##text file end

# 		## roulette wheel genre

# 		def roulette(ls):
# 			i = 1
# 			l = numGenre

# 			while i < l :
# 				ls[i] = ls[i] + ls[i-1]
# 				i = i + 1
			
			
# 			r = random.randint(0,ls[l-1]-1)
			
# 			#print ls	

# 			i = 0
# 			while i < l:
# 				if r < ls[i]:
# 				  return i
				
# 				i = i + 1


# 		##

# 		def getStringFromFile(path):

# 			s = open(path)
# 			msg = ''
# 			flg = 0

# 			for m in s:
# 				if flg == 0:
# 					msg = msg+m.strip()
# 					flg = 1
# 				else:
# 					msg = msg+"\n"+m.strip()

# 			return msg

# 		def writeFile(string,path):
# 			file = open(path,'w')
# 			file.write(string)
# 			file.close

# 		def readNews(songSpeech,rj):

# 			global newsPath
# 			newsList = os.listdir(newsPath)

# 			l = len(newsList)

# 			while l > 0:

# 				l = l - 1

# 				if newsList[l] == "news.mp3":
# 					print "news preparing"

# 					speech = "Hello listeners, Its RJ MockingJay Meow. You are listening to Radio Meow one O one point five FM. Now you will listen to the latest bulletin from BBC World Services."

# 					os.system("gtts-cli '"+ speech +"' -l '"+rj[0]+"' -o /home/rb101/Music/RoboFM/buffer/rjTemp.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/rjTemp.mp3 -C 128 -r 44100 -c 2 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/silence5.mp3 -C 128 -r 44100 -c 2 /home/rb101/Music/RoboFM/buffer/silence55.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/silence55.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp2.mp3")

# 					os.system("sox /home/rb101/Music/RoboFM/news/news.mp3 -C 128 -r 44100 -c 2 /home/rb101/Music/RoboFM/news/newsTemp.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/rjTemp2.mp3 /home/rb101/Music/RoboFM/news/newsTemp.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp3.mp3")
					
# 					os.system("gtts-cli '"+ songSpeech +"' -l '"+rj[0]+"' -o /home/rb101/Music/RoboFM/buffer/rjTemp.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/rjTemp.mp3 -C 128 -r 44100 -c 2 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/silence5.mp3 -C 128 -r 44100 -c 2 /home/rb101/Music/RoboFM/buffer/silence55.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/silence55.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp2.mp3")

# 					os.system("sox /home/rb101/Music/RoboFM/buffer/rjTemp3.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp2.mp3 /home/rb101/Music/RoboFM/buffer/rj.mp3")

# 					os.remove("/home/rb101/Music/RoboFM/news/news.mp3")

# 					print "news prepared"

# 					return 1


# 			return 0

# 		def fulfilReq(songSpeech,rj):

# 			retRj = ["0","0","0","0"]

# 			conn = sqlite3.connect('/home/rb101/Dropbox/RadioMeow/DB/request.db')
# 					#print "Opened request database successfully";

# 			cursor = conn.execute("SELECT * from REQ where STATUS = 1")
# 			for row in cursor:
# 				ID = row[0]
# 				name = row[1]
# 				song = row[2]
# 				artist = row[3]
# 				timeStamp = row[4]
# 				path = row[5]
# 				status =  row[6]
# 				lyric = ""

# 				print "Got a unfulfiled Request and the requested song is already downloaded"

# 				speech = "Hello listeners, Its RJ MockingJay Meow. You are listening to Radio Meow one O one point five FM. We just recieved a song request from " + name +" with love. Now you will listen to " +song+" by "+ artist+"."

# 				os.system("gtts-cli '"+ speech +"' -l '"+rj[0]+"' -o /home/rb101/Music/RoboFM/buffer/rjTemp.mp3")
# 				os.system("sox /home/rb101/Music/RoboFM/buffer/rjTemp.mp3 -C 128 -r 44100 -c 2 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3")
# 				os.system("sox /home/rb101/Music/RoboFM/buffer/silence5.mp3 -C 128 -r 44100 -c 2 /home/rb101/Music/RoboFM/buffer/silence55.mp3")
# 				os.system("sox /home/rb101/Music/RoboFM/buffer/silence55.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp2.mp3")

# 				os.system("sox /home/rb101/Music/RoboFM/buffer/rjTemp2.mp3 '"+path+"' /home/rb101/Music/RoboFM/buffer/rjTemp3.mp3")
				
# 				os.system("gtts-cli '"+ songSpeech +"' -l '"+rj[0]+"' -o /home/rb101/Music/RoboFM/buffer/rjTemp.mp3")
# 				os.system("sox /home/rb101/Music/RoboFM/buffer/rjTemp.mp3 -C 128 -r 44100 -c 2 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3")
# 				os.system("sox /home/rb101/Music/RoboFM/buffer/silence5.mp3 -C 128 -r 44100 -c 2 /home/rb101/Music/RoboFM/buffer/silence55.mp3")
# 				os.system("sox /home/rb101/Music/RoboFM/buffer/silence55.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp2.mp3")

# 				os.system("sox /home/rb101/Music/RoboFM/buffer/rjTemp3.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp2.mp3 /home/rb101/Music/RoboFM/buffer/rj.mp3")

# 				print "REQ RJ prepared"

# 				try:
# 					lyric = PyLyrics.getLyrics(artist,song)
# 					lyric = lyric.replace("\n","$")
			
# 					if lyric.find("<") > -1:
# 						lyric = ""
# 					#print lyric

# 				except:
# 					print "no lyrics found"


# 				retRj[0] = "REQ"
# 				retRj[1] = artist
# 				retRj[2] = song
# 				retRj[3] = lyric

# 				command = "UPDATE REQ set STATUS = 2 where ID = "+str(ID)
# 				conn.execute(command)
# 				conn.commit()

# 				conn.close()

# 				return retRj

# 			return retRj





# 		def getMusicName(musicFileName):
			
# 			music = ["",""]
# 			musicName = musicFileName.replace(".mp3", "")


# 			#print musicName

# 			i = musicName.find("-")

# 			j = 0
# 			while j < i:
# 				music[0] = music[0] + musicName[j]
# 				j = j+1

# 			l = len(musicName)
# 			j = j+1
# 			while j < l:
# 				music[1] = music[1] + musicName[j]
# 				j = j+1

# 			#print music[0]
# 			#print music[1]

# 			return music

# 		def getSpeechOfRj(songName,artistName,rj):

# 			speech = "You are listening to Radio Meow one O one point Five FM. Hey, its RJ " + rj[1] +". Now, You will listen to "+songName+" by " + artistName 
# 			return speech

# 		def speechOfRj(musicFileName):
			
# 			global RJ

# 			music = getMusicName(musicFileName)
			
			
# 			songName = music[1]
# 			artistName = music[0]

# 			l = len(RJ)
# 			r = random.randint(0,l-1)
# 			rj = RJ[r]

# 			speech = getSpeechOfRj(songName,artistName,rj)

# 			flgNews = readNews(speech,rj)

# 			if flgNews == 0:

# 				rjReq = fulfilReq(speech,rj)

# 				if rjReq[0] == "0":

# 					os.system("gtts-cli '"+ speech +"' -l '"+rj[0]+"' -o /home/rb101/Music/RoboFM/buffer/rjTemp.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/rjTemp.mp3 -C 128 -r 44100 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/silence5.mp3 -C 128 -r 44100 /home/rb101/Music/RoboFM/buffer/silence55.mp3")
# 					os.system("sox /home/rb101/Music/RoboFM/buffer/silence55.mp3 /home/rb101/Music/RoboFM/buffer/rjTemp1.mp3 /home/rb101/Music/RoboFM/buffer/rj.mp3")

# 					return rj

# 				return rjReq

# 			rj = ["news","news"]

# 			return rj
			

# 			#gtts-cli "Hello" -l 'en' -o hello.mp3


# 		def getLyrics(musicFileName , genreName):
# 			music = getMusicName(musicFileName)
			
# 			rowNum = 0;
# 			songName = music[1]
# 			artistName = music[0]

# 			ID = -1
# 			song = ""
# 			artist = ""
# 			genre = ""
# 			lyric =  ""

# 			conn = sqlite3.connect('/home/rb101/Dropbox/RadioMeow/DB/music.db')
# 			print "Opened music database for lyrics successfully";

# 			cursor = conn.execute("SELECT * from MUSIC where song = '"+songName+"' AND artist = '" + artistName + "'")
# 			for row in cursor:
# 				ID = row[0]
# 				song = row[1]
# 				artist = row[2]
# 				genre = row[3]
# 				lyric =  row[4]

# 				rowNum = rowNum + 1

# 			if rowNum == 0:

# 				print "Did not found data in database. Searching....."
# 				try:
# 					lyric = PyLyrics.getLyrics(artistName,songName)
# 					lyric = lyric.replace("'","''")
# 					#print lyric

# 				except:
# 					print "no lyrics found"


# 				command = "INSERT INTO MUSIC (song,artist,genre,lyric) VALUES ('" + songName + "', '"+artistName+"','"+ genreName+"', '"+ lyric +"' )"
# 				#print command
# 				conn.execute(command);
# 				conn.commit()

# 			#time.sleep(20)
# 			if len(lyric) > 0:
# 				print "lyrics found"
				
# 			conn.close()
# 			return lyric




# 		def debug():
# 			i = 0 
# 			l = 10000
# 			rab = 0
# 			naz = 0
# 			ind = 0
# 			bpp = 0
# 			bfk = 0
# 			brk = 0
# 			wes = 0
# 			erk = 0
# 			epp = 0
# 			erp = 0
# 			jpp = 0

# 			while i < l:
			
# 				rt = ret_time()
# 				ls = user_data(rt)
# 				genre =  roulette(ls)

# 				#print rt
# 				#print ls
			
# 				if genre == 0 :
# 					rab = rab + 1
# 				if genre == 1 :
# 					naz = naz + 1
# 				if genre == 2 :
# 					ind = ind + 1
# 				if genre == 3 :
# 					bpp = bpp + 1
# 				if genre == 4 :
# 					bfk = bfk + 1
# 				if genre == 5 :
# 					brk = brk + 1
# 				if genre == 6 :
# 					wes = wes + 1
# 				if genre == 7 :
# 					erk = erk + 1
# 				if genre == 8 :
# 					epp = epp + 1
# 				if genre == 9 :
# 					erp = erp + 1
# 				if genre == 10 :
# 					jpp = jpp + 1


# 				print "rab = " + str(rab) + "\n"
# 				print "naz = " + str(naz) + "\n"
# 				print "ind = " + str(ind) + "\n"
# 				print "bpp = " + str(bpp) + "\n"
# 				print "bfk = " + str(bfk) + "\n"
# 				print "brk = " + str(brk) + "\n"
# 				print "wes = " + str(wes) + "\n"
# 				print "erk = " + str(erk) + "\n"
# 				print "epp = " + str(epp) + "\n"
# 				print "erp = " + str(erp) + "\n"
# 				print "jpp = " + str(jpp) + "\n"

# 				i = i + 1

# 		###########################################################
# 		###main
# 		###########################################################

# 		var = 1
# 		flg = 1
# 		thread.start_new_thread(newsFetcher,())
# 		thread.start_new_thread(requestFetcher,())

# 		while var == 1 :

# 			rt = ret_time()
# 			ls = user_data(rt)
# 			genre =  roulette(ls)
# 			mus_list = os.listdir(path_genre[genre])
			
# 			#print genre
			
# 			l = len(mus_list)
# 			i = 0
# 			r = random.randint(0,l-1)

# 			#print r

# 			################

# 			rj = speechOfRj(mus_list[r])

# 			music = getMusicName(mus_list[r])
			
# 			lyric = getLyrics(mus_list[r],genreName[genre])
# 			lyric = lyric.replace("\n","$")
			
# 			if lyric.find("<") > -1:
# 				lyric = ""

			
# 			if flg == 0:
# 				inputStreamer = streamerSocket.recv(1024)
# 				print inputStreamer

# 		###########

# 			if rj[0] == "news":

# 				HDSocket.sendall("<artist>Latest news from BBC World Service" + '\n')
# 				HDSocket.sendall("<song>News Bulletin"+'\n')
# 				HDSocket.sendall("<genre>RJ" + '\n')
# 				HDSocket.sendall("<lyric>" +'\n')

# 			elif rj[0] == "REQ":
# 				HDSocket.sendall("<artist>" +rj[1]+ '\n')
# 				HDSocket.sendall("<song>"+rj[2]+'\n')
# 				HDSocket.sendall("<genre>listener request" + '\n')
# 				HDSocket.sendall("<lyric>" +rj[3]+'\n')

# 			else:

# 				HDSocket.sendall("<artist>" + '\n')
# 				HDSocket.sendall("<song>RJ " + rj[1] + '\n')
# 				HDSocket.sendall("<genre>RJ" + '\n')
# 				HDSocket.sendall("<lyric>" +'\n')


# 			path = "/home/rb101/Music/RoboFM/buffer/rj.mp3"
			
# 			streamerSocket.sendall(path + '\n')
# 			inputStreamer = streamerSocket.recv(1024)
# 			print inputStreamer

# 			path = path_genre[genre]+"/"+mus_list[r]
# 			print "playing " + path

# 			#print lyric

# 			HDSocket.sendall("<artist>Artist: " + music[0] + '\n')

# 			HDSocket.sendall("<song>" + music[1] + '\n')

# 			HDSocket.sendall("<genre>" + genreName[genre] + '\n')

# 			HDSocket.sendall("<lyric>" + lyric + '\n')


# 			streamerSocket.sendall(path + '\n')
# 			flg = 0


# 	except Exception as ex:
# 		print "System Down"
# 		print ex
# 		timeRemain = 20
		
# 		while timeRemain >= 0:
			
# 			print timeRemain
# 			timeRemain = timeRemain - 1
# 			time.sleep(1)