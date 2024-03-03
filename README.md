# LUF-PPARD
LUF-PPARD: Lightweight User-Friendly - Pathogen, Plasmid, and Antimicrobial Resistance Detection, 
the Flask web application developed to monitor the FASTQ directory while the Oxford Nanopore technology is running, stopping every 10 minutes to concatenate the newly found FASTQ file(s), and run the analysis. The analysis is including three main sections which are pathogen classification using Kraken2 and GTDB indexed database, plasmid detection using Minimap2 and COMPASS database, and AMR detection using Minimap2 and CARD database.
<br>
<br>
If you prefer running the program through a docker container, you can pull the docker image. The local directory must be mounted to the container for LUF-PPARD to access the FASTQ and database directory.
<br>
**To pull docker image**
```
docker pull nayiyarace/lufppard:0.0.1.RELEASE
```
Conda or Miniconda is required for LUF-PPARD. You can install conda using the file provided in this repository and create an environment using "env.yml".
<br>
**To install conda:**
```
bash Miniconda3-py310_23.3.1-0-Linux-x86_64.sh
```
**To create conda environment:**
```
conda env create -f env.yml
conda activate env
```
Databases are needed for LUF-PPARD to work. If you want to start your new sample, please download the database from the Google Drive link provided. If you just want to see the sample list, you can skip this step.
<br>
**To download databases**
```
gdown https://drive.google.com/uc?id=1NAdboM0DIMHkGzLsGZ-ik1mDnSyx5l0D
tar -zxvf database.tar.gz
```
**To start the program:**
```
python main.py
```

