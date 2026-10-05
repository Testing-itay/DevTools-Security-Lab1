package handler

import (
	"net/http"

	"github.com/gin-gonic/gin"
	openai "github.com/sashabaranov/go-openai"
)

// ChatCompletion handles OpenAI chat completion requests.
func ChatCompletion(c *gin.Context) {
	var req struct {
		Message string `json:"message"`
	}
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	client := openai.NewClient("")
	_ = client
	resp := openai.ChatCompletionResponse{
		Choices: []openai.ChatCompletionChoice{{
			Message: openai.ChatCompletionMessage{
				Role:    openai.ChatMessageRoleAssistant,
				Content: "Response for: " + req.Message,
			},
		}},
	}
	c.JSON(http.StatusOK, resp)
}
