# Astrid: a local AI desktop assistant

Astrid is a desktop assistant that runs a language model **locally** via
[Ollama](https://ollama.com). No cloud service, no API key, nothing leaves the machine.

This is a learning project I am building up step by step, from a plain chat loop toward
an assistant that can actually operate the system.

## Idea

Most assistants either send everything to a server or can't do anything useful on your
machine. Astrid is the other way around: the model runs locally, and the actions are
plain Python functions the model is allowed to call. The model produces text and tool
call requests, and Python does the actual work. Keeping that boundary clean is the core
design decision of the project.

## Current state

**Early stage, work in progress.** What exists today:

- Chat loop against a local Ollama instance (`ollama.chat()`)
- Message/history handling with conversion into the Ollama message format
- System prompt with identity, response rules and dynamic context (date/time, OS info)
- Tuned model parameters for a responsive assistant rather than a chatbot essay machine

## Roadmap

| Stage | Scope |
|-------|-------|
| V1 | First tools: open applications, clipboard, time/date, web search |
| V2 | System control via `pyautogui`, `psutil`, `subprocess` |
| V3 | Persistent memory across sessions |
| V4 | Local voice: `faster-whisper` (STT), Piper/Kokoro (TTS), `openWakeWord` (wake word) |

## Tech

- Python
- Ollama, running locally on port `11434`
- Qwen3 (8B/14B), chosen for native tool calling; runs on a 12 GB VRAM GPU
- Ollama Python client

## Notes from building it

A few things that cost me time and might save yours:

- **Qwen3's thinking mode splits the output** into `thinking` and `content`. With a low
  `num_predict` the reply gets cut off before `content` is ever filled, and you get an
  empty response that looks like a bug somewhere else. `think=False` is the fix for a
  fast assistant.
- **Useful parameters:** `temperature` 0.6–0.7 for reliable tool calling,
  `num_predict: 256` as a reply length cap, `num_ctx: 8192` against context amnesia.
- **Tool calling is a four-step round trip:** model requests a call → Python executes it
  → the result goes back to the model → the model writes the final answer.

## Requirements

- Python 3.11+
- Ollama installed and running
- A pulled model, e.g. `ollama pull qwen3:8b`

## Run

```bash
pip install ollama
python main.py
```
