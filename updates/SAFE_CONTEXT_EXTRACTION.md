# Safe Context Extraction Rollout

## Summary
- Routed all conversation context extraction through `extract_context_safe` to align chat handling with the safeguards layer.
- Updated `src/routes/chatbot.py` and `src/services/message_handler.py` to use the protected extractor.

## New behavior
- New conversations always use the validated context extractor before persisting memory.
- MessageHandler consumes only sanitized context payloads.

## Testing
- `pytest`
