
#!/bin/bash

#for i in {21,22}
#do
java -jar /projects/b1100/jwn2291/juicer/scripts/scripts/juicer_tools.jar dump observed NONE https://hicfiles.s3.amazonaws.com/hiseq/gm12878/in-situ/combined.hic $i $i BP 10000 chr$i.10k.obs.gm12878.matrix    
    #java -jar /projects/b1100/jwn2291/juicer/scripts/scripts/juicer_tools.jar dump observed KR https://hicfiles.s3.amazonaws.com/hiseq/imr90/in-situ/combined.hic $i $i BP 10000 chr$i.10k.KR.imr90.matrix    
    
    #java -jar /projects/b1100/jwn2291/juicer/scripts/scripts/juicer_tools.jar dump observed NONE https://hicfiles.s3.amazonaws.com/hiseq/imr90/in-situ/combined.hic $i $i BP 10000 chr$i.10k.obs.imr90.matrix    


    #python dataGenerator.py --input_file obs/chr$i.10k.obs.imr90.matrix --chrN $i --scale_factor 16
python dataGenerator.py --input_file obs/chr$i.10k.obs.gm12878.matrix --chrN $i --scale_factor 16
    #echo "chr$i imr90 completed"
    echo "chr$i gm12878 completed"




#done

