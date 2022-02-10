import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging
import os


class SISTestSuite(object):
	def __init__(self, directory, if_freq=6, oldBoard=True, card=2,
                 debug=True):
		logfile = datetime.datetime.now().strftime('sistest_%Y_%m_%d_%H%M.log')
    	logging.basicConfig(filename=logfile,
                        	level=logging.INFO,
                        	format='%(asctime)s %(levelname)s: %(message)s')
		if not os.path.exists(directory):
			self._print("making directory %s" % directory)
      	os.makedirs(directory)
		self.directory = directory

	def _print(self, msg, loglevel=logging.INFO, ):
		if self.debug:
			print(msg)
    logging.log(level=loglevel, msg=msg)

  def dc_iv_sweep(self, channel=0, device='3',
									vmin=-2, vmax=16, step=0.1,
									gain_Vs=80, gain_Is=200,
									timeout=0.010, off=None,
									makeplot=True, save=True):
		"""
		Function to get the IV sweep with no LO.
		"""
		self._print('Performing DC IV Sweep on channel %d device %s' % (channel, device))
		if off is None:
				off = 2
				self._print("Offset : %s" % off)
		vlist = numpy.arange(vmin, vmax+step, step)
		lisdic = []
		for Vsis in vlist:
				dic = {}
				dic['Vsis'] = Vsis
				Vs = Vsis/vmax*45*np.random.normal(loc=1,scale=0.5)
				Is = Vs/45*np.random.normal(loc=1,scale=0.5)
				dic['Vs'] = Vs
				dic['Is'] = Is
				lisdic.append(dic)
		self._print("Setting and reading channel %d to voltage: %s" % (channel, '##')
		df = pd.DataFrame(lisdic)
		if makeplot:
				figIV, axIV = plt.subplots(1,1,figsize=(8,6))
				axIV.plot(df.Vs, df.Is, 'o-', label='SIS%s cold' % device)
				axIV.legend(loc='best')
				axIV.set_xlim(0, 25)
				axIV.set_ylim(-10, 200)
				axIV.grid()
		if save:
				fname = os.path.join(self.directory, 'sis%s_cold.csv' % device)
				df.to_csv(fname)
				self._print('Saving DC IV sweep to %s' % fname)
		return df
