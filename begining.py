import numpy as np
import scipy.stats as scipy
import matplotlib.pyplot as plt

data = np.load('pulsars_data.npy')



def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def ranges(flux):
    Max = max(flux)
    Min = min(flux)
    Range = Max - Min
    return Min,Max,Range/10,Range

def flux_integral(pulse):
    area = pulse[19900:21200]
    flux = sum(area)
    return flux


flux,flux_max_list,flux_bin_max_list = [],[],[]
mean_profile = 0
for pulse in data:
    dick = {np.mean(i):np.std(i) for i in chunks(pulse[:19900],2000)}
    dick2 = {np.mean(i):np.std(i) for i in chunks(pulse[21200:],2000)}
    baseline = (min(dick, key=dick.get) + min(dick2,key=dick2.get))/2
    pulse -= baseline
    mean_profile  += pulse
    area = pulse[19900:21200]
    integral = sum(area)
    flux_max = max(area)
    flux_bin_max = np.where(area==area.max())[0]
    flux.append(integral)
    flux_max_list.append(flux_max)
    flux_bin_max_list.append(int(flux_bin_max[0]))

mean_profile = mean_profile / len(data)  #mean profile
mean_profile = mean_profile /max(mean_profile)
indices = np.argsort(flux)
flux_array = data[indices] # pulses sorted according to value of flux
Range = ranges(flux) # range of values of fluxes
first_range = Range[0]
rang = Range[2]
queba = first_range + rang
counter = 0
for i in xrange(10):
    try:
        i = str(i)
        prof = []
        for pulse in data:
            if flux_integral(pulse) < queba and flux_integral(pulse) > first_range:
                prof.append(pulse)
        pro = sum(prof)/len(prof)
        pro = pro /max(pro)

        fig = plt.figure(1)
        ax = fig.add_subplot(111)
        plt.xlabel('Phase[s]')
        plt.ylabel('Flux')
        plt.plot(pro,label = 'profile of ' + str(len(prof)) + ' pulses ; Range between  ' + str(round(first_range * 1,2)) + ' and  ' +str(round(queba * 1,2))+ 'mJy')
        plt.plot(mean_profile,'--',color='red', label='mean profile')
        plt.xlim([19000,23000])

        handles, labels = ax.get_legend_handles_labels()
        lgd = ax.legend(handles, labels, loc='center left', bbox_to_anchor=(1,0.5))
        fig.savefig(i + '_intensity_range_plot' + '.png', bbox_extra_artists=(lgd,), bbox_inches='tight')
        plt.clf()

        queba = queba + rang
        first_range = first_range + rang
        del prof
        counter = counter + 1
        print counter
    except ZeroDivisionError:
        pass
