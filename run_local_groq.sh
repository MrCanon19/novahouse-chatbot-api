#!/usr/bin/env bash

# Prosty start lokalny z Groq albo dummy
# Zakładam, że venv masz już aktywny

echo "Ustawiam domyslnego providera na groq (jeśli nie ustawiony)..."
export LLM_PROVIDER="${LLM_PROVIDER:-groq}"

echo "Startuję backend na main.py z LLM_PROVIDER=$LLM_PROVIDER"
python main.py
