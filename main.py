from pydub import AudioSegment

bell = AudioSegment.from_mp3("audio/bell.mp3")
oclock = AudioSegment.from_mp3("audio/12.mp3")

five_oclock = oclock + bell * 5

five_oclock.export("test.mp3", format="mp3")