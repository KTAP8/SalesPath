FROM continuumio/miniconda3

WORKDIR /app

# Copy and create environment
COPY environment/clean-environment.yml .
RUN conda update -n base -c defaults conda && \
    conda env create -f clean-environment.yml

# Activate env by default
SHELL ["/bin/bash", "-c"]

# Ensure env is available in later RUN/CMD
ENV PATH /opt/conda/envs/salespathenv/bin:$PATH

# Copy backend and install any extra Python deps
COPY backend/ .
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "run.py"]
