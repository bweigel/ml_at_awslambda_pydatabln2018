#!/usr/bin/env bash

BASEDIR=$( dirname "${BASH_SOURCE[0]}" )

set -euo pipefail

read -e -p "Enter bucket name: " -i "dreigelb.public" BUCKET
read -e -p "Enter object prefix: " -i "pydatabln2018" PREFIX

set -x

aws s3 cp --recursive ${BASEDIR}/models s3://${BUCKET}/${PREFIX}/