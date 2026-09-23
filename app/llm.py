import os
import json
import time

from google import genai


API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY was not found in environment variables."
    )

client = genai.Client(
    api_key=API_KEY
)

PRIMARY_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)

FAST_MODEL = PRIMARY_MODEL

FALLBACK_MODELS = [
    PRIMARY_MODEL,
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
]


def generate_with_fallback(
    prompt: str,
    preferred_model: str = PRIMARY_MODEL,
    max_retries_per_model: int = 2,
):
    models_to_try = [
        preferred_model,
        *FALLBACK_MODELS,
    ]

    # Remove duplicate model names
    models_to_try = list(
        dict.fromkeys(models_to_try)
    )

    last_error = None

    for model_name in models_to_try:

        for attempt in range(
            max_retries_per_model
        ):
            try:
                print(
                    f"Gemini model: {model_name} "
                    f"attempt {attempt + 1}/"
                    f"{max_retries_per_model}"
                )

                response = (
                    client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )
                )

                return response

            except Exception as exc:

                last_error = exc
                error_text = str(
                    exc
                ).lower()

                temporary_error = (
                    "503" in error_text
                    or "unavailable"
                    in error_text
                    or "high demand"
                    in error_text
                    or "429"
                    in error_text
                    or "resource_exhausted"
                    in error_text
                )

                if temporary_error:

                    if (
                        attempt
                        < max_retries_per_model - 1
                    ):
                        wait_time = (
                            5 * (attempt + 1)
                        )

                        print(
                            "Temporary Gemini error. "
                            f"Waiting {wait_time}s..."
                        )

                        time.sleep(
                            wait_time
                        )

                        continue

                    print(
                        f"⚠️ {model_name} unavailable. "
                        "Trying fallback model..."
                    )

                    break

                raise

    raise RuntimeError(
        "All Gemini models failed. "
        f"Last error: {last_error}"
    )


def clean_json_response(
    text: str
):
    clean_text = text.strip()

    if clean_text.startswith(
        "```json"
    ):
        clean_text = clean_text[7:]

    elif clean_text.startswith(
        "```"
    ):
        clean_text = clean_text[3:]

    if clean_text.endswith(
        "```"
    ):
        clean_text = clean_text[:-3]

    return json.loads(
        clean_text.strip()
    )
