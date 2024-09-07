FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

# Command to run the application
CMD ["sh", "-c", "main.py"]