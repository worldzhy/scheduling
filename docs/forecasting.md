# Forecasting

Given a historical time series data of the demand per studio, location, and program, the model will try to forecast the future demand given the following: year, month, studio, location, and program.

## Constraints

- Do not schedule a coach that is not available on the specific time and day
- Do not assign assign a coach that is not qualified to lead a specific program
- A studio can only cater one program on a specific time and day.

## Dataset

Raw tables needed from `snowflake` are:

- `tblclasses.csv`

  - Main dataset needed to do the forecast.
  - Columns: `CLASSDATESTART`, `LOCATIONID`, `CLASSID`, `STUDIOID`, `CLASSTRAINERID`, `CLASSCAPACITY`, `WAITLISTSIZE`, `DAYSUNDAY`, `DAYMONDAY`, `DAYTUESDAY`, `DAYWEDNESDAY`, `DAYTHURSDAY`, `DAYFRIDAY`, `DAYSATURDAY`

- `tblclasses_descriptions.csv`

  - Supplementary dataset needed to map each classid to valid program.
  - Columns: `CLASSID`, `CLASSNAME`

## Algorithm

### Preprocessing

Two main preprocessing steps were done: 1) mapping of class ids to program names and 2) processing of the main dataset (`tblclasses.csv`) to desired format.

#### Mapping of class ids

Given that in `tblclasses.csv`, only class ids are given but the forecasting model need to be done in the basis of program names. There is a need then to map each of the class ids present on `tblclasses.csv` to a valid program name. That is the goal of this preprocessing step: to produce an interim data `classnames.csv` which contains the said mapping.

The interim data `classname.csv` will have two column names: `classid` and `classname`.

Recall that these are the valid program names: `30minexpress`, `advanced`, `armsabs`, `beginner`, `bunsabs`, `bunsguns`, `training`, `foundations`, `fullbody`.

#### Preprocessing of main dataset

Series of steps were taken to transform the raw data `tblclasses.csv` into a format that the forecast model requires:

1. Convert the date column to python datetime.

2. Aggregate columns `DAY*` in single column called `day`. For example, if a row has `DAYSATURDAY = TRUE`, then that row will have a value of 6 under column `day`. The mapping would be as follows:

   - Monday: 1
   - Tuesday: 2
   - Wednesday: 3
   - Thursday: 4
   - Friday: 5
   - Saturday: 6
   - Sunday: 7

3. Add program column. Using the csv mapping produced from the previous preprocessing step, a new column called `program` will be created containing the correct program name corresponding to the class id.

4. Create demand column. Demand is calculated as the sum of capcity and waitlist size.

5. Remove rows with missing data.

6. Create a new column called `group` which is the combination of `location` and `program`. A forecast model will subsequently be fitted for each `group`.

7. For each `group`, aggregate demand with multiple dates by taking the average of the demand. For context, since a date can have multiple programs scheduled (with different timeslot), it is likely that a program can be scheduled more than once. This will result in a group having two or more entries of demand for the same date. Since a timeseries model requires only one value for each date, we need to reconcile the multiple demands. The way it was done in this preprocessing step is to just take the average of the of those demands in the same date so that only one value for the date is retained.

8. Once this step is done, a processed data called `capacity.csv` would be produced. Sample:

   ```
   date,studio,location,program,day,demand,group
   2014-11-01,44717,4,fullbody,3,16.928571428571427,fullbody-4
   2014-11-02,44717,4,fullbody,7,16.8,fullbody-4
   2014-11-04,44717,4,fullbody,2,17.0,fullbody-4
   2014-11-05,44717,4,fullbody,3,17.0,fullbody-4
   2014-11-06,44717,4,fullbody,4,17.0,fullbody-4
   ```

### Forecasting model

The forecasting model makes use of the [Prophet](https://facebook.github.io/prophet/docs/quick_start.html) package developed by the Facebook (Meta) group. This package gained popularity as it was able to give good forecast results with little tuning or configuration needed. The forecast algorithm does the following:

1. Based on the parameters passed to the model, the model will first filter the data to target studio, location, and program.

2. Model will be fitted to the data. Additional regressor are also incorporated to improve model performance. These regressors are: day of the week and US country holidays.

3. Based on the target month and year of forecast, using the fitted model, the model will generate forecasted demand for those dates.

### Usage

#### Input

```
{
    "studio_id": 44717,
    "location_id": 4,
    "program_id": 8,
    "month": 4,
    "year": 2025
}
```

- `studio_id`: the id corresponding to a studio
- `location_id`: the id corresponding to a location
- `program_id`: the id corresponding to a program
- `month`: the number of the month (ex: 1 - January, 2 - February, ..., 12 - December)
- `year`: target year

#### Output

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
