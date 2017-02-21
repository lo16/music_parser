import os



with open('songs.csv', 'w') as f:
	fav_songs = []
	rem_songs = []
	
	os.chdir("D:\\music\\current playlist\\a5")

	for root, dirs, files in os.walk("."):
		for file in files:
			#add file to list
			if file.split('.')[-1] == 'mp3':
				fav_songs.append(file)

	os.chdir("D:\\music\\current playlist")

	for root, dirs, files in os.walk("."):
		for file in files:
			try:
				if file.split('.')[-1] == 'mp3' and file not in fav_songs:
					rem_songs.append(file)
			except:
				pass

	print len(fav_songs), len(rem_songs)

	for song in fav_songs:
		write_str = song + ', 1\n'
		f.write(write_str)

	for song in rem_songs:
		write_str = song + ', 0\n'
		f.write(write_str)