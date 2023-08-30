# Scheduling Model

## Steps to run (To be improved)

1. Build container and image

   ```bash
   docker-compose up --build
   ```

2. Execute

   ```bash
   docker run {serviceName}
   ```

## Project Structure

- data: consists of data used for model training/retraining.
  - raw: original data dump
  - interim: intermediate data that has been transformed
  - processed: final data to be used for modeling
- docs: consists of files related to the product requirement specifications (PRS) and technical design specifications (TDS)
- models: consist of files representing trained models
- reports: Generated analysis of the data
- src: source code of the project
  - data: scripts to download or generate data
  - preprocessing: scripts to turn raw data to interim data for modeling
  - features: scripts to turn raw/interim data to processed data for modeling
  - models: scripts to train models and then use trained models to make predictions
