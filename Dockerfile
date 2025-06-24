FROM python:3.11-slim-bookworm

WORKDIR /app

# Install system dependencies (tambahan: build-essential, gcc, rustc, dll)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    libatlas-base-dev \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    rustc \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python deps
COPY requirements.txt .

# Install pip packages (gunakan --use-pep517 supaya build wheel modern)
RUN pip install --upgrade pip setuptools wheel && \
    pip install --use-pep517 -r requirements.txt

# Download OCR model
RUN mkdir -p /app/models/det_model /app/models/rec_model && \
    wget -qO - https://paddle-model-ecology.bj.bcebos.com/paddlex/official_inference_model/paddle3.0.0/PP-OCRv5_server_det_infer.tar \
    | tar -xC /app/models/det_model --strip-components=1 && \
    wget -qO - https://paddle-model-ecology.bj.bcebos.com/paddlex/official_inference_model/paddle3.0.0/PP-OCRv5_server_rec_infer.tar \
    | tar -xC /app/models/rec_model --strip-components=1

# Optional: hapus wget (tapi perintahmu typo)
RUN apt-get purge -y wget

ENV DET_MODEL_DIR=/app/models/det_model
ENV REC_MODEL_DIR=/app/models/rec_model

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
