import logging

from groq import Groq

logger = logging.getLogger(__name__)

MODEL_NAME = "llama-3.3-70b-versatile"


def get_ai_recommendation(user_interest, coupons, api_key):
    # AI tips are a bonus feature - if the key is missing or Groq errors
    # out, fall back to None so the rest of the page still renders.
    if not api_key:
        logger.warning("GROQ_API_KEY is not set; skipping AI recommendation")
        return None

    try:
        client = Groq(api_key=api_key)
        coupon_list = "\n".join(
            f"- {c['store']}: {c['title']} (code: {c['code']}, expires: {c['expires']})"
            for c in coupons
        )
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{
                "role": "user",
                "content": (
                    f'A user is looking for: "{user_interest}"\n'
                    f"Here are available coupons:\n{coupon_list}\n"
                    "Recommend the top 2-3 most relevant coupons and explain in 1 "
                    "sentence why each is a good match. Mention the expiry date. "
                    "Be friendly and helpful. Keep it short."
                ),
            }],
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception:
        logger.exception("Groq AI recommendation request failed")
        return None
