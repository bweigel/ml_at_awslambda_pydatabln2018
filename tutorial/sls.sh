#!/usr/bin/env bash

BASEDIR=$( dirname "${BASH_SOURCE[0]}" )
${BASEDIR}/node_modules/serverless/bin/serverless $@ --github_token=${GITHUB_TOKEN}