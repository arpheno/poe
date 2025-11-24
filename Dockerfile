# start from an official image
FROM python:3.9-slim

# arbitrary location choice: you can change the directory
RUN mkdir -p /opt/services/djangoapp/src
WORKDIR /opt/services/djangoapp/src

# install our dependencies
# we use --system flag because we don't need an extra virtualenv
COPY requirements.txt /opt/services/djangoapp/src/
RUN pip install -r requirements.txt
RUN pip install gunicorn
# copy our project code
COPY frontend/thinking /opt/services/djangoapp/src
COPY  poe /opt/services/djangoapp/src/poe
COPY  poe/constants.py /opt/services/djangoapp/src/
RUN python manage.py collectstatic --no-input -v 2

# expose the port 8000
EXPOSE 80
ENV PYTHONUNBUFFERED=1

# define the default command to run when starting the container
CMD ["gunicorn", "--chdir", "thinking", "--bind", ":80", "thinking.wsgi:application"]

# Build stage
FROM node:16.20.2-slim AS builder

# Set working directory
WORKDIR /app

# Install Angular CLI globally first
RUN npm install -g @angular/cli@13.1.2

# Copy package files from the correct location
COPY frontend/getting-rich/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY frontend/getting-rich/ .

# Build the application
RUN ng build --configuration=production

# Production stage
FROM nginx:1.25-alpine

# Create non-root user
RUN adduser -D -u 1001 appuser && \
    mkdir -p /var/cache/nginx /var/run /var/log/nginx && \
    chown -R appuser:appuser /var/cache/nginx /var/run /var/log/nginx && \
    chmod -R 755 /var/cache/nginx /var/run /var/log/nginx

# Copy nginx configuration
COPY docker/nginx.conf /etc/nginx/nginx.conf

# Copy built files from builder stage
COPY --from=builder /app/dist/getting-rich /usr/share/nginx/html

# Set permissions for nginx directories
RUN chown -R appuser:appuser /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html && \
    chown -R appuser:appuser /etc/nginx/nginx.conf && \
    chmod 644 /etc/nginx/nginx.conf

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Start nginx
CMD ["nginx", "-g", "daemon off;"]