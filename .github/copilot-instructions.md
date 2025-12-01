# AI Coding Agent Instructions - LangChain Ollama Chat

## Project Overview
This is a minimal **LangChain + Ollama + Streamlit** chat application. The system chains together:
- **Streamlit** for the UI layer (`app.py`)
- **LangChain** for prompt management and LLM orchestration
- **Ollama** as the local LLM backend (model specified via `OLLAMA_MODEL` env var, defaults to `llama3.2`)

**Key Architecture Pattern**: Simple chain-based approach where user input flows through a templated prompt system to the Ollama model.

## Critical Workflows

### Running the Application
```bash
# Prerequisites: Ollama running locally (default: http://localhost:11434)
python -m pip install --upgrade pip
python -m pip install streamlit langchain ollama
python -m streamlit run ./app.py
```
The app runs on `http://localhost:8501` by default.

### Environment Configuration
- `OLLAMA_MODEL`: Set the model to use (default: `llama3.2`)
- Ollama must be running as a separate service before starting the app
- No authentication configured - assumes local deployment

## Code Patterns & Conventions

### LangChain Prompt Structure
**Pattern**: Use `ChatPromptTemplate` with `SystemMessagePromptTemplate` + `HumanMessagePromptTemplate` for multi-turn structure.

Example from `app.py`:
```python
system = SystemMessagePromptTemplate.from_template("You are a helpful assistant.")
human = HumanMessagePromptTemplate.from_template("{user_input}")
chat_prompt = ChatPromptTemplate.from_messages([system, human])
```

**Why**: Provides semantic separation between system instructions and user queries, matching OpenAI chat API semantics.

### LLMChain Pattern
Use `LLMChain(llm=llm, prompt=chat_prompt).run()` with dict inputs matching template variables:
```python
chain = LLMChain(llm=llm, prompt=chat_prompt)
response = chain.run({"user_input": user_input})
```

### Streamlit UI Patterns
- **Input**: `st.text_input()` for single-line user queries
- **Async handling**: Wrap LLM calls in `with st.spinner()` context
- **Output**: `st.write()` for response display
- **Interactivity**: Button check: `if st.button() and input_value:`

## Integration Points

### Ollama Backend
- Ollama runs on `http://localhost:11434` by default
- `Ollama()` class from LangChain auto-discovers this endpoint
- Model must be pre-downloaded: `ollama pull llama3.2`
- **No error handling** currently for Ollama unavailability - consider adding try/catch

### Dependencies
- `langchain`: Prompt templates, LLMChain orchestration
- `streamlit`: Web UI framework
- `ollama`: Python client for Ollama API

## Known Limitations & Improvement Areas

1. **No conversation history**: Each query is independent (no memory context)
2. **No error handling**: Missing try/except for Ollama unavailability or malformed responses
3. **Hardcoded system prompt**: "You are a helpful assistant." - could be configurable via UI or env var
4. **Package installation in runtime**: `app.py` contains `os.system()` calls at module level (lines 28-30) - should be pre-installation step instead
5. **Single-turn only**: No session state for multi-turn conversations

## When Extending This Codebase
- Keep LangChain prompt composition patterns consistent with the existing template structure
- Any new features should maintain the `user_input → chain.run() → st.write()` flow
- Consider adding error boundaries before calling `chain.run()`
- For multi-turn support, use Streamlit's `st.session_state` with LangChain's conversation memory classes
