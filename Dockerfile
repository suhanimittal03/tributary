FROM python:3.10
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./entrypoint.py .
# CMD echo "Hello World"
# CMD python entrypoint.py
CMD exec gunicorn entrypoint:app