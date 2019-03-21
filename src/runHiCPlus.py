# Author: Yan Zhang  
# Email: zhangyan.cse (@) gmail.com

import argparse
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
import utils
import math
from datetime import datetime


startTime = datetime.now()

parser = argparse.ArgumentParser(description='PyTorch Super Res Example')
parser.add_argument('--input_matrix', type=str, required=True, help='input matrix to use')
parser.add_argument('--model', type=str, required=True, help='model file to use')
#parser.add_argument('--output_filename', type=str, help='where to save the output image')
#parser.add_argument('--scale_factor', type=float, help='factor by which super resolution needed')
#parser.add_argument('--chr', type=int,required=True, help='chromosome number')
parser.add_argument('--cuda', action='store_true', help='use cuda')
opt = parser.parse_args()

print(opt)

use_gpu = opt.cuda
if use_gpu and not torch.cuda.is_available():
    raise Exception("No GPU found, please run without --cuda")

#use_gpu = 1

conv2d1_filters_numbers = 8
conv2d1_filters_size = 9
conv2d2_filters_numbers = 8
conv2d2_filters_size = 1
conv2d3_filters_numbers = 1
conv2d3_filters_size = 5


down_sample_ratio = 16
epochs = 10
HiC_max_value = 100


chrs_length = [249250621,243199373,198022430,191154276,180915260,171115067,159138663,146364022,141213431,135534747,135006516,133851895,115169878,107349540,102531392,90354753,81195210,78077248,59128983,63025520,48129895,51304566]

chrN = 21

expRes = 10000
## need to make resolution adjustable.
length = chrs_length[chrN-1]/expRes

# divide the input matrix into sub-matrixes. 
input_file = opt.input_matrix

inputMatrix = utils.readFiles(input_file, length + 1, expRes)

low_resolution_samples, index = utils.divide(inputMatrix)

low_resolution_samples = np.minimum(HiC_max_value, low_resolution_samples)

batch_size = 256 #low_resolution_samples.shape[0]


# Reshape the high-quality Hi-C sample as the target value of the training. 
sample_size = low_resolution_samples.shape[-1]
padding = conv2d1_filters_size + conv2d2_filters_size + conv2d3_filters_size - 3
half_padding = padding / 2
output_length = sample_size - padding


print(low_resolution_samples.shape)

lowres_set = data.TensorDataset(torch.from_numpy(low_resolution_samples), torch.from_numpy(np.zeros(low_resolution_samples.shape[0])))
lowres_loader = torch.utils.data.DataLoader(lowres_set, batch_size=batch_size, shuffle=False)

hires_loader = lowres_loader

model = model.Net(40, 28)
model.load_state_dict(torch.load(opt.model))
if use_gpu:
    model = model.cuda()

#_loss = nn.MSELoss()


#running_loss = 0.0
#running_loss_validate = 0.0
#reg_loss = 0.0


for i, (v1, v2) in enumerate(zip(lowres_loader, hires_loader)):    
    _lowRes, _ = v1
    _highRes, _ = v2

    _lowRes = Variable(_lowRes).float()
    _highRes = Variable(_highRes).float()

    
    if use_gpu:
        _lowRes = _lowRes.cuda()
        _highRes = _highRes.cuda()
    y_prediction = model(_lowRes)

    
#print '-------', i, running_loss, strftime("%Y-%m-%d %H:%M:%S", gmtime())


y_predict = y_prediction.data.cpu().numpy()


print(y_predict.shape)

# recombine samples

length = int(y_predict.shape[2])
y_predict = np.reshape(y_predict, (y_predict.shape[0], length, length))


length = int(chrs_length[chrN-1]/expRes)

prediction_1 = np.zeros((length, length))


print('predicted sample: ', y_predict.shape, '; index shape is: ', index.shape)
#print index
for i in range(0, y_predict.shape[0]):          
    if (int(index[i][1]) != chrN):
        continue
    #print index[i]
    x = int(index[i][2])
    y = int(index[i][3])
    #print np.count_nonzero(y_predict[i])
    prediction_1[x+6:x+34, y+6:y+34] = y_predict[i]

np.save(input_file + 'enhanced.npy', prediction_1)

print(datetime.now() - startTime) 

np.savetxt(input_file + 'enhanced.txt',prediction_1, fmt='%d', delimiter="\t")




