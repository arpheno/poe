def resolve_trade_action_mode(params):
    action = str(params.get("action") or "").lower()
    game = str(params.get("game") or "").lower()
    if action == "travel_to_hideout" or game == "poe2" or "hideout_token" in params:
        return "poe2_travel_to_hideout"
    return "poe1_whisper"


def validate_token(token):
    if not isinstance(token, str):
        return None
    token = token.strip()
    if not token:
        return None
    return token


def is_valid_values(values):
    if not isinstance(values, list):
        return False
    if not values:
        return False
    return all(isinstance(value, (int, float)) and value > 0 for value in values)


def build_trade_api_error_message(response, fallback):
    if response is None:
        return f"Trade request failed before receiving a response: {fallback}"
    try:
        data = response.json()
    except ValueError:
        data = None

    if isinstance(data, dict):
        error = data.get("error")
        if isinstance(error, dict) and error.get("message"):
            return str(error["message"])
        if isinstance(error, str):
            return error

    text = response.text.strip() if response.text else ""
    if text:
        return text[:200]
    return fallback
