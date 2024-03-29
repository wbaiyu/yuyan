"""
Hands-free Voice Assistant with Snowboy and Alexa Voice Service. The wake-up keyword is "alexa"

Requirement:
    sudo apt-get install python-numpy
    pip install webrtc-audio-processing
"""


import time
import logging
from voice_engine.source import Source
from voice_engine.channel_picker import ChannelPicker
from voice_engine.kws import KWS
from voice_engine.ns import NS
from doa_respeaker_v2_6mic_array import DOA
from avs.alexa import Alexa


def main():
    logging.basicConfig(level=logging.DEBUG)

    src = Source(rate=16000, channels=8)
    ch1 = ChannelPicker(channels=8, pick=1)
    ns = NS(rate=16000, channels=1)
    kws = KWS(model='alexa.pmdl')
    doa = DOA(rate=16000)
    alexa = Alexa()

    src.link(ch1)
    ch1.link(ns)
    ns.link(kws)
    kws.link(alexa)

    src.link(doa)

    def on_detected(keyword):
        logging.info('detected {} at direction {}'.format(keyword, doa.get_direction()))
        alexa.listen()

    kws.set_callback(on_detected)

    src.recursive_start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.recursive_stop()


if __name__ == '__main__':
    main()
