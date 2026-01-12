# Minimal research container (CPU base). Swap to nvidia/cuda for GPU/Jetson builds.
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY README.md ./

CMD ["python", "-m", "src.main", "--source", "0"]
