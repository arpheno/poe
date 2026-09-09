from contextlib import nullcontext
from unittest.mock import MagicMock, patch

from poe.equipment_tracker.direct_whisperer import DirectWhisperer


@patch("poe.equipment_tracker.direct_whisperer.limit_rate", return_value=nullcontext())
@patch("poe.equipment_tracker.direct_whisperer.requests.post")
def test_direct_whisper_posts_poe1_payload(mock_post, _mock_limit_rate):
    response = MagicMock()
    response.json.return_value = {"ok": True}
    mock_post.return_value = response

    whisperer = DirectWhisperer(cache=MagicMock())
    result = whisperer.direct_whisper("token-1", values=[2])

    assert result == {"ok": True}
    mock_post.assert_called_once()
    assert mock_post.call_args.kwargs["json"] == {"token": "token-1", "values": [2]}
    assert mock_post.call_args.args[0] == whisperer.url


@patch("poe.equipment_tracker.direct_whisperer.limit_rate", return_value=nullcontext())
@patch("poe.equipment_tracker.direct_whisperer.requests.post")
def test_travel_to_hideout_posts_poe2_payload(mock_post, _mock_limit_rate):
    response = MagicMock()
    response.json.return_value = {"ok": True}
    mock_post.return_value = response

    whisperer = DirectWhisperer(cache=MagicMock())
    result = whisperer.travel_to_hideout("hideout-token")

    assert result == {"ok": True}
    mock_post.assert_called_once()
    assert mock_post.call_args.kwargs["json"] == {"token": "hideout-token"}
    assert mock_post.call_args.args[0] == whisperer.poe2_travel_url
