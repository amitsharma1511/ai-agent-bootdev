import os
import sys
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions.call_functions import available_functions, call_function
from config import MAX_ITERATIONS

def main() -> None:

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    openai_api_key = os.getenv('OPENAI_API_KEY')
    

    if not api_key:
        raise RuntimeError("API Key for OPENROUTER_API_KEY env variable not found or invalid.")

    # client = OpenAI(
    #     base_url="https://openrouter.ai/api/v1",
    #     api_key=api_key
    #     )
    client = OpenAI(api_key=openai_api_key)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    for _ in range(MAX_ITERATIONS):
        try:
            result = generate_content(client, messages, args.verbose)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        if result is not None:
            print("Response:")
            print(result)
            return
    else:
        print(f"Stopped: reached {MAX_ITERATIONS} iterations without a final answer.")
        sys.exit(1)


def generate_content(client: OpenAI, messages: list, verbose: bool) -> str | None:
    # response = client.chat.completions.create(
    #     model="nvidia/nemotron-3-ultra-550b-a55b:free",
    #     messages=messages,
    #     tools=available_functions
    # )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=available_functions
    )

    if not response.usage:
        raise RuntimeError("Usage not available, probably the API request failed")

    if verbose:
        print("Prompt tokens: ",response.usage.prompt_tokens)
        print("Response tokens: ",response.usage.completion_tokens)

    finish_reason = response.choices[0].finish_reason

    message = response.choices[0].message
    messages.append(message)

    if finish_reason in ("length", "content_filter"):
        raise RuntimeError(f"Model stopped early: {finish_reason}")

    if finish_reason != "tool_calls":
        return message.content or ""


    
    tool_call_results = []
    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue
        result = call_function(tool_call, verbose)
        tool_call_results.append(result)
        if not result.get("content"):
            raise RuntimeError(f"Empty function response for {tool_call.function.name}")
        if verbose:
            print(f"-> {result['content']}")

    messages.extend(tool_call_results)

    return None

if __name__ == "__main__":
    main()
