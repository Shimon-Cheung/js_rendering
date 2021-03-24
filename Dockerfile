FROM centos

COPY main.py main.py

COPY requirements.txt requirements.txt

RUN yum groupinstall "Development tools" -y

RUN yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel xz-devel libffi-devel wget -y

RUN wget https://www.python.org/ftp/python/3.9.2/Python-3.9.2.tgz

RUN mkdir /usr/local/python3 -p && tar zvxf Python-3.9.2.tgz && cd Python-3.9.2 && ./configure --prefix=/usr/local/python3 --enable-optimizations && make && make install

RUN ln -s /usr/local/python3/bin/python3 /usr/local/bin/python && ln -s /usr/local/python3/bin/pip3 /usr/local/bin/pip

RUN yum install xorg-x11-fonts-100dpi xorg-x11-fonts-75dpi xorg-x11-utils xorg-x11-fonts-cyrillic xorg-x11-fonts-Type1 xorg-x11-fonts-misc -y

RUN yum install pango.x86_64 libXcomposite.x86_64 libXcursor.x86_64 libXdamage.x86_64 libXext.x86_64 libXi.x86_64 libXtst.x86_64 cups-libs.x86_64 libXScrnSaver.x86_64 libXrandr.x86_64 GConf2.x86_64 alsa-lib.x86_64 atk.x86_64 gtk3.x86_64 -y

RUN cd / && pip install --upgrade pip && pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt

RUN /usr/local/python3/bin/pyppeteer-install

EXPOSE 8050

CMD /usr/local/python3/bin/uvicorn main:app --reload --host '0.0.0.0' --port 8050