# Build stage
FROM gradle:7.6.1-jdk17 AS build

WORKDIR /home/gradle/project
COPY --chown=gradle:gradle . .

RUN gradle build --no-daemon

# Execution stage
FROM openjdk:17-jdk-slim

WORKDIR /app
COPY --from=build /home/gradle/project/build/libs/*.jar app.jar

# Directory for storing static files
RUN mkdir /static
# Root directory for FileSystemResource
RUN mkdir /app/static
# Symbolic link from the FileSystemResource directory to the static files directory
RUN ln -s /static /app/static/link

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
