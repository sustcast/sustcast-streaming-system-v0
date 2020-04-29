import _thread
import time
import sqlite3

currentFile = ''
currentProgress = 0.0
currentPlayQueue = 0
currentArtist = ''
currentSong = ''
currentLyric = ''
currentGenre = ''

prevFile = ''
prevProgress = 0.0
prevPlayQueue = 0
prevArtist = ''
prevSong = ''
prevLyric = ''
prevGenre = ''

def getStringFromFile(path):

	s = open(path)
	msg = ''
	flg = 0

	for m in s:
		if flg == 0:
			msg = msg+m.strip()
			flg = 1
		else:
			msg = msg+"\n"+m.strip()

	return msg



def updateCurrent():
    global currentFile
    global currentProgress
    global currentPlayQueue 
    global currentArtist
    global currentSong 
    global currentLyric 
    global currentGenre
    
    global prevFile
    global prevProgress
    global prevPlayQueue 
    global prevArtist
    global prevSong 
    global prevLyric 
    global prevGenre 
    
    var = 1
    while var == 1:
        try:
            cue = getStringFromFile('/tmp/ices.cue').split('\n')

            currentFile = cue[0]
            currentProgress = cue[4]
            currentPlayQueue = cue[5]
            currentArtist = cue[6]
            currentSong = cue[7]

            if prevArtist != currentArtist :
                conn = sqlite3.connect('DB/current.db')
                command = "UPDATE CURRENT set artist = '"+currentArtist.replace("'","''")+"' where ID = 1"
                conn.execute(command)
                conn.commit()
                conn.close()

                prevArtist = currentArtist

            if prevSong != currentSong :
                conn = sqlite3.connect('DB/current.db')
                command = "UPDATE CURRENT set song = '"+currentSong.replace("'","''")+"' where ID = 1"
                conn.execute(command)
                conn.commit()
                conn.close()

                prevSong = currentSong

            if prevFile != currentFile:
                conn = sqlite3.connect('DB/current.db')
                command = "UPDATE CURRENT set filepath = '"+currentFile.replace("'","''")+"' where ID = 1"
                conn.execute(command)
                conn.commit()
                conn.close()

                prevFile = currentFile

            if prevGenre != currentGenre:
                conn = sqlite3.connect('DB/current.db')
                command = "UPDATE CURRENT set genre = '"+currentGenre+"' where ID = 1"
                conn.execute(command)
                conn.commit()
                conn.close()

                prevGenre = currentGenre

            if prevLyric != currentLyric:
                conn = sqlite3.connect('DB/current.db')
                command = "UPDATE CURRENT set lyric = '"+currentLyric.replace("'","''")+"' where ID = 1"
                conn.execute(command)
                conn.commit()
                conn.close()

                prevLyric = currentLyric

            if prevPlayQueue != currentPlayQueue:
                conn = sqlite3.connect('DB/current.db')
                command = "UPDATE CURRENT set queue = "+currentPlayQueue+" where ID = 1"
                conn.execute(command)
                conn.commit()
                conn.close()

                prevPlayQueue = currentPlayQueue

            if prevProgress != currentProgress:
                conn = sqlite3.connect('DB/current.db')
                command = "UPDATE CURRENT set progress = "+currentProgress+" where ID = 1"
                conn.execute(command)
                conn.commit()
                conn.close()

                prevProgress = currentProgress
                time.sleep(1)

        except IndexError as iex:
            time.sleep(0.1)
        except Exception as ex:
            print ("update current => "+str(ex))
#0 - filename 1-size 2-bitrate 3-time 4-progress 5-playlistnumber 6-id3 artist 7-id3 song

try:
    _thread.start_new_thread( updateCurrent, () )
    #readNews("genajjnvwev eda",alphaMeow)
except:
    print ("Error: unable to start ices thread")
var = 1
while var == 1:
    time.sleep(2)
    print(currentProgress)
    