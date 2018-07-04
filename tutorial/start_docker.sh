#!/usr/bin/env bash

set -euo pipefail

echo ${AWS_PROFILE:=default}

export AWS_ACCESS_KEY_ID=$(aws --profile ${AWS_PROFILE} configure get aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws --profile ${AWS_PROFILE} configure get aws_secret_access_key)

docker run --rm -ti -v $(pwd)/from_scratch:/workd -w /workd \
    -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
    -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} bweigel/ml_at_awslambda_pydatabln2018_autobuild:latest /bin/bash