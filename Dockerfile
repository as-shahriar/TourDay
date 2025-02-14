FROM python:3.7
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update && \
    apt-get install -y curl build-essential
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN cargo --version
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 8000

WORKDIR /code/TourDay
RUN python manage.py makemigrations
RUN python manage.py migrate