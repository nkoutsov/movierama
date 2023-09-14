# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /movie_rating_app

# Copy the current directory contents into the container at /app
COPY . /movie_rating_app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World
ENV FLASK_ENV=development


# Run app.py when the container launches
CMD [ "flask", "--app", "movie_rating_app", "run", "--host=0.0.0.0", "--port=8080"]