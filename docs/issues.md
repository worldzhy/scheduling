# Issues

## 2023 November 19

- Starting few weeks ago, it was observed that the result of the forecasting model differs between the image on the EC2 isntance compare to the local image. An instance of this scenario was observed when using the following inputs:

  ```bash
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

- Cleaning and purging docker both from the EC2 instance and local instance was also tried, but the issue still persisted. The following commands were used to clean docker:

  ```bash
  #### Remove all containers
  docker stop $(docker ps -a -q)
  docker rm $(docker ps -a -q)

  #### Remove all images
  docker rmi $(docker images -a -q)

  ### Remove unused volumes
  docker volume prune

  #### System cleanup
  docker system prune -a
  ```

- As an experimentation, another machine (M1) was used to freshly install docker and build the image. The result is that, the API built from this gave reasonable forecast results, which is different from the result given by the API deployed on an EC2 instance. From this, it can be safely concluded that the difference of the result is not due to some caching issue. It is highly likely the the difference of the results may be due to the different architecture of the local machine and the EC2 isntance.

- Container from EC2 instance and local instance was also inspected using `docker inspect {containerId}` to check if there are any significant differences between the two. But upon inspection, there was no visible differences aside from the ids and hashes.

- Initially, docker on the EC2 instance would require `sudo` to be executed. It was also suspected that this was the root of the issue. But after fixing the permission (see code block below), and building again without root access, the difference on the results is still there.

  ```bash
  sudo usermod -a -G docker ec2-user
  sudo chmod 666 /var/run/docker.sock
  docker version
  ```

- Docker version on the EC2 instance and local instance was also different. EC2 instance has `Docker version 20.10.23, build 7155243` installed, but local instance has `Docker version 24.0.6, build ed223bc`. Updating the docker on the EC2 instance to the latest build was not successful as `amazonlinux` only have `Docker version 20.10.23, build 7155243` as the latest one. So, in order for the two to have the same version, local instance's docker version was downgraded to docker desktop v4.18.0 which has docker engine v20.10.24 (https://docs.docker.com/desktop/release-notes/#4180), close to the docker engine version of that in the EC2 instance. However, even with the downgraded docker on the local instance, the difference in the result still persisted.

- The current direction now is to apply the `build once deploy many` principle. I will try to build the image and upload it to some repository, then EC2 instance would just pull from it rather than build the image again.

- Investigation continued on 2023-11-29. After building the image to be published to the repository and testing it, the image showed issue described above which was unexpected. So further investigation was made, and the root cause this time was identitfied to be on the use of `pd.concat()` function which has unexpected results when dataframes being concatenated have no column names such as the CSVs we have from snowflake. The current direction now is to find alternative functions for `pd.concat()` that can handle plain concatenation disregarding any column names. For this reason `copyfileobj` method from `shutil` package is used. Upon deploying and testing again the updated image, all is working fine locally and in EC2 instance. This issue is now resolved.
