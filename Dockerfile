FROM python:3.7 − alpine
WORKDIR /MiniProject
COPY . /MiniProject
RUN pip install −r requirements.txt
EXPOSE 5000
CMD ["python", "MiniProjectApp.py"]
