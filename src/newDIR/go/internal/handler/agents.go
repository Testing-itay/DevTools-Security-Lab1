package handler

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/devtools-engine/go-service/internal/model"
)

// ListAgents returns all agents.
func ListAgents(c *gin.Context) {
	agents := []model.Agent{}
	c.JSON(http.StatusOK, agents)
}

// GetAgent returns a single agent by ID.
func GetAgent(c *gin.Context) {
	id := c.Param("id")
	if id == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "id required"})
		return
	}
	c.JSON(http.StatusOK, model.Agent{ID: id})
}

// CreateAgent creates a new agent.
func CreateAgent(c *gin.Context) {
	var agent model.Agent
	if err := c.ShouldBindJSON(&agent); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusCreated, agent)
}

// DeleteAgent deletes an agent by ID.
func DeleteAgent(c *gin.Context) {
	id := c.Param("id")
	if id == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "id required"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"deleted": id})
}
