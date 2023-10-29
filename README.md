# Scheduling Model

## Steps to run

1. Populate `.env` based on `.env.example`.

1. Start app in docker

   ```bash
   chmod +x scripts/start.sh
   scripts/start.sh
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
        "capacity": 19.048705245367334,
        "capacity_lower": 12.230880018612881,
        "capacity_upper": 25.404814339108576,
        "date": "Tue, 01 Apr 2025 00:00:00 GMT",
        "location_id": 10,
        "program_id": 8,
        "studio_id": 44717
    },
    {
        "capacity": 19.24758122649038,
        "capacity_lower": 12.760553310676244,
        "capacity_upper": 25.930341096904595,
        "date": "Wed, 02 Apr 2025 00:00:00 GMT",
        "location_id": 10,
        "program_id": 8,
        "studio_id": 44717
    },
    ...
    {
        "capacity": 20.689135564125674,
        "capacity_lower": 14.540704757678094,
        "capacity_upper": 27.287256508980633,
        "date": "Tue, 29 Apr 2025 00:00:00 GMT",
        "location_id": 10,
        "program_id": 8,
        "studio_id": 44717
    },
    {
        "capacity": 20.403568461176988,
        "capacity_lower": 13.667114145579541,
        "capacity_upper": 27.284815934213018,
        "date": "Wed, 30 Apr 2025 00:00:00 GMT",
        "location_id": 10,
        "program_id": 8,
        "studio_id": 44717
    }
]
```

Sample CURL:

```
curl --location '{baseUrl}/forecast' \
--header 'Content-Type: application/json' \
--data '{
    "params": {
        "studio_id": 44717,
        "location_id": 10,
        "program_id": 8,
        "month": 4,
        "year": 2025
    },
    "config": {
        "force_fetch": false
    }
}'
```

### Studio mapping

Gives the mapping of studio id to its string value.

Endpoint:

```
GET {baseurl}/studio
```

Sample payload: No payload

Sample response:

```
[
    {
        "id": 44717,
        "value": "[solidcore] DC.MD.VA"
    },
    {
        "id": 186771,
        "value": "[solidcore] Minnesota"
    },
    ...
    {
        "id": 5730646,
        "value": "[solidcore] Tennessee"
    },
    {
        "id": 5730673,
        "value": "[solidcore] Tennessee"
    }
]
```

Sample CURL:

```
curl --location --request GET '{baseurl}/studio' \
--header 'Content-Type: application/json'
```

### Location mapping

Gives the mapping of location id to its string value.

Endpoint:

```
GET {baseurl}/location
```

Sample payload:

- `studio_id` (int): query parameter indicating the target studio of the locations to be retrieved

Sample response:

```
[
    {
        "id": 1,
        "value": "DC, Adams Morgan"
    },
    {
        "id": 2,
        "value": "DC, Shaw"
    },
    ...
    {
        "id": 40,
        "value": "New Location"
    },
    {
        "id": 98,
        "value": "Online Store"
    }
]
```

Sample CURL:

```
curl --location '{baseurl}/location?studio_id=44717'
```

### Program mapping

Gives the mapping of program id to its string value.

Endpoint:

```
GET {baseurl}/program
```

Sample payload: No payload

Sample response:

```
[
    {
        "id": 0,
        "value": "30minexpress"
    },
    {
        "id": 1,
        "value": "advanced"
    },
    ...
    {
        "id": 7,
        "value": "foundations"
    },
    {
        "id": 8,
        "value": "fullbody"
    }
]
```

Sample CURL:

```
curl --location --request GET '{baseurl}/program' \
--header 'Content-Type: application/json'
```

### Month mapping

Gives the mapping of month id to its string value.

Endpoint:

```
GET {baseurl}/month
```

Sample payload: No payload

Sample response:

```
[
    {
        "id": 1,
        "value": "January"
    },
    {
        "id": 2,
        "value": "February"
    },
    ...
    {
        "id": 11,
        "value": "November"
    },
    {
        "id": 12,
        "value": "December"
    }
]
```

Sample CURL:

```
curl --location --request GET '{baseurl}/month' \
--header 'Content-Type: application/json'
```
