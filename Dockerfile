FROM python:3.11-slim
WORKDIR /books
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH ./

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
RUN chmod a+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]