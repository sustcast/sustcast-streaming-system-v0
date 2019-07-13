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

cue = getStringFromFile('/tmp/ices.cue').split('\n')
#0 - filename 1-size 2-bitrate 3-progress 4-playlistnumber 5-id3 artist 6-id3 song
print(cue[3])