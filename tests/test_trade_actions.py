from frontend.thinking.trades.trade_actions import (
    build_trade_api_error_message,
    is_valid_values,
    resolve_trade_action_mode,
    validate_token,
)


class MockResponse:
    def __init__(self, body=None, text=""):
        self._body = body
        self.text = text

    def json(self):
        if self._body is None:
            raise ValueError()
        return self._body


def test_resolve_trade_action_mode_poe1_default():
    assert resolve_trade_action_mode({"token": "abc"}) == "poe1_whisper"


def test_resolve_trade_action_mode_poe2_with_hideout_token():
    assert resolve_trade_action_mode({"hideout_token": "abc"}) == "poe2_travel_to_hideout"


def test_validate_token_rejects_empty_and_non_string():
    assert validate_token(123) is None
    assert validate_token(" ") is None
    assert validate_token(" token ") == "token"


def test_is_valid_values_requires_positive_numbers():
    assert is_valid_values([1, 2]) is True
    assert is_valid_values([]) is False
    assert is_valid_values([0]) is False
    assert is_valid_values(["1"]) is False


def test_build_trade_api_error_message_prefers_nested_message():
    response = MockResponse(body={"error": {"message": "token expired"}})
    assert build_trade_api_error_message(response, "fallback") == "token expired"


def test_build_trade_api_error_message_falls_back_to_text():
    response = MockResponse(body=None, text="plain error")
    assert build_trade_api_error_message(response, "fallback") == "plain error"
