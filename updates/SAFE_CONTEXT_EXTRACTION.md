# Safe Context Extraction Rollout

## Summary
- Routed all conversation context extraction through `extract_context_safe` to align chat handling with the safeguards layer.
- Updated `src/routes/chatbot.py` and `src/services/message_handler.py` to use the protected extractor.
- Documented the migration path, request flow, and guardrails for the new extractor.

## Migration notes
- Replaced the legacy context extractor with `extract_context_safe` in the chatbot route so every new conversation is hydrated through the safeguarded path.
- Simplified `MessageHandler` to rely solely on the validated payload returned by `extract_context_safe`, removing the legacy fallback logic.

## Request flow in `src/routes/chatbot.py`
1. A new conversation is created with an empty `context_data` payload.
2. `extract_context_safe` receives the incoming user message plus the current in-memory context (initially `{}`) and returns a sanitized context.
3. The sanitized context is persisted back to `context_data` before any downstream processing occurs.
4. Subsequent routing (booking intent, learned FAQ, standard FAQ, GPT) consumes only the validated context returned by step 2.

## Expected behaviors and guardrails
- All newly created conversations are hydrated through `extract_context_safe`; there is no remaining fallback to the legacy extractor.
- Persisted context data contains only sanitized keys/values produced by the safeguarded extractor.
- Message processing logic never reads user-supplied context directly; it consumes only the validated payload returned by `extract_context_safe`.

## Testing
- `pytest`
