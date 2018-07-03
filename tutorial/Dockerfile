FROM lambci/lambda:build-python3.6

RUN curl https://nodejs.org/dist/v8.2.1/node-v8.2.1-linux-x64.tar.xz | tar -xJ -C /opt && pushd . && \
  ln -fs /opt/node-v8.2.1-linux-x64/bin/* /usr/bin/.

RUN chmod --recursive 777 /tmp && groupadd -g 1000 lambdadev \
        && adduser -u 1000 -g lambdadev -s /bin/bash lambdadev

RUN pip install pipenv pytest && pip install -U awscli

COPY . /workd/
RUN cd /workd && make clean && make setup

USER lambdadev

CMD ["/bin/bash"]