# 1. Start with a lightweight Linux computer that already has Python 3.10 installed
FROM python:3.10-slim

# 2. Create a folder inside that Linux computer called /app
WORKDIR /app

# 3. Copy your requirements list from your Windows laptop to the Linux computer
COPY requirements.txt .

# 4. Tell the Linux computer to install all your packages
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your actual Python code from your laptop to the Linux computer
COPY travel_api.py .

# 6. Open port 8000 so the FastAPI Receptionist can hear the outside world

EXPOSE 7860
CMD ["uvicorn", "travel_api:api", "--host", "0.0.0.0", "--port", "7860"]