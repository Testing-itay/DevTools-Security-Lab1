


# Stage 1: builder
FROM golang:1.21-alpine as builder

WORKDIR /app

COPY src/go/go.mod ./
RUN go mod download
COPY src/go .
RUN CGO_ENABLED=0 go build -o /server ./cmd/server

# Stage 2: runtime
FROM alpine:3.19

WORKDIR /app

COPY --from=builder /server .

EXPOSE 8080

ENTRYPOINT ["./server"]
