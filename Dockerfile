FROM continuumio/miniconda3
WORKDIR /app
COPY . /app
RUN conda env create -f env.yml
SHELL ["conda", "run", "-n", "env", "/bin/bash", "-c"]
EXPOSE 3000
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "env", "python", "main.py"]
