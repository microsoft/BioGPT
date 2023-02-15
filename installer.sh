
# this script installs biogpt requirements.
# 1- creates virtual enviroment of python3.10 @ ~/venvs/biogpt
# 2- clone and checkout fairseq v0.12.0 & moses & fastBPE
# 3- pip install requirements

export ve_name='biogpt'
export py_version=3.10
curl bit.ly/cfgvelinux -L | bash
source ~/venvs/$ve_name/bin/activate
ve_data_path=$HOME/venvs/$ve_name/data
ve_code_path=$HOME/venvs/$ve_name/code
export MOSES=$ve_code_path/mosesdecoder
export FASTBPE=$ve_code_path/fastBPE


mkdir $ve_code_path
mkdir $ve_data_path


cd $ve_code_path
git clone https://github.com/pytorch/fairseq
cd fairseq
git checkout v0.12.0
pip install .
python setup.py build_ext --inplace

cd $ve_code_path
git clone https://github.com/moses-smt/mosesdecoder.git

cd $ve_code_path
git clone https://github.com/glample/fastBPE.git
cd fastBPE
g++ -std=c++11 -pthread -O3 fastBPE/main.cc -IfastBPE -o fast
pip install .


pip install sacremoses
pip install scikit-learn
# pip install torch==1.12.0

mkdir $ve_data_path/checkpoints
cd ~/venvs/biogpt/data/checkpoints

# this downloads all checkpoints, remove as approriate
wget https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/Pre-trained-BioGPT.tgz
tar -zxvf Pre-trained-BioGPT.tgz
wget https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/Pre-trained-BioGPT-Large.tgz
tar -zxvf Pre-trained-BioGPT-Large.tgz
wget https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/QA-PubMedQA-BioGPT.tgz
tar -zxvf QA-PubMedQA-BioGPT.tgz
wget https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/QA-PubMedQA-BioGPT-Large.tgz
tar -zxvf QA-PubMedQA-BioGPT-Large.tgz
wget https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/RE-BC5CDR-BioGPT.tgz
tar -zxvf RE-BC5CDR-BioGPT.tgz
wget https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/RE-DDI-BioGPT.tgz
tar -zxvf RE-DDI-BioGPT.tgz
wget https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/RE-DTI-BioGPT.tgz
tar -zxvf RE-DTI-BioGPT.tgz
wget https://msramllasc.blob.core.windows.net/modelrelease/BioGPT/checkpoints/DC-HoC-BioGPT.tgz
tar -zxvf DC-HoC-BioGPT.tgz


cat <<EOF > ~/venvs/$ve_name/code/setup_env_var.sh
export ve_name='biogpt'
export py_version=3.10
export ve_data_path=$HOME/venvs/$ve_name/data
export ve_code_path=$HOME/venvs/$ve_name/code
export MOSES=$ve_code_path/mosesdecoder
export FASTBPE=$ve_code_path/fastBPE
EOF


mkdir ~/code || true
cd ~/code
git clone https://github.com/microsoft/BioGPT
cd ./BioGPT
git pull
ln -s ~/venvs/$ve_name/data/checkpoints ./checkpoints


cat <<EOF > run.sh
source ~/venvs/biogpt/bin/activate  # activate virtual enviroment.
source ~/venvs/biogpt/setup_env_var.sh  # declare enviroment variables
cd ~/code/BioGPT  # head to the repostiroy
python  # run stuff
EOF

echo "Done."
echo "Source run.sh in ~/code/BioGPT then run any of the examples."

