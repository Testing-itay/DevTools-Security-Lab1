package main

import (
	"context"
	"log"

	"github.com/gin-gonic/gin"
	"github.com/devtools-engine/go-service/internal/auth"
	"github.com/devtools-engine/go-service/internal/handler"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/sdk/trace"
)

func main() {
	tp := trace.NewTracerProvider()
	otel.SetTracerProvider(tp)
	defer func() { _ = tp.Shutdown(context.Background()) }()

	r := gin.Default()
	r.Use(gin.Recovery())

	r.GET("/health", handler.Health)
	r.GET("/metrics", gin.WrapH(promhttp.Handler()))

	api := r.Group("/api")
	api.Use(auth.JWTMiddleware())
	{
		api.GET("/agents", handler.ListAgents)
		api.GET("/agents/:id", handler.GetAgent)
		api.POST("/agents", handler.CreateAgent)
		api.DELETE("/agents/:id", handler.DeleteAgent)
		api.POST("/ai/chat", handler.ChatCompletion)
	}

	if err := r.Run(":8080"); err != nil {
		log.Fatal(err)
	}
}
