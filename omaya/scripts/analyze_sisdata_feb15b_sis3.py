import pandas as pd
import os
import glob
import re
import numpy

#freqs = numpy.arange(237, 283, 3)
freqs = numpy.arange(216, 283, 3)
#freqs = [219, 225, 228, 231, 234, 237, 240, 243,
#         246, 252, 255, 258, 261, 264, 267, 270, 273,
#         276, 279, 282]
#freqs = [237]

#freqs = [276]

def get_optim_bias(filename):
    fp = open(filename, 'r')
    line = fp.readline()
    dic = eval(line.strip().split('# ')[1])
    return dic

def analyze_all(lo_source='YIG'):
    lisdic = []
    for freq in freqs:
        #if freq<250:
        #    basedir = 'may19_2021'
        #else:
         #   basedir = 'may20_2021'
        basedir = 'feb15b_2022'
        fileglob = os.path.join(basedir, 'sis3_*_%sGHz_*_if0_hot.txt' % (freq))
        pat = os.path.join(basedir, 'sis3_\w+_%sGHz_(?P<power>\d+)mW_if0_hot.txt' % (freq))
        filenames = glob.glob(fileglob)
        print(fileglob, filenames)
        for filename in filenames:
            ifhot_fname = filename
            match = re.match(pat, filename)
            if match:
                power = "%s mW" % match.groupdict()['power']
            else:
                power = ""
            ifcold_fname = filename.replace('if0_hot', 'if0_cold')
            print(ifhot_fname, ifcold_fname)
            ifhot = pd.read_csv(ifhot_fname, skiprows=1)
            ifcold = pd.read_csv(ifcold_fname, skiprows=1)
            bias_dic = get_optim_bias(ifhot_fname)
            frequency = freq
            print(ifhot.columns)
            phot = ifhot.Power_0
            pcold = ifcold.Power_0
            y = phot/pcold
            TR =(46.3 - y*3.7)/(y-1)
            for i, if_freq in enumerate(ifhot.Frequency):
                dic = {}
                dic['RFFreq'] = frequency
                dic['IFFreq'] = if_freq
                dic['LOPower'] = power
                dic['TR'] = TR[i]
                dic['LOSource'] = lo_source
                dic['Vs'] = bias_dic['Vs']
                dic['Is'] = bias_dic['Is']
                dic['lopower'] = bias_dic['lopower']
                lisdic.append(dic)
    return pd.DataFrame(lisdic)


def consolidate_best_power(df, meanIF=(4, 8)):
    """
    Given a dataframe of frequencies and powers,
    keep only the data for the optimal LO power
    """
    frequencies = df.RFFreq.unique()
    for i, frequency in enumerate(frequencies):
        dff = df[df.RFFreq == frequency]
        dff2 = df[(df.RFFreq == frequency) & (df.IFFreq>=meanIF[0]) & (df.IFFreq<=meanIF[1])]
        dg = dff.groupby('LOPower')
        dgg = dff2.groupby('LOPower')
        optim_power = dgg.TR.mean().idxmin()
        if i == 0:
            dfout = dg.get_group(optim_power)
        else:
            dfout = pd.concat([dfout, dg.get_group(optim_power)], axis=0)
    return dfout

# def consolidate_best_power(df):
#     """
#     Given a dataframe of frequencies and powers,
#     keep only the data for the optimal LO power
#     """
#     frequencies = df.RFFreq.unique()
#     for i, frequency in enumerate(frequencies):
#         dff = df[df.RFFreq == frequency]
#         dg = dff.groupby('LOPower')
#         optim_power = dg.TR.mean().idxmin()
#         if i == 0:
#             dfout = dg.get_group(optim_power)
#         else:
#             dfout = pd.concat([dfout, dg.get_group(optim_power)], axis=0)
#     return dfout

        
def make_ifpowers(dfout):
    basedir = 'dec09b_2021'
    for freq in freqs:
        power = dfout[dfout.RFFreq==freq].LOPower.iloc[0]
        fname = os.path.join(basedir, 'sis3_%s_%sGHz_%s_if0_hot.txt' % (basedir, freq, power.replace(' ', '')))
        if os.path.exists(fname):
            df_hot = pd.read_csv(fname, skiprows=1)
            df_hot.rename(columns={'Power_1': 'HotPower'}, inplace=True)
            fname_cold = fname.replace('hot', 'cold')
            df_cold = pd.read_csv(fname_cold, skiprows=1)
            df_hot['ColdPower'] = df_cold.Power_1
            fname_both = fname.replace('hot', 'both')
            df_hot[['Frequency', 'HotPower', 'ColdPower']].to_csv(fname_both, index=False)
