#FROM nvcr.io/nvidia/tensorflow:21.04-tf2-py3
FROM tensorflow/tensorflow:2.3.3-gpu

LABEL IMAGE="dlicv"
LABEL VERSION="0.1.1"
LABEL CI_IGNORE="True"

RUN apt-get update && apt-get install -y \
    git \
    htop \
    zip \
    unzip \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install setuptools SimpleITK==1.2.4
RUN pip install scipy==1.5.4 matplotlib==3.3.3 dill==0.3.4 h5py==2.10.0 hyperopt==0.2.5 keras==2.6.0 numpy==1.18.5 protobuf==3.17.3 pymongo==3.12.0 scikit-learn==0.24.2 nibabel==3.2.1 resource==0.2.1 networkx==2.5.1

RUN mkdir /src

WORKDIR /src
COPY files/driverscript.py /src

RUN mkdir /tempmuse

RUN mkdir /muse-pip-package

RUN git clone https://github.com/CBICA/DeepMRSeg.git /muse-pip-package && cd /muse-pip-package && git checkout 1.0.0.Alpha2
#RUN git clone  https://github.com/CBICA/DeepMRSeg.git /muse-pip-package

RUN cd /muse-pip-package && python setup.py install

COPY files/ /src

CMD ["python3","-u","/src/driverscript.py"]
