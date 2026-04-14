FROM python:3.14-slim

WORKDIR /app

COPY ./ .

RUN pip install --upgrade pip && \
    if [ -f requirements.txt ]; then \
        pip install -r requirements.txt; \
    else \
       echo "No requirements.txt found" >&2; \
    fi

EXPOSE 8088

CMD ["python", "main.py"]
