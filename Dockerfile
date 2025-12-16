FROM python:3
ARG UNAME=wikibot
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME
USER $UNAME

WORKDIR /pwb
RUN git clone --recurse-submodules --shallow-submodules --depth 1 https://gerrit.wikimedia.org/r/pywikibot/core.git --branch 10.7.2
WORKDIR  /pwb/core
RUN pip install -r requirements.txt

WORKDIR /wmb
COPY . .
RUN pip install -r requirements.txt
ENV PWB_USERNAME=WikiBot

ENTRYPOINT ["/wmb/entrypoint.sh"]
