FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (layer-cached)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Uploaded photos and favicons are stored here; mount a volume over this path
RUN mkdir -p static/uploads/photos static/uploads/favicon

EXPOSE 8000

ENTRYPOINT ["bash", "entrypoint.sh"]
