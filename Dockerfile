FROM python:3.13

RUN mkdir /hotel_app

WORKDIR /hotel_app

COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY . .

RUN chmod a+x /hotel_app/docker/*.sh

CMD ["gunicorn" , "app.main:app" , "--workers" , "4" , "--worker-class" , "uvicorn.workers.UvicornWorker" ,"--bind=0.0.0.0:8000"]
