To actually play something:

Decode a file:

./simple_decoder.py 2> foo.raw

Assuming that the ogg is originally from a CD or similar quality source, You can play it now:

aplay -f cd foo.raw

You can also convert those raw PCM samples to a wav, by providing
appropriate info:

ffmpeg -f s16le -ar 44100 -ac 2 -i foo.raw   foo.wav

You can then play that:

mplayer foo.wav

Not sure when this actually started working.
