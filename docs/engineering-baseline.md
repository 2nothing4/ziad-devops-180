# Day 34: Engineering Baseline & Inventory

**Date:** November 1, 2026
**Objective:** Record defects, duplicate files, and current working commands.

## 1. Known Defects & Technical Backlog
- [ ] **Helm Chart Conflict:** Duplicate charts (`helm/ziad-devops` and `ziad-devops-chart`). Need to consolidate.
- [ ] **Terraform Subnet Bug:** RDS subnet group only has 1 AZ. Needs 2. Missing NAT Gateway.
- [ ] **Test Suite Gap:** `/cache` endpoint is not actually tested.
- [ ] **Hardcoded Secrets:** Found demo passwords in config files.
- [ ] **CI Security Gate:** Checkov has `soft_fail: true`.
- [ ] **Repo Hygiene:** `.terraform/` folder and `.tfstate` files tracked in Git.