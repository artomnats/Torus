FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG torus_dir="home/Torus/"

RUN mkdir ${torus_dir}

WORKDIR ${torus_dir}

RUN pip install pip -U
RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev -y

ADD requirements.txt ${torus_dir}

RUN pip install -r ${torus_dir}/requirements.txt
COPY . ${torus_dir}

#RUN mkdir /Torus && \
#    tdnf update -y && \
#    tdnf erase toybox -y && \
#    tdnf install -y shadow glibc-devel linux-devel python3-devel \
#                    build-essential python3 python3-pip tzdata vim less && \
#    pip3 install --upgrade pip && \
#    pip3 install setuptools>=39.0.1
#
#ARG torus_dir="home/Torus/"
#COPY . ${torus_dir}
#
#RUN pip3 install -r ${torus_dir}/requirements.txt
#
#WORKDIR ${torus_dir}
#
#ENV PATH="/venv/bin:$PATH"
#CMD ["bash"]
#FROM photon:3
