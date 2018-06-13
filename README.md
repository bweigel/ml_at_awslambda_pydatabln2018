# Deploying ML-models to AWS lambda @ Workshop PyData Berlin 2018

### What you will need (and should already have installed)

- Python 3.6
- [node.js](https://nodejs.org/en/) (>=8.0) & NPM
- [Docker](https://www.docker.com/community-edition)


1. create AWS account at [https://aws.amazon.com](https://aws.amazon.com) if you have not already done so (see [Instruction](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/))
    - you will need a credit card to do this, but you __will not be charged__ if you stay in the [free tier](https://aws.amazon.com/free/)
    - *Beware:* the S3 capabilities, that we will be using, will only be free of charge for the first 12 months!
    - [create a new user within IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) (do not use root user to do stuff in your account and be sure to use MFA and a secure password)
    - [create an access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey) for programmatic access
2. install and setup the [AWS Command Line Interface](https://aws.amazon.com/cli/)
    - `pip install awscli`
    - `aws configure` (see [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html))
2. create an s3 bucket, where you want serverless to deploy your code (`aws s3api create-bucket --acl private --bucket <your_bucket_name>`)
3. 