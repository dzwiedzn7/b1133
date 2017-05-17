import collections as cl  #package which contain OrderedDictionary
import numpy as np
import matplotlib.pyplot as plt
import csv


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

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
    np.save('profile_data',avg_pulse)
    plt.plot(avg_pulse)
    plt.xlim([19000,22000])
    plt.show()

def noise(data):
    """ save to file all information about noise"""
    file_=open('new_name.txt','r') #it is separate file which contain name of every pulse file
    namespace = [i for i in file_]
    noise = csv.writer(open('flux_noise.csv','a'))
    noise.writerow(['name','min_avg_left','min_std_left','max_avg_left','max_std_left',
                    'min_avg_right','min_std_right','max_avg_right','max_std_right',
                    'off_left_min','off_left_max','off_right_min','off_right_max'])
    counter = 0
    for idx,pulse in enumerate(data):
        name = namespace[idx]
        dick_left = cl.OrderedDict(((np.mean(i),np.std(i)) for i in chunks(pulse[:19900],2000)))
        dick_right = cl.OrderedDict(((np.mean(i),np.std(i)) for i in chunks(pulse[21200:],2000)))
        min_avg_left = min(dick_left, key=dick_left.get)
        max_avg_left = max(dick_left,key=dick_left.get)
        min_avg_right = min(dick_right, key=dick_right.get)
        max_avg_right = max(dick_right,key=dick_right.get)
        min_std_left = dick_left[min_avg_left]
        max_std_left = dick_left[max_avg_left]
        min_std_right = dick_right[min_avg_right]
        max_std_right = dick_right[max_avg_right]
        off_left_min = float(dick_left.keys().index(min_avg_left) * 2000)
        off_right_min = float((dick_right.keys().index(min_avg_right)*2000) + 21200)
        off_left_max = float(dick_left.keys().index(max_avg_left) * 2000 )
        off_right_max = float((dick_right.keys().index(min_avg_right)*2000) + 21200)
        noise.writerow([name,min_avg_left,min_std_left,max_avg_left,max_std_left,
                        min_avg_right,min_std_right,max_avg_right,max_std_right,
                        off_left_min,off_left_max,off_right_min,off_right_max])
        counter += 1
        print counter

def flux(data):
    """ calculate flux,max value and bin from max value from data and plot
    histograms """

    file_ = open('new_name.txt','r')
    namespace = [i for i in file_]
    file_final = csv.writer(open('flux.csv','a'))
    file_final.writerow(['name','flux','flux_max','flux_bin'])
    flux_list = []
    flux_max_list = []
    flux_bin_max_list = []
    counter = 0
    for idx,pulse in enumerate(data):
        name = namespace[idx]
        dick = {np.mean(i):np.std(i) for i in chunks(pulse[:19900],2000)}
        dick2 = {np.mean(i):np.std(i) for i in chunks(pulse[21200:],2000)}
        baseline = (min(dick, key=dick.get) + min(dick2,key=dick2.get))/2
        pulse -= baseline
        area = pulse[19900:21200]
        flux = sum(area)
        flux_max = max(area)
        flux_bin_max = np.where(area==area.max())[0]
        flux_list.append(flux)
        flux_max_list.append(flux_max)
        flux_bin_max_list.append(int(flux_bin_max[0]))
        file_final.writerow([name,flux,flux_max,19900 + int(flux_bin_max[0])])
        counter += 1
        print counter
    plt.hist(flux_list,bins=100)
    plt.show()
    plt.hist(flux_max_list,bins=100)
    plt.show()
    plt.hist(flux_bin_max_list)
    plt.show()








data = np.load('pulsars_data.npy')
profile_avg(data)
#noise(data)
#flux(data)
