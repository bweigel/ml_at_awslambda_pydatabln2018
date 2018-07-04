#!/usr/bin/env bash

set -euo pipefail

if [[ -z "${AWS_ACCESS_KEY_ID:-}" ]]; then
    echo "AWS_ACCESS_KEY_ID not set in environment."
    echo "Getting AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY from profile \"${AWS_PROFILE:=default}\"..."
    export AWS_ACCESS_KEY_ID=$(aws --profile ${AWS_PROFILE} configure get aws_access_key_id)
    export AWS_SECRET_ACCESS_KEY=$(aws --profile ${AWS_PROFILE} configure get aws_secret_access_key)
fi

docker pull bweigel/ml_at_awslambda_pydatabln2018_autobuild:latest
docker run --rm -ti -v $(pwd)/from_scratch:/from_scratch -w /from_scratch \
    -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
    -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} bweigel/ml_at_awslambda_pydatabln2018_autobuild:latest /bin/bash