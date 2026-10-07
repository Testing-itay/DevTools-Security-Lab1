---
name: log-triage
description: Find the cause of an error from service logs. Use when a user reports an error and gives a time or a correlation ID.
---

# Log triage

1. Search the logs by correlation ID first. Use the time window only when no ID
   is given.
2. Follow the ID across services and find the first service that logged an
   error.
3. Report that service, the error message and the request that caused it.
