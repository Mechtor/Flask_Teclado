FROM python:3.10
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]
