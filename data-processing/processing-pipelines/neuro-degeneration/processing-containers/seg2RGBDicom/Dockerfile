FROM python:3.9-slim

LABEL IMAGE="seg2RGBDicom"
LABEL VERSION="0.1.1"
LABEL CI_IGNORE="True"

RUN pip install --upgrade pip

RUN pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org SimpleITK numpy

COPY files/seg2rgbdicom.py /

CMD ["python3","-u","/seg2rgbdicom.py"]