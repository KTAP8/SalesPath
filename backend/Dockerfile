FROM continuumio/miniconda3

WORKDIR /app

# Copy and create environment
COPY environment/clean-environment.yml .
# COPY clean-environment.yml .
RUN conda update -n base -c defaults conda && \
    conda env create -f clean-environment.yml

# Activate env by default
SHELL ["/bin/bash", "-c"]

# Ensure env is available in later RUN/CMD
ENV PATH /opt/conda/envs/salespathenv/bin:$PATH

# Copy backend and install any extra Python deps
COPY backend/ .
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "run.py"]

# FROM continuumio/miniconda3

# WORKDIR /app

# COPY clean-environment.yml .
# RUN conda update -n base -c defaults conda && \
#     conda env create -f clean-environment.yml

# # Use bash shell
# SHELL ["/bin/bash", "-c"]

# COPY requirements.txt ./
# RUN pip install -r requirements.txt

# COPY . .

# EXPOSE 8080

# CMD ["conda", "run", "--no-capture-output", "-n", "salespathenv", "python", "run.py"]
