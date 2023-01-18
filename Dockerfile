FROM python:3.10-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
COPY . .
ENTRYPOINT ["/usr/local/bin/flask"]
CMD ["run", "--host=0.0.0.0"]