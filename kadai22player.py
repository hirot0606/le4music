#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import wave
import time
import numpy as np
import alsaaudio
from optparse import OptionParser
from multiprocessing import Queue

BUF_SIZE = 4000
DELTA_TIME = 0.001
WRITE_BEFORE = 0.1

FRAME_DURATION = 0.1
FRAME_RATE = 10.0
FRAME_INTERVAL = 1.0 / FRAME_RATE

def __init__(self,wavfile,buf_size = BUF_SIZE,delta_time = DELTA_TIME,write_before = WRITE_BEFORE,frame_duration = FRAME_DURATION,frame_rate = FRAME_RATE,verbose = False):
	self.wavfile = wavfile
	self.buf_size = buf_size
	self.delta_time = delta_time
	self.write_before = write_before
	self.frame_duration = frame_duration
	self.frame_rate = frame_rate
	self.frame_interval = 1.0 / self.frame_rate
	self.verbose = verbose

	self.nchannels = self.wavfile.getnchannels()
	if self.verbose: print 'player: channels: %d' % (self.nchannels)
	self.sampling_rate = self.wavfile.getframerate()
	if self.verbose: print 'player: sampling_rate %d' % (self.sampling_rate)
	self.nsamples = self.wavfile.getnframes()
	if self.verbose: print 'player: number of samples: %d' % (self.nsamples)

	self.out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK)
	self.out.setchannels(self.wavefile.getnchannels())
	self.out.setrate(self.wavefile.getframerate())
	self.out.setformat(alsaaudio.PCM_FORMAT_S16_LE)
	self.out.setperiodsize(self.buf_size)

	self.buf = np.ndarray(self.buf_size)
	self.buf_pos = 0

	self.frame_size = int(self.sampling_rate * self.frame_duration)
	self.frame_shift = int(self.sampling_rate * self.frame_interval)
	self.frame = np.zeros(self.frame_size)
	self.window = np.hanning(self.frame_size)
	self.frame_replace = min(self.frame_size,self.frame_shift)
	self.queue = Queue()

def play(self,size):
	buf_remain = self.buf_size - self.buf_pos
	if buf_remain >= size:
		buf_pos0 = self.buf_pos
		self.buf_pos += size
		return self.buf[buf_pos0:self.buf_pos]
	else:
		frame = np.ndarray(size)
		frame[:buf_remain] = self.buf[self.buf_pos:]
		frame_remain = size - buf_remain
		while frame_remain > self.buf_size:
			d = self.wavfile.readframes(self.buf_size)
			self.out.write(d)
			w = np.fromstring(d,dtype = 'int16') * ( 2.0 ** -15)
			frame[-frame_remain :-frame_remain + self.buf_size] = w
			frame_remain -= self.buf_size
		if frame_remain > 0:
			d = self.wavfile.readframes(self.buf_size)
			self.out.write(d)
			self.buf = np.fromstring(d,dtype = 'int16') * (2.0 ** -15)
			frame[-frame_remain:] = self.buf[:frame_remain]
			self.buf_pos = frame_remain
		return frame

	def run(self):
		t0 = time.time()
		curren_sample = 0
		while current_sample < self.nsamples:
			t1 = time.time()
			while (t1 - t0) * self.sampling_rate - self.write_before < current_sample:
				time.sleep(self.delta_time)
				t1 = time.time()
			if self.verbose: print 'player: elapsed: %f, expected: %f' %(t1 -t0,float(current_sample) / self.sampling_rate)
			frame0 = self.play(self.frame_shift)
			if self.frame_size > self.frame_shift:
				self.frame[:self.frame_shift] = frame0[-self.frame_shift:]
				self.frame = np.roll(self.frame,-self.frame_shift)
			else:
				self.frame = frame0
			wframe = self.frame * self.window
			self.queue.put(wframe)
			current_sample += self.frame_shift
def main():
	parser = OptionParser(usage = 'usage: %prog[options] WAVFILE')
	parser.add_option('-v','-verbose',dest = 'verbose',action = 'store_true',default = False,help = 'verbose output')
	(options,args) = parser.parse_args()
	verbose = options.verbose
	if verbose: print 'verbose output mode.'
	if len(args) == 0:
		print 'no input files.'
		exit

	filename = args[0]
	if verbose: print 'filename: ' + filename
	wavefile = wave.open(filename,'r')
	p = player(wavefile,verbose = verbose)
	p.run()

if __name__ == '__main__':
	main()


















