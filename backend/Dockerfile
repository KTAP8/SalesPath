FROM continuumio/miniconda3

WORKDIR /app

# Copy and create environment
COPY environment/clean-environment.yml .
# COPY clean-environment.yml .
RUN conda update -n base -c defaults conda && \
    export PIP_NO_CACHE_DIR=true && \
    export PIP_NO_REQUIRE_HASHES=true && \
    conda env create -f clean-environment.yml

# Activate env by default
SHELL ["/bin/bash", "-c"]

# Ensure env is available in later RUN/CMD
ENV PATH="/opt/conda/envs/salespathenv/bin:$PATH"

# Copy backend and install any extra Python deps
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "run.py"]

# FROM continuumio/miniconda3

# WORKDIR /app

# # Copy and create environment
# COPY environment/clean-environment.yml ./clean-environment.yml
# RUN conda update -n base -c defaults conda && \
#     conda env create -f clean-environment.yml

# # Use bash for subsequent RUN
# SHELL ["/bin/bash", "-c"]

# # Make the env available (modern syntax)
# ENV PATH=/opt/conda/envs/salespathenv/bin:$PATH
# ENV PORT=8080

# # Copy backend (adjust paths depending on your build context; see note below)
# COPY . .

# # Install extra Python deps *inside* the conda env
# RUN conda run -n salespathenv pip install -r requirements.txt

# EXPOSE 8080

# # Start inside the conda env (keeps deps consistent on Cloud Run)
# CMD ["conda", "run", "--no-capture-output", "-n", "salespathenv", "python", "run.py"]


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
