package com.devtools.service;

import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class AnalysisService {

    public Map<String, Object> analyzeCode(String code) {
        int lineCount = code.split("\n").length;
        return Map.of(
                "lineCount", lineCount,
                "status", "analyzed"
        );
    }
}
