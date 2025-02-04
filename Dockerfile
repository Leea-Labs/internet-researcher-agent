FROM python:3.12-slim-bullseye

WORKDIR /opt/app

RUN apt-get update && \
    apt-get satisfy -y "chromium, chromium-driver (>= 115.0)" && \
    apt-get install -y --no-install-recommends firefox-esr wget build-essential git && \
    wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz && \
    tar -xvzf geckodriver-v0.33.0-linux64.tar.gz && \
    chmod +x geckodriver && \
    mv geckodriver /usr/local/bin/ && \
    rm geckodriver-v0.33.0-linux64.tar.gz && \
    chromium --version && chromedriver --version && \
    rm -rf /var/lib/apt/lists/*  # Clean up apt lists to reduce image size

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./

ENTRYPOINT ["python", "main.py"]
