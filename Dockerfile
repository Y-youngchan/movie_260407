FROM python:3.13-slim

ENV TZ=Asia/Seoul \
    FLASK_APP=pybo:create_app \
    FLASK_ENV=production \
    FLASK_DEBUG=0 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN flask db stamp head --purge

EXPOSE 5000

CMD ["sh", "-c", "flask db upgrade && exec gunicorn --bind 0.0.0.0:${PORT:-5000} 'pybo:create_app()'"]
