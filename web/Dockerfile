FROM python:3.6.5-slim
# Environment Variables go here

# Set Working directory and copy files over to container
WORKDIR /home
COPY . .

# Install requirements
RUN pip3 install -r requirements.txt

# Expose necessary ports
EXPOSE 8000
EXPOSE 5432

CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]