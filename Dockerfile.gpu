#Fetch our GPU docker base
FROM 221497708189.dkr.ecr.us-west-2.amazonaws.com/ml_resources:pytorch_gpu_ecs_470

RUN apt -y update &&\
    apt -y upgrade &&\
    apt install -y git

RUN mkdir -p /app/
WORKDIR /app

#Clone BioGPT
RUN git clone https://github.com/microsoft/BioGPT.git
WORKDIR /app/BioGPT

#Install Moses
RUN git clone https://github.com/moses-smt/mosesdecoder.git
RUN export MOSES=${PWD}/mosesdecoder

#Install fastBPE
RUN git clone https://github.com/glample/fastBPE.git
RUN export FASTBPE=${PWD}/fastBPE
WORKDIR fastBPE/
RUN g++ -std=c++11 -pthread -O3 fastBPE/main.cc -IfastBPE -o fast
#pip installation for NOT FOUND fastBPE error
RUN pip install fastBPE

WORKDIR /app/BioGPT

#Install requirements and upgrade cudatoolkit
RUN pip install -r requirements.txt
RUN conda install -y pytorch==1.12.0 torchvision==0.13.0 torchaudio==0.12.0 cudatoolkit=11.6 -c pytorch -c conda-forge

COPY BioGPT/biogpt_trial_inference.py /app/BioGPT/

#Install models
RUN mkdir -p checkpoints/
WORKDIR /app/BioGPT/checkpoints

#Pre-Trained BioGPT
RUN wget https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/Pre-trained-BioGPT.tgz &&\
    tar -zxvf Pre-trained-BioGPT.tgz &&\
    rm Pre-trained-BioGPT.tgz

##Pre-Trained BioGPT-Large
#RUN wget https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/Pre-trained-BioGPT-Large.tgz &&\
#    tar -zxvf Pre-trained-BioGPT-Large.tgz &&\
#    rm Pre-trained-BioGPT-Large.tgz
#
##QA-PubMedQA-BioGPT
#RUN wget https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/QA-PubMedQA-BioGPT.tgz &&\
#    tar -zxvf QA-PubMedQA-BioGPT.tgz &&\
#    rm QA-PubMedQA-BioGPT.tgz
#
##QA-PubMedQA-BioGPT-Large
#RUN wget https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/QA-PubMedQA-BioGPT-Large.tgz &&\
#    tar -zxvf QA-PubMedQA-BioGPT-Large.tgz &&\
#    rm QA-PubMedQA-BioGPT-Large.tgz
#
##RE-BC5CDR-BioGPT
#RUN https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/RE-BC5CDR-BioGPT.tgz &&\
#    tar -zxvf RE-BC5CDR-BioGPT.tgz &&\
#    rm RE-BC5CDR-BioGPT.tgz
#
##RE-DDI-BioGPT
#RUN wget https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/RE-DDI-BioGPT.tgz &&\
#    tar -zxvf RE-DDI-BioGPT.tgz &&\
#    rm RE-DDI-BioGPT.tgz
#
##RE-DTI-BioGPT
#RUN wget https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/RE-DTI-BioGPT.tgz &&\
#    tar -zxvf RE-DTI-BioGPT.tgz &&\
#    rm RE-DTI-BioGPT.tgz
#
##DC-HoC-BioGPT
#RUN wget https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/DC-HoC-BioGPT.tgz &&\
#    tar -zxvf DC-HoC-BioGPT.tgz &&\
#    rm DC-HoC-BioGPT.tgz

WORKDIR /app/BioGPT

#Run preprocess for all models
RUN export MOSES=${PWD}/mosesdecoder &&\
    export FASTBPE=${PWD}/fastBPE &&\ 
    for folder in DC-HoC QA-PubMedQA RE-BC5CDR RE-DDI RE-DTI; \
    do \
        cd /app/BioGPT/examples/$folder && bash preprocess.sh && cd ../../; \
    done &&\
    cp data/biogpt_large_bpecodes data/biogpt_large_dict.txt data/PubMedQA/raw/ &&\
    cd /app/BioGPT/examples/QA-PubMedQA &&\
    bash preprocess_large.sh &&\
    cd ../../

COPY server server/

ENTRYPOINT [ "python3", "-m" , "server/application"]
