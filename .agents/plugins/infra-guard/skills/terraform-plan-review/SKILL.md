---
name: terraform-plan-review
description: Review a Terraform plan before apply. Use when a PR changes files under infrastructure/ or when a plan output is shared.
---

# Terraform plan review

1. Flag every resource the plan destroys or replaces.
2. Flag security groups or firewall rules that open a port to `0.0.0.0/0`.
3. Flag IAM changes that add `*` to actions or resources.
4. Approve only when each flagged item has a reason in the PR.
