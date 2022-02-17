import pandas as pd
import numpy
import os

def analyze_sb_for_lo(basedir, lofreq, lowest_IF=3):
    #offsets for each channel:
    off_left = 0.021
    off_right = 0.023
    basename = os.path.join(basedir, "sideband_lo_%sGHz_" % (lofreq))
    dfboth = pd.read_csv(basename + "both_on.csv")
    dfboth['Left'] = dfboth['Left'] - off_left
    dfboth['Right'] = -(dfboth['Right']-off_right)
    df3 = pd.read_csv(basename + "one_on_two_max.csv")
    df4 = pd.read_csv(basename + "one_max_two_on.csv")
    dfboth['Left3'] = df3['Left'] - off_left
    dfboth['Right3'] = -(df3['Right'] - off_right)
    dfboth['Left4'] = df4['Left'] - off_left
    dfboth['Right4'] = -(df4['Right'] - off_right)
    #return dfboth

    raw_sb_ratios = []
    corr3s = []
    corr4s = []
    avg_corrs = []
    sb_ratios = []
    db_sb_ratios = []
    iffreqs = []
    db_sb_ratio_reals = []
    for i, freq in enumerate(dfboth.Freq):
        corr3 = dfboth.Left3.iloc[i]/dfboth.Right3.iloc[i]
        corr4 = dfboth.Left4.iloc[i]/dfboth.Right4.iloc[i]
        avg_corr = (corr3 + corr4)/2.0
        if freq < lofreq:
            raw_sb_ratio = dfboth.Left.iloc[i]/dfboth.Right.iloc[i]
            sb_ratio = raw_sb_ratio/avg_corr
        else:
            raw_sb_ratio = dfboth.Right.iloc[i]/dfboth.Left.iloc[i]
            sb_ratio = raw_sb_ratio * avg_corr
        raw_sb_ratios.append(raw_sb_ratio)
        db_sb_ratio = 10 * numpy.log10(sb_ratio)
        corr3s.append(corr3)
        corr4s.append(corr4)
        avg_corrs.append(avg_corr)
        sb_ratios.append(sb_ratio)
        db_sb_ratios.append(db_sb_ratio)
        iffreqs.append(freq - lofreq)
        if abs(lofreq - freq) < lowest_IF:
            db_sb_ratio_reals.append(numpy.nan)
        else:
            db_sb_ratio_reals.append(db_sb_ratio)
    dfboth['LOFreq'] = lofreq
    dfboth['IFFreq'] = iffreqs
    dfboth['raw_sb_ratio'] = raw_sb_ratios
    dfboth['corr3'] = corr3s
    dfboth['corr4'] = corr4s
    dfboth['avg_corr'] = avg_corrs
    dfboth['sb_ratio'] = sb_ratios
    dfboth['db_sb_ratio'] = db_sb_ratios
    dfboth['db_sb_ratio_real'] = db_sb_ratio_reals
    return dfboth

if __name__ == '__main__':        
    lofreqs =  numpy.arange(216, 283, 3) #[276,] #numpy.arange(216, 283, 3) #[219, 222, 225, 228, 231, 234, 240, 246, 249] #numpy.arange(216, 283, 3)

    for i, lofreq in enumerate(lofreqs):
        #if lofreq == 222:
        #    lofreq = 222.2
        if i == 0:
           df = analyze_sb_for_lo('feb16_2022_sb', lofreq)
        else:
            dft = analyze_sb_for_lo('feb16_2022_sb', lofreq)
            df = pd.concat([df, dft], axis=0)
        print("Finished freq %s" % lofreq)

    df.to_excel('feb16_2022_sideband_ratios_all_freqs.xlsx')
    #plot(df.IFFreq[df.LOFreq==lofreq],
    #     df.db_sb_ratio_real[df.LOFreq==lofreq], 's-', label='%s' % lofreq)
    #draw()
    #show()

    fig, axs = subplots(5, 5)

    i = 0
    #for row in range(1):
    for row in range(5):
        for col in range(5):
            lofreq = lofreqs[i]
            #if lofreq == 222:
            #    lofreq = 222.2
            axs[row, col].plot(df.IFFreq[df.LOFreq==lofreq], df.db_sb_ratio_real[df.LOFreq==lofreq], 's-', label='%s' % lofreq)
            axs[row, col].set_ylim(-5, 30)
            axs[row, col].grid()
            axs[row, col].legend(loc='best')
            i += 1
            if i > 21:
                break

