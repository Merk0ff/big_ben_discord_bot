from io import BytesIO
from pathlib import Path

from datetime import time

from pydub import AudioSegment


class BigBanSampler:
    def __init__(self):
        bell = AudioSegment.from_mp3("audio/bell.mp3")
        chime = {
            '00': AudioSegment.from_mp3("audio/12.mp3"),
            '15': AudioSegment.from_mp3("audio/quarter_hour_chime.mp3"),
            '30': AudioSegment.from_mp3("audio/half_hour.mp3"),
            '45': AudioSegment.from_mp3("audio/3_quarter_hour_chime.mp3"),
        }

        self.__bells = {}

        for hour in range(1, 12):
            for k, v in chime.items():
                output = BytesIO()
                sound = v + bell * hour
                sound.export(output, format='mp3')

                self.__bells.update({
                    f'{hour}{k}': output,
                })

    def get_bell(self, t: time):
        return self.__bells[t.strftime('%-I%M')]

    def save(self, out_dir='./audio_out'):
        Path(out_dir).mkdir(parents=True, exist_ok=True)

        for k, v in self.__bells.items():
            with open(f'{out_dir}/{k}.mp3', 'wb') as f:
                f.write(v.read())
