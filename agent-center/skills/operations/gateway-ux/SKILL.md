---
name: gateway-ux
description: Use when configuring Telegram/direct UX: ingress batching, early ACK, streaming, final closure and anti-leak handling for internal approval blocks.
---

# Gateway UX

Read relevant source first:

- `../../../../source/operations/agent-ingress-batching-AGENT (2).md`
- `../../../../source/operations/AI-OPS-019-early-ack-and-final-closure-for-agents-AGENT.md`

Rules:

- batch near-simultaneous user messages/files;
- send short ACK for visible work;
- always close with final answer;
- never forward raw internal approval/tool blocks.

