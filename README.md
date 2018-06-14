# Deploying ML-models to AWS lambda - Workshop @ PyData Berlin 2018 (WIP)

### What you will need (and should already have installed)

- Python 3.6
- [node.js](https://nodejs.org/en/) (>=8.0) & NPM
- [Docker](https://www.docker.com/community-edition)

### Quickstart (minimal DevOps overhead)

1. create an AWS account at [https://aws.amazon.com](https://aws.amazon.com) if you have not already done so (see [Instruction](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/))
    - you will need a credit card to do this, but you __will not be charged__ if you stay in the [free tier](https://aws.amazon.com/free/)
    - **BEWARE** the S3 capabilities, that we will be using, will only be free of charge for the first 12 months!
    - [create a new user within IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) (do not use root user to do stuff in your account and be sure to use MFA and a secure password)
    - [create an access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey) for programmatic access
2. install and setup the [AWS Command Line Interface](https://aws.amazon.com/cli/)
    - `pip install awscli`
    - `aws configure` (see [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html))
3. clone repo `git clone https://github.com/bweigel/ml_at_awslambda_pydatabln2018.git` 
    - and change into the `tutorial` folder `cd ml_at_awslambda_pydatabln2018/tutorial`
4. setup tooling with `make setup`. This installs:
    - virtualenv with dependencies defined in `Pipfile` using `pipenv` in `.venv`
    - the serverless framework and dependencies defined in `package.json` via `npm install` in `node_modules`    
5. create an s3 bucket to hold models and lambda code: `make bucket`
    - **BEWARE** S3-bucket names must be globally unique!
6. upload the provided models in `training/models` using `make deploy-model`
    - this will prompt you to enter the bucket name from **5** and an object prefix (think of it as a folder name)
    - the output tells you what has been uploaded:
        ```bash
        $ make deploy-model
        ./training/deploy_model.sh
        Enter bucket name: eigelbdemo
        Enter object prefix: pydatabln2018
        + aws s3 cp --recursive ./training/models s3://eigelbdemo/pydatabln2018/
        upload: training/models/naive_bayes_clf.pkl to s3://eigelbdemo/pydatabln2018/naive_bayes_clf.pkl
        upload: training/models/tfidf_vectorizer.pkl to s3://eigelbdemo/pydatabln2018/tfidf_vectorizer.pkl
        ```
5. find the `TODOs` in the `serverless.yml` and fill in the bucket specified in **5** and the path to the classifiers:
    ![](./resources/serverless_todo1.png) 
    ![](./resources/serverless_todo2.png) 
6. deploy your service to AWS using `make deploy`
    ![](./resources/serverless_deployment.png)
7. test your service (take url from `make deploy` output):
     ```
     $ curl -X POST https://vmrabekuo4.execute-api.eu-central-1.amazonaws.com/dev/spamorham -w "\n" -d "Am I spam or am I ham?" 
    ["spam"]
    ```

### The Deep Dive (if you want to know whats going on)

Follow steps 1. to 3. in the Quickstart section.

4. create an s3 bucket to hold your serialized (pickled) models and the lambda code
    - use the cli `aws s3api create-bucket --acl private --bucket <your_deployment_bucket_name>` or the [S3 Management Console](https://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html)   
    - **BEWARE** S3-bucket names must be globally unique!

TODO

-------------------------------------------------------------------------------

## Things to keep in mind

All the ML frameworks in Python are quite heavy weight when it comes to size. However for individual lambda deployments 
(not as part of a cloudformation stack) there is a hard filesize limit of 50 MB enforced by AWS. This is not only because AWS 
wants to srew with you, but because it wants developers to build apps with the highest performance.
There are a couple of tricks to reduce the size of your deployment zip-file. See below and the resources section for more info.

If you deploy your function as part of a cloudformation stack (which the serverless framework does by default) this limit
goes up to about 250 MB of ___unzipped___ code. I am not exactly sure what that means for the zip-file, but it is well above 50 MB.

### Things that can be optimized

Most libraries come bundled with their test-code, when installed. This test code might amount to up to 10% of the size of the package.
However 3rd party test code will be rarely needed in production environments, so one can get rid of the tests.
Also some packages provide their own datasets, which are quite useful for learning, but not so much when you want to optimize.

*Here are some examples of what can be excluded from libraries to reduce the size of the deployment package*:

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
    
Another quite useful tip that I picked up from [this][1] blogpost is to bytecompile everything and then ship it.

*Example workflow to byte compile everything*:

**NOTE** There is no tooling around this, so it is all hands on. Be sure to do this in the lambda
runtime environment (e.g. this docker image `lambci/lambda:build-python3.6`).

1. byte-compile (inside lambda dockedr container) `python -m compileall .`
2. copy `*.pyc` files from `__pycache__` to top-level directory: `find . -type f -name '*.pyc' | while read f; do n=$(echo $f | sed 's/__pycache__\///' | sed 's/.cpython-36//'); cp $f $n; done;`
3. remove `__pycache__` directories: `find . -type d -a -name '__pycache__' | xargs rm -rf`
3. remove `*.py` files: `find . -type f -name '*.py' | xargs rm`


#### Resources

[1]: AWS Lambda Python magic. Tips for creating powerful Lambda functions. https://blog.mapbox.com/aws-lambda-python-magic-e0f6a407ffc6