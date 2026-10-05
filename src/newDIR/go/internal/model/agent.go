package model

import "time"

// Agent represents a security scanning agent.
type Agent struct {
	ID        string    `json:"id" bson:"_id"`
	Name      string    `json:"name" bson:"name"`
	Type      string    `json:"type" bson:"type"`
	Status    string    `json:"status" bson:"status"`
	CreatedAt time.Time `json:"created_at" bson:"created_at"`
}

// AnalysisResult holds the output of a security scan.
type AnalysisResult struct {
	AgentID   string   `json:"agent_id" bson:"agent_id"`
	Findings  []string `json:"findings" bson:"findings"`
	Severity  string   `json:"severity" bson:"severity"`
	Timestamp time.Time `json:"timestamp" bson:"timestamp"`
}
