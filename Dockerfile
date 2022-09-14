FROM amazonlinux:2

RUN yum install wget -y 
RUN yum install git -y
RUN yum install -y python3 python3-pip
RUN pip3 install boto3 Pillow numpy
# RUN pip3 install -q tflite-model-maker
RUN yum install -y libusbx
RUN pip3 install -q tflite-support
RUN yum install -y python3-devel
RUN yum install -y gcc gcc-c++ kernel-devel
RUN pip3 install --upgrade cython
RUN pip3 install pycocotools==2.0.4 
# RUN pip3 install "git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI"
# CMD ["python3", "-m", "site"]
# RUN git clone https://github.com/cocodataset/cocoapi.git
# RUN /usr/bin/make --version
WORKDIR /opt/amazon/
COPY . .
RUN git clone https://github.com/tensorflow/examples
RUN cd examples/tensorflow_examples/lite/model_maker/pip_package && pip3 install -e .
RUN pip3 install -U tensorflow==2.8.2


ARG OUTPUT_PATH=s3://rekognition-content-moderation-annotations-shared/drugs/bbox/inhouse/2020325-35114-Datbboxcmbatch1/
ARG SAMPLE_COUNT=750
ARG LABEL=Joints
ARG BATCH_SIZE=4
ARG EPOCH=75


ENV OUTPUT_PATH=$OUTPUT_PATH
ENV SAMPLE_COUNT=$SAMPLE_COUNT
ENV LABEL=$LABEL
ENV BATCH_SIZE=$BATCH_SIZE
ENV EPOCH=$EPOCH
# ENV ISENGARD_PRODUCTION_ACCOUNT=false
# ENV AWS_ACCESS_KEY_ID=ASIASA24U3CBX5VHJQH6
# ENV AWS_SECRET_ACCESS_KEY=hTGhEnqZc5TfOIUjG9arUInJH76DSoLEuhlbILLN
# ENV AWS_SESSION_TOKEN=IQoJb3JpZ2luX2VjEPT//////////wEaCXVzLWVhc3QtMSJHMEUCIQCSLGZY6IBK3mK0c1nwWzYxxs1kmgHG4RtgjoNRNhYX/AIgBwgBKUo7eH2utIF4w9/tF96b+0kSQpi5B+xhac8KsyAqpQIIjP//////////ARAEGgwxMzkyNDM4NzAzMzkiDBBruUu3cqfd41BRTCr5Af++tQOsDEXpDPyM/JOXAowLMT3SPl9DUcYgkwxuKtgcxGbHunyBfOKV3MDtUecUkeWajvcnGD/CSDYn+XGsjkLdxeqv7LRy7/f8R8EPPaRZKxs4PTaFphDLszhOKcfJ1En1nnFzyban1X1N3VY39F2M8ucOVlOZLna+0QnknuPGK2gXD1o3vTAxer2xzvpmaZZonuekDUEa0/xZ5WnJOI+Cz7k5+rKRBmNVrbpLaQxtzopHtxAfE1kDqTakfv5Gqwv/1mry23iQpSm43jEGXj7ZIn0QXz6oopyUqcj1c+8bIE2zR9aWANekTDB9hIUvtl9CT/bP/uDhWjC6rPyYBjqdAex0r8/NFdNcTWvxPnDlXwdtP3p7Ee48hAWH37mBcek097J5ggH6POz3AKDYnhPieYP2s9xanThoDwch/zRwWHsu4RFr6PsP8+/A6xXZaixTtEHaW1pkZB6GVtLr6Knm+JkO9gsXTM0/pH8S/f2OoIMA1GpvHuliP24yofMkeq4oibXvRA8pcfgPHknJlu4qqMu6bh+d/EFbRu0CPgY=
# RUN ["ls"]
# RUN pip3 show tflite-model-maker
# RUN find / -name "create_pascal_tfrecord.py"
# RUN cd /usr/local/lib/python3.7/site-packages/tflite_model_maker && ls
RUN ["sh", "-c", "chmod +x /opt/amazon/util.sh"]
RUN ["sh", "-c", "/opt/amazon/util.sh"]
CMD ["sh", "-c", "python3 index.py $OUTPUT_PATH $SAMPLE_COUNT $BATCH_SIZE $EPOCH $LABEL"]
