package service

import (
	"os"
	"strings"

	"github.com/devtools-engine/go-service/internal/model"
)

// Scanner performs security analysis on files.
type Scanner struct{}

// NewScanner creates a new Scanner instance.
func NewScanner() *Scanner {
	return &Scanner{}
}

// AnalyzeFile reads and analyzes a file for security issues.
func (s *Scanner) AnalyzeFile(path string) (*model.AnalysisResult, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	content := string(data)
	findings := []string{}
	if strings.Contains(content, "password") {
		findings = append(findings, "potential hardcoded credential")
	}
	if strings.Contains(content, "eval(") {
		findings = append(findings, "dangerous eval usage")
	}
	return &model.AnalysisResult{
		Findings: findings,
		Severity: "medium",
	}, nil
}
