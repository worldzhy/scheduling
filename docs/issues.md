# Issues

## 2023 November 19

- Starting few weeks ago, it was observed that the result of the forecasting model differs between the image on the EC2 isntance compare to the local image. An instance of this scenario was observed when using the following inputs:

```
    curl --location '{baseUrl}/forecast' \
    --header 'Content-Type: application/json' \
    --data '{
        "params": {
            "studio_id": 44717,
            "location_id": 10,
            "program_id": "8",
            "month": "10",
            "year": 2025
        },
        "config": {
            "force_fetch": true
        }
    }'
```

- Using the CURL above, the forecasting API on the EC2 instance would give `"An error occurred: No data found for program \"8\" in location \"10\"."` error message. Whereas, the forecasting API built locally would give reasonable results.

- It was suspected that the architecture of the two machines differs, giving chance that the image built on the same Dockerfile result on different image. Local machine is an M1 Mac, but the EC2 instance is Linux Fedora.

- The following major fixes were applied to attempt to solve this issue:

  - Specified the version of the packages on `requirements.txt`.
  - Specified the version of python on `Dockerfile` to be 3.12.0.
  - Specified the base image for the python to be `slim-bullseye`.
  - Disabled caching when building Docker image in `scripts/start.sh`.
  - Specified the platform on `scripts/start.sh` and `Dockerfile`.

- However, even after applying all the fixes above, the issue still persisted.

- Cleaning and purging docker both from the EC2 instance and local instance was also tried, but the issue still persisted.

- As an experimentation, another machine (M1) was used to freshly install docker and build the image. The result is that, the API built from this gave reasonable forecast results, which is different from the result given by the API deployed on an EC2 instance. From this, it can be safely concluded that the difference of the result is not due to some caching issue. It is highly likely the the difference of the results may be due to the different architecture of the local machine and the EC2 isntance.

- Container from EC2 instance and local instance was also inspected using `docker inspect {containerId}` to check if there are any significant differences between the two. But upon inspection, there was no visible differences aside from the ids and hashes.

- Initially, docker on the EC2 instance would require `sudo` to be executed. It was also suspected that this was the root of the issue. But after fixing the permission, and building again without root access, the difference on the results is still there.

- The current direction now is to apply the `build once deploy many` principle. I will try to build the image and upload it to some repository, then EC2 instance would just pull from it rather than build the image again.
