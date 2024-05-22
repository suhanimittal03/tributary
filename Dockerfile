FROM python:3.10
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./test_file.py .
COPY ./entrypoint.py .
# CMD echo "Hello World"
# CMD python entrypoint.py
CMD exec gunicorn --bind 0.0.0.0:8000 entrypoint:app