"""Week 5 - Day 2: AutoGen Weather News agent.

Takes a city from the user, searches DuckDuckGo news (no API key needed),
and replies in exactly 3 short lines.

Setup:
    pip install -U ddgs autogen-agentchat "autogen-ext[openai]"
    export OPENAI_API_KEY="sk-..."      # Windows: setx OPENAI_API_KEY "sk-..."
Run:
    python weather_news.py
"""
from dotenv import load_dotenv
load_dotenv()
import asyncio
import os
import sys

from ddgs import DDGS
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


def search_weather_news(city: str) -> str:
    """Search the web for TODAY'S weather news for one city.

    Use this tool whenever the user asks about current weather, today's
    forecast, rain, storms, heat, or weather alerts in a specific city.
    Do not use it for general trivia, history, or non-weather questions.

    Args:
        city: Name of the city to look up, e.g. "Chennai" or "London".

    Returns:
        A string holding up to 5 recent news results (title, date, source,
        summary) about today's weather in that city, or an error message
        if the search failed.
    """
    try:
        results = DDGS().news(query=f"{city} weather today", max_results=5)
    except Exception as exc:  # network problems, rate limits, etc.
        return f"Search failed for {city}: {exc}"
    if not results:
        return f"No weather news found for {city}."
    return str(results)


SYSTEM_MESSAGE = (
    "You are a weather news reporter. "
    "Always call the search_weather_news tool for the city you are given; "
    "never answer from memory. "
    "Then reply in EXACTLY 3 short lines of plain text, one sentence each: "
    "line 1 is today's main weather headline, "
    "line 2 is a key detail such as temperature, rain or wind, "
    "line 3 is any alert or what to expect next. "
    "No bullets, no numbering, no blank lines, no extra text. "
    "Use only facts found in the search results."
)


async def main() -> None:
    # The key lives in an environment variable, never in the code.
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        sys.exit("Set the OPENAI_API_KEY environment variable first.")

    city = input("Which city? ").strip()
    if not city:
        sys.exit("Please enter a city name.")

    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", api_key=api_key)

    agent = AssistantAgent(
        name="weather_news",
        model_client=model_client,
        tools=[search_weather_news],
        system_message=SYSTEM_MESSAGE,
        reflect_on_tool_use=True,  # write an answer from the results, not raw output
    )

    try:
        await Console(
            agent.run_stream(task=f"Give me today's weather news for {city} in 3 short lines.")
        )
    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())