 HiCPlus
Impletmented by PyTorch 

## Dependency

* [Python] (https://www.python.org) (2.7/3.6) with Numpy and Scipy. We recommand use the  [Anaconda] (https://www.continuum.io) distribution to install Python. 

* [PyTorch] (https://http://pytorch.org/) (> 0.4.0). GPU acceleration is not required but strongly recommended. 

## Installation
Clone the repo to your local folder. 

```
$ git clone https://github.com/wangjuan001/HiCPlus_pytorch.git

```
## Usage

### Prediction
If the user doesn't train the model, just use [runHiCPlus.py](https://github.com/zhangyan32/HiCPlus_pytorch/blob/master/src/runHiCPlus.py) to generate the enhanced Hi-C interaction matrix. 


### Training
In the training stage, both high-resolution Hi-C samples and low-resolution Hi-C samples are needed. Two samples should be in the same shape as (N, 1, n, n), where N is the number of the samples, and n is the size of the samples. The sample index of the sample should be from the sample genomic location in two input data sets. 

We provided a training pipeline for convenient usage [dataGenerator.py](https://github.com/wangjuan001/HiCPlus_pytorch/blob/master/src/dataGenerator.py). 

This also includes the training dataset generating steps. All you need to do is to provide the high resolution matrix data (both sparse, dense matrix are fine), specify the chromosome number, downsampling rate(default : 16), the name of output model name (default: 80M_model).

example: 
```
python dataGenerator.py --input_file chr22.10k.obs.gm12878.matrix --chrN 22 --scale_factor 60 --out_model 80M_model

```
### Prediction
Only low-resolution Hi-C samples are needed. The shape of the samples should be the same with the training stage. The prediction generates the enhanced Hi-C data, and the user should recombine the output to obtain the entire Hi-C matrix. 

example:
```
python runHiCplus.py --input_matrix Matrixfile --model ../model/pytorch_gm12878_chr21_model_3900 --chr 1

```

### Input file generate
You can input both dense and sparse matrix file. An easy way to generate a test data is to use juicer. 
e.g.  
```

java -jar juicer_tools.jar dump observed KR https://hicfiles.s3.amazonaws.com/hiseq/gm12878/in-situ/combined.hic 1:20480000:40960000 1:20480000:40960000 BP 10000 combined_10Kb.txt

```

### Suggested way to generate samples
We suggest that generate a file containing the location of each samples when generate the samples with n x n size. Therefore, after obtaining the high-resolution Hi-C, it is easy to recombine all of the samples to obtain high-resolution Hi-C matrix. 

### Normalization and experimental condition
Hi-C experiments have several different types of cutting enzyme as well as different normalization method. Our model can handle all of the conditions as long as the training and testing are under the same condition. For example, if the KR normalized samples are used in the training stage, the trained model only works for the KR normalized low-resolution sample. 

