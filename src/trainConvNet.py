# Author: Yan Zhang  
# Email: zhangyan.cse (@) gmail.com

import sys
import numpy as np
#import matplotlib.pyplot as plt
import pickle
import os
import gzip
import model
from torch.utils import data
import torch
import torch.optim as optim
from torch.autograd import Variable
from time import gmtime, strftime
import sys
import torch.nn as nn
import argparse

use_gpu = 1

conv2d1_filters_numbers = 8
conv2d1_filters_size = 9
conv2d2_filters_numbers = 8
conv2d2_filters_size = 1
conv2d3_filters_numbers = 1
conv2d3_filters_size = 5


down_sample_ratio = 16
epochs = 10
HiC_max_value = 100
batch_size = 512


# This block is the actual training data used in the training. The training data is too large to put on Github, so only toy data is used. 
# cell = "GM12878_replicate"
# chrN_range1 = '1_8'
# chrN_range = '1_8'

# low_resolution_samples = np.load(gzip.GzipFile('/home/zhangyan/SRHiC_samples/'+cell+'down16_chr'+chrN_range+'.npy.gz', "r")).astype(np.float32) * down_sample_ratio
# high_resolution_samples = np.load(gzip.GzipFile('/home/zhangyan/SRHiC_samples/original10k/'+cell+'_original_chr'+chrN_range+'.npy.gz', "r")).astype(np.float32)

# low_resolution_samples = np.minimum(HiC_max_value, low_resolution_samples)
# high_resolution_samples = np.minimum(HiC_max_value, high_resolution_samples)


#low_resolution_samples = np.load(gzip.GzipFile('../../data/GM12878_replicate_down16_chr19_22.npy.gz', "r")).astype(np.float32) * down_sample_ratio
#high_resolution_samples = np.load(gzip.GzipFile('../../data/GM12878_replicate_original_chr19_22.npy.gz', "r")).astype(np.float32)

#low_resolution_samples = np.load(gzip.GzipFile('/home/zhangyan/SRHiC_samples/IMR90_down_HINDIII16_chr1_8.npy.gz', "r")).astype(np.float32) * down_sample_ratio
#high_resolution_samples = np.load(gzip.GzipFile('/home/zhangyan/SRHiC_samples/original10k/_IMR90_HindIII_original_chr1_8.npy.gz', "r")).astype(np.float32)

def train(lowres,highres, outModel="model"):
    low_resolution_samples = lowres.astype(np.float32) * down_sample_ratio

    high_resolution_samples = highres.astype(np.float32) 

    low_resolution_samples = np.minimum(HiC_max_value, low_resolution_samples)
    high_resolution_samples = np.minimum(HiC_max_value, high_resolution_samples)



    # Reshape the high-quality Hi-C sample as the target value of the training. 
    sample_size = low_resolution_samples.shape[-1]
    padding = conv2d1_filters_size + conv2d2_filters_size + conv2d3_filters_size - 3
    half_padding = padding / 2
    output_length = sample_size - padding
    Y = []
    for i in range(high_resolution_samples.shape[0]):
        no_padding_sample = high_resolution_samples[i][0][half_padding:(sample_size-half_padding) , half_padding:(sample_size - half_padding)]
        Y.append(no_padding_sample)
    Y = np.array(Y).astype(np.float32)

    print(low_resolution_samples.shape, Y.shape)

    lowres_set = data.TensorDataset(torch.from_numpy(low_resolution_samples), torch.from_numpy(np.zeros(low_resolution_samples.shape[0])))
    lowres_loader = torch.utils.data.DataLoader(lowres_set, batch_size=batch_size, shuffle=False)

    hires_set = data.TensorDataset(torch.from_numpy(Y), torch.from_numpy(np.zeros(Y.shape[0])))
    hires_loader = torch.utils.data.DataLoader(hires_set, batch_size=batch_size, shuffle=False)


    Net = model.Net(40, 28)

    if use_gpu:
        Net = Net.cuda()

    optimizer = optim.SGD(Net.parameters(), lr = 0.00001)
    _loss = nn.MSELoss()
    Net.train()

    running_loss = 0.0
    running_loss_validate = 0.0
    reg_loss = 0.0

    # write the log file to record the training process
    with open('HindIII_train.txt', 'w') as log:
        for epoch in range(0, 3500):
            for i, (v1, v2) in enumerate(zip(lowres_loader, hires_loader)):    
                if (i == len(lowres_loader) - 1):
                    continue 
		_lowRes, _ = v1
		_highRes, _ = v2
	    

		_lowRes = Variable(_lowRes)
		_highRes = Variable(_highRes)

	    
		if use_gpu:
		    _lowRes = _lowRes.cuda()
		    _highRes = _highRes.cuda()
		optimizer.zero_grad()
		y_prediction = Net(_lowRes)

		loss = _loss(y_prediction, _highRes) 

		loss.backward()  
		optimizer.step()

		running_loss += loss.data[0]
	    
	    print('-------', i, epoch, running_loss/i, strftime("%Y-%m-%d %H:%M:%S", gmtime()))
	
	    log.write(str(epoch) + ', ' + str(running_loss/i,) + '\n')
	    running_loss = 0.0
	    running_loss_validate = 0.0
	    # save the model every 100 epoches
	    if (epoch % 100 == 0):
		torch.save(Net.state_dict(), outModel + str(epoch) + str('.model'))
		pass








