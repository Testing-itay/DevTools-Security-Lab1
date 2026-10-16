
# Stage 1: builder
FROM maven:3.9-eclipse-temurin-21 as builder

WORKDIR /app

COPY src/java/pom.xml .
RUN mvn dependency:go-offline -B

COPY src/java .
RUN mvn package -DskipTests -B

# Stage 2: runtime
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

COPY --from=builder /app/target/*.jar app.jar

EXPOSE 8081

ENTRYPOINT ["java", "-jar", "app.jar"]
