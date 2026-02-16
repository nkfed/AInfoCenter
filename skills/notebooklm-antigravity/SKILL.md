---
name: notebooklm-antigravity
description: Доступ до приватної бази знань ЕСОЗ через NotebookLM. Пошук у нотатниках (МСЕК, єКров, ДЗР, BPG).
metadata: {"clawdbot": {"emoji": "📚", "always": true}}
---

# NotebookLM Anti-gravity

Інструмент для взаємодії з приватною бібліотекою NotebookLM (eHealth / ЕСОЗ).

## When to use

- Коли потрібна інформація про ЕСОЗ (електронна система охорони здоров'я)
- Питання про МСЕК, єКров, ДЗР, BPG, eHealth
- Пошук у приватній базі знань з медичних нотатників
- Робота з медичною документацією та нормативами

## Tools

All tools are executed via bash. The script path is: `{baseDir}/notebooklm.sh`

### list_notebooks

List all available notebooks and their IDs.

```bash
bash {baseDir}/notebooklm.sh list
```

Returns JSON: `{"success": true, "notebooks": [...], "count": N}`

### query_notebook

Ask a question to a specific notebook.

Parameters:
- `notebook_id` (required): notebook ID from list_notebooks output
- `query` (required): question in Ukrainian or English

```bash
bash {baseDir}/notebooklm.sh query "<notebook_id>" "<query>"
```

Example:
```bash
bash {baseDir}/notebooklm.sh query "notebook-18-ekopfo-msek" "Які документи потрібні для проходження МСЕК?"
```

### create_summary

Get a concise summary of a notebook.

```bash
bash {baseDir}/notebooklm.sh summary "<notebook_id>"
```

## Workflow

1. Always run `list` first to get available notebook IDs.
2. Then `query` a specific notebook with the user's question.
3. Use `summary` when the user wants a general overview.

## Available Notebooks (reference)

- notebook-0-common-questions — Загальні питання
- notebook-1-bpg-esoz — BPG ЕСОЗ
- notebook-2-clinical-impression-processes — Клінічні враження
- notebook-3-medical-devices — Медичні вироби
- notebook-4-technical-rehabilitation — Технічна реабілітація
- notebook-5-technical-composition — Технічний склад
- notebook-6-technical-prescriptions — Технічні рецепти
- notebook-7-personal-cabinet — Особистий кабінет
- notebook-8-technical-foreigners — Іноземці
- notebook-9-MyHealth@EU — MyHealth@EU
- notebook-10-public-health-information-platform — Платформа публічного здоров'я
- notebook-11-e-krov — єКров
- notebook-12-cosmetic-products-notification — Косметичні продукти
- notebook-13-endoprosthetics-queues — Черги ендопротезування
- notebook-14-job-vacancy-portal — Портал вакансій
- notebook-15-professional-development — Професійний розвиток
- notebook-16-esrr-internship — ЕСРР стажування
- notebook-18-ekopfo-msek — МСЕК (еКОПФО)
- notebook-19-assistive-devices — Допоміжні засоби
- notebook-20-notebooklm-antigravity — NotebookLM Antigravity

## Notes

- All responses are JSON. Parse them and present results in user-friendly format.
- Notebooks contain Ukrainian medical/eHealth documentation.
- Answer the user in the language they asked in (usually Ukrainian).
