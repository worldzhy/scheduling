# Terminologies

## Entities

### Studio

The state where solidcore studio exists. Examples: California, Texas, Washington.

### Location

The specific area where a solidcore studio exists. For example in the state of California, these are valid areas: Hollywood, Santa Monica, Pasadena.

### Program

The workout program. Valid values: `30minexpress`, `advanced`, `armsabs`, `beginner`, `bunsabs`, `bunsguns`, `training`, `foundations`, `fullbody`. Each program also has its own duration.

- `30minexpress` - 30 minutes
- `advanced` - 65 minutes
- `arms+abs` - 50 minutes
- `beginner` - 50 minutes
- `buns+abs` - 50 minutes
- `buns+guns` - 50 minutes
- `coach-in-training` - 50 minutes
- `foundations` - 50 minutes
- `fullbody` - 50 minutes

### Coach

The name of the coach assigned to lead a specific program. Each coach also has their own availability and expertise.

- Coach availability: the day and time on which the coach can be assigned to lead a program
- Coach expertise: the programs on which the coach is allowed to lead

### Time

The time element of the program. This is composed of the start and the end time of the program’s schedule.

### Day

The number of the month where a program is scheduled.

### Course

This is the basic element of a schedule. A course is composed of a studio, a location, a program, a coach, time, and a day.

### Schedule

This is composed of courses. A schedule compromises the complete one month schedule of solidcore on a specific studio and location. This means that if a studio has ‘n’ number of locations, then there will be ‘n’ number of Schedules also in that particular studio.

## Models

### Scheduling

Given a list of studios, locations, programs, coaches, and data about the coaches’ availability and expertise, the model will try to generate a per-studio schedule that fits some predefined constraints.

### Forecasting

Given a historical time series data of the demand per studio, location, and program, the model will try to forecast the future demand given the following: year, month, studio, location, and program.
