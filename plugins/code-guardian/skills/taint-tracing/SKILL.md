---
name: Taint Tracing
description: Trace untrusted input from request handlers to sinks.
---

# Taint Tracing

Start from the route handler, follow the parameter to every sink (query, exec, template, file path) and record the path.
