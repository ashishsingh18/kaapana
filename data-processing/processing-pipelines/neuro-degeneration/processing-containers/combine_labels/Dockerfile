FROM python:3.9-slim

LABEL IMAGE="combine_labels"
LABEL VERSION="0.1.0"
LABEL CI_IGNORE="True"

RUN pip install --upgrade pip

RUN pip3 install SimpleITK

#RUN mkdir /temp_muse_subset

COPY files/combine_labels.py /
COPY files/MUSE_Kapaana_DerivedRegions_v3.csv /

CMD ["python3","-u","/combine_labels.py"]