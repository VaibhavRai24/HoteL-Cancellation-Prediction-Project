FROM python:slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install -e

RUN pip install --no-cache-dir -r requirements.txt

RUN python HoteL-Cancellation-Prediction-Project\src\HotelCancellationPrediction\pipeline\training.py

EXPOSE 5000

CMD ["python", "application.py"]

