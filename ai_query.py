import os
from dotenv import load_dotenv
import anthropic

from crud import get_cost_summary, get_all_source_summaries, get_total_outage_hours, get_generator_load_estimate

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

tools = [
    {
        "name": "get_cost_summary",
        "description": "Get total cost and usage (kWh, diesel liters, hours run) for energy entries, optionally filtered by source and/or date range.",
        "input_schema": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "enum": ["grid", "generator", "solar"],
                    "description": "Filter by energy source. Omit to include all sources."
                },
                "start_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format. Omit for no start limit."
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format. Omit for no end limit."
                }
            }
        }
    }
]


def ask_energy_question(session, business_id, user_question):
    messages = [{"role": "user", "content": user_question}]

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            tools=tools,
            messages=messages,
        )
    except anthropic.APIError:
        return "Sorry, I couldn't reach the AI service right now. Please try again in a moment."

    if response.stop_reason == "tool_use":
        tool_calls = [block for block in response.content if block.type == "tool_use"]

        tool_results = []
        for tool_call in tool_calls:
            result = get_cost_summary(
                session=session,
                business_id=business_id,
                source=tool_call.input.get("source"),
                start_date=tool_call.input.get("start_date"),
                end_date=tool_call.input.get("end_date"),
            )
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": str(result),
            })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

        try:
            final_response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                tools=tools,
                messages=messages,
            )
        except anthropic.APIError:
            return "Sorry, I couldn't finish processing that question. Please try again."
        return final_response.content[0].text

    return response.content[0].text


def get_recommendation(session, business_id):
    summaries = get_all_source_summaries(session, business_id)
    outage_hours = get_total_outage_hours(session, business_id)
    load_estimate = get_generator_load_estimate(session, business_id)

    generator_load_note = ""
    if load_estimate.get("possible") and load_estimate["load_percentage"] < 50:
        generator_load_note = (
            f"\nEstimated generator load: running at approximately {load_estimate['load_percentage']}% "
            f"of its rated capacity ({load_estimate['estimated_kw']} kW estimated average load against "
            f"{load_estimate['rated_kw']} kW rated real power). Only mention that the generator may be "
            "oversized for its typical load if this specific data point supports it."
        )

    prompt = f"""Here is a small business's energy cost data in Lebanon, broken down by source:

Grid: {summaries['grid']}
Generator: {summaries['generator']}
Solar: {summaries['solar']}
Total grid outage hours logged: {outage_hours}{generator_load_note}

Based on this data, give a short, practical recommendation on how this business could reduce energy costs. Consider shifting usage between sources, but also consider whether battery storage makes sense (using the outage hours and generator cost as a guide), whether a shared generator subscription ("ishtirak") might be cheaper than running their own generator if the generator cost per hour seems high, and whether the generator appears oversized for its typical load if that estimate is provided above. Only mention an idea if the numbers actually support it — don't include generic advice that isn't backed by the data given. Keep it to 3-4 sentences. Respond in plain text only — no Markdown, no bold, no headers, no bullet points."""
    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
    except anthropic.APIError:
        return "Sorry, I couldn't generate a recommendation right now. Please try again in a moment."

    return response.content[0].text