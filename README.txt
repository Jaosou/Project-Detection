source ~/tf_ubuntu_env/bin/activate

#Active Docker Bash
sudo docker exec -it cuda-wsl bash

#Remmove and Clean
sudo apt-get remove --purge 'cuda*' 'nvidia*'
sudo apt-get autoremove
sudo apt-get clean


#Add Path
echo 'export PATH=/usr/local/cuda-12.2/bin:$PATH' >> ~/envs/tsf-py311/bin/activate
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.2/lib64:$LD_LIBRARY_PATH' >> ~/envs/tsf-py311/bin/activate


#Activate
source ~/tf_gpu_env_wsl/bin/activate

#Add env for kernel
pip install jupyter ipykernel
python -m ipykernel install --user --name=tsf-py311 --display-name "TensorFlow 2.15"

sudo cp cudnn-linux-x86_64-8.9.4.25_cuda12-archive/include/cudnn*.h /usr/local/cuda-12.2/include
sudo cp cudnn-linux-x86_64-8.9.4.25_cuda12-archive/lib/libcudnn* /usr/local/cuda-12.2/lib64


 #Config WSL  
wsl --list --verbose (Check WSL)
wsl --unregister (name)   (delete wsl)

#Add Conda Path
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

#Create ENV Conda
conda create --name (name) python=(version : 3.10)

#Activate ENV
source ~/.bashrc
conda activate (name)

#Check  Location Path
 whereis cuda



