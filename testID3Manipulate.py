from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH

# Create MP3File instance.
mp3 = MP3File('music/rck/Linkin Park-Numb.mp3')
mp3.set_version(VERSION_2)

# Get/set/del tags value.
alb = mp3.song

mp3.song = "Numb"
mp3.artist = "Linkin Park"
#mp3.genre = "SEMI_CLASSICAL"
#mp3.comment = ''

print(mp3.song)
#mp3.song = 'Fade'
#mp3.artist = 'Alan Walker'
#del mp3.album

"""
Allowed tags:

    - artist;
    - album;
    - song;
    - track;
    - comment;
    - year;
    - genre;
    - band (version 2.x);
    - composer (version 2.x);
    - copyright (version 2.x);
    - url (version 2.x);
    - publisher (version 2.x).
"""

# Get all tags.
tags = mp3.get_tags()
print(tags)

"""
Output:
{'ID3TagV1': {'song': 'Prowler', 'artist': 'Iron Maiden', 'album': 'Iron Maiden',
'year': '1980', 'comment': None, 'track': 1, 'genre': 'Other'},
'ID3TagV2': {'artist': 'Iron Maiden', 'band': 'Iron Maiden', 'album': 'Iron Maiden',
'song': 'Prowler', 'track': '1/9', 'genre': 'Heavy Metal', 'year': '1980'}}
"""

# # By default selected tags in both versions.
#mp3.set_version(VERSION_BOTH)

# # Change to 2.x version.
#mp3.set_version(VERSION_2)

# # For 1.x version
#mp3.set_version(VERSION_1)

# # After the tags are edited, you must call the save method.
mp3.save()