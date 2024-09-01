FROM tensorflow/tensorflow:latest-jupyter

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt install cmake -y

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt --ignore-installed embedchain

COPY . /code/app

RUN mkdir /video


CMD ["fastapi", "run", "app/main.py", "--port", "80"]