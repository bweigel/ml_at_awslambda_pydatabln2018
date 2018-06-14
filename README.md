# Deploying ML-models to AWS lambda - Workshop @ PyData Berlin 2018 (WIP)

### What you will need (and should already have installed)

- Python 3.6
- [node.js](https://nodejs.org/en/) (>=8.0) & NPM
- [Docker](https://www.docker.com/community-edition)

### Quickstart (minimal DevOps overhead)

1. create an AWS account at [https://aws.amazon.com](https://aws.amazon.com) if you have not already done so (see [Instruction](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/))
    - you will need a credit card to do this, but you __will not be charged__ if you stay in the [free tier](https://aws.amazon.com/free/)
    - *Beware:* the S3 capabilities, that we will be using, will only be free of charge for the first 12 months!
    - [create a new user within IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) (do not use root user to do stuff in your account and be sure to use MFA and a secure password)
    - [create an access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey) for programmatic access
2. install and setup the [AWS Command Line Interface](https://aws.amazon.com/cli/)
    - `pip install awscli`
    - `aws configure` (see [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html))
3. create an s3 bucket to hold your serialized (pickled) models and the lambda code
    - use the cli `aws s3api create-bucket --acl private --bucket <your_deployment_bucket_name>` or the [S3 Management Console](https://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html)   
    - **BEWARE** S3-bucket names must be globally unique!
4. clone this repo `git clone https://github.com/bweigel/ml_at_awslambda_pydatabln2018.git` 
    - and change into the `tutorial` folder `cd ml_at_awslambda_pydatabln2018/tutorial`
6. upload the provided models in `training/models` using `make deploy-model`
    - this will prompt you to enter the bucket name from **3** and an object prefix (think of it as a folder name)
    - the output tells you what has been uploaded:
        ```bash
        $ make deploy-model
        ./training/deploy_model.sh
        Enter bucket name: dreigelb.public
        Enter object prefix: pydatabln2018
        + aws s3 cp --recursive ./training/models s3://dreigelb.public/pydatabln2018/
        upload: training/models/naive_bayes_clf.pkl to s3://dreigelb.public/pydatabln2018/naive_bayes_clf.pkl
        upload: training/models/tfidf_vectorizer.pkl to s3://dreigelb.public/pydatabln2018/tfidf_vectorizer.pkl
        ```
5. find the `TODOs` in the `serverless.yml` and fill in the buckets specified in **3** and the path to the classifiers:
    ![](./resources/serverless_todo1.png) 
    ![](./resources/serverless_todo2.png) 
6. deploy your service to AWS using `make deploy`

TODO


-------------------------------------------------------------------------------


### Things that can be optimized

*Exclude stuff from libraries to reduce the size of the deployment package*:

1. **pandas** (57 MB total):
    - 32 MB of `test` code means 57 MB down to 25 MB (-56%)
2. **sklearn** (47 MB total):
    - 1.6 MB of `datasets` code (-3.4%)
    - 4.5 MB of `tests` code (-9.6%)
3. **numpy** (57 MB total):
    - 1.4 MB of `distutils` code(-3%)
    - 5.8 MB of `tests` code (-10%)
    - **DO NOT** remove `numpy.testing`
4. **scipy** (117 MB total):
    - 13.3 MB of `tests` code (-11.3%)
    
*Byte compile everything*:

1. byte-compile (inside lambda dockedr container) `python -m compileall .`
2. copy `*.pyc` files from `__pycache__` to top-level directory: `find . -type f -name '*.pyc' | while read f; do n=$(echo $f | sed 's/__pycache__\///' | sed 's/.cpython-36//'); cp $f $n; done;`
3. remove `__pycache__` directories: `find . -type d -a -name '__pycache__' | xargs rm -rf`
3. remove `*.py` files: `find . -type f -name '*.py' | xargs rm`
