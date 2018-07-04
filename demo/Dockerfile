FROM lambci/lambda:build-python3.6

RUN curl https://nodejs.org/dist/v8.2.1/node-v8.2.1-linux-x64.tar.xz | tar -xJ -C /opt && pushd . && \
  ln -fs /opt/node-v8.2.1-linux-x64/bin/* /usr/bin/.
ENV PATH=/opt/node-v8.2.1-linux-x64/bin/:${PATH}

RUN chmod --recursive 777 /tmp && groupadd -g 1000 lambdadev \
        && adduser -u 1000 -g lambdadev -s /bin/bash lambdadev

RUN pip install pipenv pytest && pip install -U awscli

RUN mkdir /demo
COPY . /demo/
RUN cd /demo && sed -i -e 's/dockerizePip: true/dockerizePip: false/' serverless.yml && pipenv install --dev --system && pipenv install --system && npm install -g serverless

RUN chown -R lambdadev:lambdadev /demo
USER lambdadev

CMD ["/bin/bash"]