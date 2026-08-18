FROM python:3.11-slim
WORKDIR /app
COPY demo01_modeling_agent/app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY demo01_modeling_agent/app/ .
COPY common/data/raw_logbook_sample.json /common/data/raw_logbook_sample.json
ENV PORT=8080
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
