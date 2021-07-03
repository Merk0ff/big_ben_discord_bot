from datetime import time

from pydub import AudioSegment


class BigBanSampler:
    def __init__(self):
        bell = AudioSegment.from_mp3("audio/bell.mp3")
        oclock = AudioSegment.from_mp3("audio/12.mp3")
        three_quarter_hour_chime = AudioSegment.from_mp3("audio/3_quarter_hour_chime.mp3")
        half_hour_chime = AudioSegment.from_mp3("audio/half_hour.mp3")
        quarter_hour_chime = AudioSegment.from_mp3("audio/quarter_hour_chime.mp3")

        self.__bells = {}

        for hour in range(1, 12):
            self.__bells.update({
                f'{hour}00': oclock + bell * hour,
                f'{hour}15': quarter_hour_chime + bell * hour,
                f'{hour}30': half_hour_chime + bell * hour,
                f'{hour}45': three_quarter_hour_chime + bell * hour,
            })

    def get_bell(self, t: time):
        return self.__bells[t.strftime('%-I%M')]