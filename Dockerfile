FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1     METRON_MODE=user     METRON_TARGET=octocat     GITHUB_TOKEN=     PORT=5000
EXPOSE 5000
CMD ["python", "-m", "gitscanner.dashboard"]
