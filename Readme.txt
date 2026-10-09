Week 5 - Day 2: AutoGen Weather News agent.

Takes a city from the user, searches DuckDuckGo news (no API key needed),
and replies in exactly 3 short lines.

Setup:
    pip install -U ddgs autogen-agentchat "autogen-ext[openai]"
    export OPENAI_API_KEY="sk-..."      # Windows: setx OPENAI_API_KEY "sk-..."
Run:
    python weather_news.py
