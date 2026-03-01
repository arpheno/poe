# Stage 1: Build the Angular application
FROM node:20-slim AS builder

# Set working directory
WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies with npm ci for more reliable builds
RUN npm ci

# Copy the rest of the application code
COPY . .

# Build the application with production configuration
RUN npm run build --configuration=production

# Stage 2: Serve with nginx
FROM nginx:1.25-alpine

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built application from builder stage
COPY --from=builder /app/dist/getting-rich /usr/share/nginx/html

# Add non-root user
RUN adduser -D -H -u 1001 -G www-data www-data && \
    chown -R www-data:www-data /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# Configure nginx
RUN touch /var/run/nginx.pid && \
    chown -R www-data:www-data /var/run/nginx.pid && \
    chown -R www-data:www-data /var/cache/nginx

# Switch to non-root user
USER www-data

# Expose port 8080 instead of 80 for non-root binding
EXPOSE 8080

# Use environment variables for configuration
ENV PORT=8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget -q --spider http://localhost:8080/ || exit 1
