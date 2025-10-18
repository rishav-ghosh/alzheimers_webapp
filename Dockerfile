FROM python:3.10

WORKDIR /app

# Copy your code (but *not* the large model file)
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create model directory
RUN mkdir -p /app/model

# Download the model file from Google Drive
RUN pip install gdown
RUN gdown "https://drive.google.com/uc?id=1JlZI7v9G9SLjlAu8ogFdJtNdYuPxX2Dc" -O /app/model/resnet101_extraData_5epochs.pth


EXPOSE 5000

CMD ["python3", "app.py"]
