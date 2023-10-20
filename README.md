# Scheduling Model

## Steps to run

1. Start app in docker

   ```bash
   chmod +x start.sh
   ./start.sh
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

## Endpoints

### Scheduling

TODO: Add scheduling API documentation

### Forecast

Gives the forecasted capacity (with lower and upper confidence interval) per day in a month given the following: month, year, studio, location, and program.

Endpoint:

```
POST {baseurl}/forecast
```

Sample payload:

```
{
    "params": {
        "studio_id": 5723430,
        "location_id": 4,
        "program_id": 8,
        "month": 11,
        "year": 2023
    },
    "config": {
        "force_fetch": false
    }
}
```

- `params`
  - `studio_id` (int): the id corresponding to a studio
  - `location_id` (int): the id corresponding to a location
  - `program_id` (int): the id corresponding to a program
  - `month` (int): the number of the month (ex: 1 - January, 2 - February, ..., 12 - December)
  - `year` (int): target year
- `config`:
  - `force_fetch` (bool): if true, redownloads data, else downloads only data if data is not available locally

Sample response:

```
[
    {
        "capacity": 22.829049133915003,
        "capacity_lower": 20.278792945252004,
        "capacity_upper": 25.393690083255862,
        "date": "Wed, 01 Jan 2025 00:00:00 GMT",
        "location": "4",
        "program": "fullbody",
        "studio": "44717"
    },
    {
        "capacity": 22.662822979118967,
        "capacity_lower": 20.074596372500963,
        "capacity_upper": 25.357740963911674,
        "date": "Thu, 02 Jan 2025 00:00:00 GMT",
        "location": "4",
        "program": "fullbody",
        "studio": "44717"
    },
    ...
    {
        "capacity": 22.140122922527585,
        "capacity_lower": 19.63426186769817,
        "capacity_upper": 24.669962181906076,
        "date": "Thu, 30 Jan 2025 00:00:00 GMT",
        "location": "4",
        "program": "fullbody",
        "studio": "44717"
    },
    {
        "capacity": 22.21153949707805,
        "capacity_lower": 19.652092099154224,
        "capacity_upper": 24.770904455912014,
        "date": "Fri, 31 Jan 2025 00:00:00 GMT",
        "location": "4",
        "program": "fullbody",
        "studio": "44717"
    }
]
```

Sample CURL:

```
curl --location '{baseurl}/forecast' \
--header 'Content-Type: application/json' \
--data '{
    "studio": "44717",
    "location": "4",
    "program": "fullbody",
    "month": 1,
    "year": 2025
}'
```
