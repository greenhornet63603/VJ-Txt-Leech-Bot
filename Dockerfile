# Don't Remove Credit @VJ_Bots
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

FROM python:3.10-slim

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    gcc libffi-dev ffmpeg aria2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Better: choose ONE entrypoint (recommended for Render bots)
CMD ["python3", "main.py"]
