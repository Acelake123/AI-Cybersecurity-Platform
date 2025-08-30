
# Adapter Dockerfile for cowrie repo
FROM python:3.10-slim
WORKDIR /opt/cowrie
COPY . /opt/cowrie
RUN pip install --no-cache-dir -r requirements.txt || true
CMD ["bash","-lc","if [ -f bin/cowrie ]; then bin/cowrie start; else echo 'Cowrie adapter: no runnable cowrie found, sleeping'; tail -f /dev/null; fi"]
