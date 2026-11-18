# Korean Shorts Script AI

Streamlit app that generates 숏폼 애니메이션/웹툰 scripts and per-scene image prompts with Gemini.

## Structure
```
app.py            UI only
core/config.py    secrets + option lists
core/schema.py    pydantic models (also the Gemini output schema)
core/prompts.py   prompt building
core/generator.py Gemini API wrapper
core/export.py    Markdown / SRT export (pure functions)
tests/            pytest
```

## Run
```
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # add your key
streamlit run app.py
```
Streamlit Cloud: put `GEMINI_API_KEY` in the Secrets panel.

## Test
```
pip install -r requirements-dev.txt && pytest
```
