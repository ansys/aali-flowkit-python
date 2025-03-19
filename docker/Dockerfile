FROM python:3.12-slim

# Create a non-root user and group
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Set the home directory for the non-root user
ENV HOME=/home/appuser
ENV PATH="$HOME/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Set the ownership of the /app directory to the non-root user
RUN chown -R appuser:appgroup /app

# Copy the application files and config.yaml, setting ownership to the non-root user
COPY --chown=appuser:appgroup src /app
COPY --chown=appuser:appgroup README.md /app
COPY --chown=appuser:appgroup pyproject.toml /app
COPY --chown=appuser:appgroup configs/config.yaml /app
COPY --chown=appuser:appgroup LICENSE /app

# Switch to the non-root user
USER appuser

# Create a virtual environment and install dependencies inside it
RUN python -m venv /app/venv \
    && . /app/venv/bin/activate \
    && pip install --upgrade pip \
    && pip install --no-cache-dir .[all]

# Expose the port that the service will listen on
EXPOSE 50052

# Activate the virtual environment and run the service
CMD ["/bin/sh", "-c", ". /app/venv/bin/activate && allie-flowkit-python"]
