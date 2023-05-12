#FROM nvcr.io/nvidia/tensorflow:21.04-tf2-py3
FROM tensorflow/tensorflow:2.3.3-gpu

LABEL IMAGE="muse"
LABEL VERSION="0.1.0"
LABEL CI_IGNORE="True"

RUN apt-get update && apt-get install -y \
    git \
    htop \
    zip \
    unzip \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install setuptools SimpleITK==1.2.4

RUN mkdir /src

WORKDIR /src
COPY files/driverscript.py /src

RUN mkdir /tempmuse

RUN mkdir /muse-pip-package
#RUN git clone  https://github.com/CBICA/DeepMRSeg.git /muse-pip-package && cd /muse-pip-package && git checkout 1.0.0.Alpha2
RUN git clone  https://github.com/CBICA/DeepMRSeg.git /muse-pip-package

RUN cd /muse-pip-package && python setup.py install

COPY files/ /src

CMD ["python3","-u","/src/driverscript.py"]
