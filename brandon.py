#!/usr/local/bin/python3

#from scipy import signal 
import matplotlib.pyplot as plt
import numpy as np
import time
import argparse
import math,sys


N = 10
alpha = 2/(N+1)
ema_yday = 0
ema_variance_yday = 0

def generator():
    randominput = np.random.randint(args.low, args.high, size=args.numsamples)
    return randominput

def receiver(inarray):
   global ema_yday, ema_variance_yday
   ema_list = []
   sd_list = []
   min_in_range = sys.maxsize
   max_in_range = 0
 
   for i in np.nditer(inarray):
       diff = i - ema_yday
       ema_today = ema_yday + (alpha*diff)
       ema_variance = (1 - alpha) * (ema_variance_yday + alpha * diff * diff) 
       ema_list.append(ema_today)
       sd = math.sqrt(ema_variance)
       sd_list.append(sd)
       if sd > args.stddev_threshold:
          print('standard deviation {} exceeds threshold {}'.format(sd, args.stddev_threshold))
       ema_yday = ema_today
       ema_variance_yday = ema_variance
       if i < min_in_range:
          min_in_range = i
       if i > max_in_range:
          max_in_range = i
    
   ema_ary = np.array(ema_list)
   sd_ary = np.array(sd_list)
   print('Range of samples in this batch: {} -> {}'.format(min_in_range, max_in_range))
   return ema_ary, sd_ary

def display(ema_ary, sd_ary, randominput):
    # Create two subplots sharing y axis
    # fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)

    x1 = np.arange(0, args.numsamples)

    ax1.set(title='Plot of standard deviation')
    ax1.plot(x1, sd_ary, 'g.-', label='stddev')
    ax1.legend()

    ax2.set(title='Plot of moving average', xlabel='sample number')
    ax2.plot(x1, randominput, 'k.-', label='input')
    ax2.plot(x1, ema_ary, 'r.-', label='EMA')
    ax2.legend()
 
    plt.ioff()
    plt.show()
    plt.close()


if __name__ == "__main__":

    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", action="store", type = int, dest="verbosity", default=1)
    parser.add_argument("-l", "--low", action="store", type = int, dest="low", default=30)
    parser.add_argument("-i", "--high", action="store", type = int, dest="high", default=80)
    parser.add_argument("-s", "--size", action="store", type = int, dest="numsamples", default=1000)
    parser.add_argument("-t", "--stddev_threshold", action="store", type = int, dest="stddev_threshold", default=20)
    args = parser.parse_args()

    while True:
        inarray = generator()
        ema, sd = receiver(inarray)

        print('press \'d\' to display last {} samples; \'x\' to exit; any other key for generating new sample set'.format(args.numsamples))
        user = input()
        if user == 'd':
            display(ema, sd, inarray)
        elif user == 'x':
            break
        else:
            print('Generating another {} samples after 2 second'.format(args.numsamples))
            time.sleep(2)

