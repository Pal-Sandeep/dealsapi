# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.11.7
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# creating a non-root user
ARG USERNAME=backendbuilder
ARG USER_UID=10001
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
#RUN --mount=type=cache,target=/root/.cache/pip \
 #   --mount=type=bind,source=requirements.txt,target=requirements.txt \
#    python -m pip install -r requirements.txt
COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER backendbuilder

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8001

# Run the application.
# CMD ["gunicorn", "--bind", "0.0.0.0:8001", "backend.asgi:application"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
