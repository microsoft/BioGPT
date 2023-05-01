FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-runtime

RUN apt-get update && \
	apt-get install -y \
		git \
		gcc \
		build-essential \
		wget

WORKDIR /app

# Install Fairseq
RUN git clone https://github.com/pytorch/fairseq && \
	cd fairseq && \
	git checkout v0.12.0 && \
	pip install . && \
	python setup.py build_ext --inplace

# Install Moses
RUN git clone https://github.com/moses-smt/mosesdecoder.git
ENV MOSES=/app/mosesdecoder

# Install python dependencies
RUN pip install \
	sacremoses==0.0.53 \
	scikit-learn==1.0.2 \
	fastBPE==0.1.0 \
	flask==2.2.4

# Copy BioGPT into container
COPY data data
COPY server.py server.py
COPY cmd.sh cmd.sh

# Start server
EXPOSE 80
CMD ["bash", "cmd.sh"]
