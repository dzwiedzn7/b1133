from __future__ import division
import itertools
import numpy as np
import scipy.stats as scipy
import matplotlib.pyplot as plt
import time

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def sort_max(data):
    array_max = np.amax(data,axis = 1)
    indices = np.argsort(array_max)
    data = data[indices]
    return data


def flux_range(data):
    array = sort_max(data)
    max_list = [ max(i) for i in array]
    rang = (max_list[-1] - max_list[0])/10.
    return rang


def profile_avg(data):
    """Calculate and plot mean profile from data"""
    counter = 0
    avg_pulse = 0
    for pulse in data:
        dick = {np.mean(i):np.std(i) for i in chunks(pulse,2000)}
        baseline = min(dick, key=dick.get)
        pulse -= baseline
        avg_pulse += pulse
        counter += 1
        print counter #counter shows only how long its gonna take time
    avg_pulse = avg_pulse / len(data)
    #np.save('profile_data',avg_pulse)
    #plt.plot(avg_pulse)
    #plt.xlim([19000,22000])
    #plt.show()
    return avg_pulse

def divide(data):
    """ divide range of intensities for 10 smaller ranges and plot"""
    counter = 0
    avg = profile_avg(data)
    avg = avg / max(avg)
    dane = sort_max(data)
    rang = flux_range(data)
    first_range = max(dane[0])
    queba = first_range + rang
    for i in xrange(10):
        try:
            i = str(i)
            prof = []
            for pulse in data:
                if max(pulse) < queba and max(pulse) > first_range:
                    prof.append(pulse)
            pro = sum(prof)/len(prof)
            pro = pro /max(pro)

            fig = plt.figure(1)
            ax = fig.add_subplot(111)
            plt.xlabel('Phase[s]')
            plt.ylabel('Flux')
            plt.plot(pro,label = 'profile of ' + str(len(prof)) + ' pulses ; Range between  ' + str(round(first_range * 1000,2)) + 'and  ' +str(round(queba * 1000,2))+ 'mJy')
            plt.plot(avg,color='red', label='mean profile')

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

def SNR(data):
    """ Plot all profiles with Signal to Noise Ratio > 20 sigma """
    counter = 0
    avg = 0
    snrdata,flux_max_list,flux_bin_max_list= [],[],[]
    for pulse in data:
        dick = {np.mean(i):np.std(i) for i in chunks(pulse,2000)}
        baseline = min(dick, key=dick.get)
        pulse -= baseline
        avg += pulse
        SNR = scipy.signaltonoise(pulse)
        if SNR > np.std(pulse) * 20 :
            snrdata.append(pulse)
            area = pulse#[19900:21200]
            flux_max = max(area)
            flux_bin_max = np.argmax(area)
            #flux_bin_max = np.where(area==area.max())[0]
            flux_max_list.append(flux_max)
            flux_bin_max_list.append(flux_bin_max)
            #flux_bin_max_list.append(int(flux_bin_max[0]))
        counter += 1
        print counter
    
    avg = avg / len(data)
    avg = avg / max(avg)
    snr = sum(snrdata)/ len(snrdata)
    snr = snr/ max(snr)
    flux_max_list = flux_max_list / max(flux_max_list)
    plt.plot(avg,'--',linewidth=1,c='r',label = 'mean_profile')
    plt.plot(snr,linewidth=0.7,c='b',label = 'SNR profile')
    plt.scatter(np.array(flux_bin_max_list),flux_max_list,c = 'g',s=10)
    plt.xlim([19900,21200])
    plt.ylabel('Flux')
    plt.xlabel('Phase[bin]')
    plt.legend(loc='upper right')
    plt.show()

def baseline():
    data = np.load('pulsars_data.npy')
    pulses = []
    counter = 0
    start_time = time.time()
    for pulse in data:
        dick = {np.mean(i):np.std(i) for i in chunks(pulse,2000)}
        baseline = min(dick, key=dick.get)
        pulse -= baseline
        pulses.append(pulse)
        counter = counter + 1
        time_left = time.time() - start_time
        print("--- %s seconds ---" % (time_left))
    array = np.array(pulses)
    np.save('baseline',array)

data = np.load('baseline.npy')
divide(data)
SNR(data)
#plt.show()
