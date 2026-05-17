---
title: Rowan Brand Assets — Canonical Project Brief
status: active
owner: Mitch Metz
steward: Glarth
last_reviewed: 2026-05-17
next_review: monthly
canonical: true
classification: public-safe
---

# Rowan Brand Assets — Canonical Project Brief

## Source request

Mitch asked for one public GitHub repo that gathers Rowan branding material: copywriting guidelines, design guidelines, icon direction, colors, fonts, carousel generation, PDF generation notes, and brand voice, without breaking existing Knowledgebase references or exposing API/private material.

## Executive summary

This repo is the public-safe Rowan brand package. It is for collaborators who need clear brand guidance and reusable production tools without needing access to internal Rowan strategy or private client context.

## Current scope in one sentence

Maintain one public-safe brand source for Rowan Builder Marketing with clickable GitHub-ready references and clear separation from private/internal material.

## Must include

- Brand and design guidelines
- Copywriting and voice guidance
- Color, typography, icon, and logo rules
- Public-safe logo assets
- Quote-card/carousel generator notes and tool
- PDF/carousel production notes
- Source map, governance, and change history

## Must not include

- API keys, credentials, analytics IDs, tokens, or login details
- Customer or client data
- Private Rowan strategy or internal-only operating notes
- Licensed font binaries
- Cross-client context

## Success criteria

- A reader can start from [README](../README.md) and understand the brand system quickly
- All references work as clickable GitHub or Rowan links
- The package audit passes before material updates are called complete
- Existing Knowledgebase brand references keep working through compatibility bridges

## Open decisions

- None currently

## Risks and guardrails

- Risk: public repo accidentally accumulates internal/private context — Guardrail: follow [.repo-policy.yaml](../.repo-policy.yaml) and stage ambiguous material internally first
- Risk: old website references drift — Guardrail: keep [source map](source-map.md) and compatibility notes updated
- Risk: tool docs expose local/internal assumptions — Guardrail: keep public docs path-relative and credential-free

## Key links

- [Source map](source-map.md)
- [Tools and accounts](tools-and-accounts.md)
- [Governance](governance.md)
- [Change log](change-log.md)
- [Call notes](call-notes/README.md)
- [Archive guide](../archive/README.md)
