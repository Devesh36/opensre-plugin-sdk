"""Bridged tool: twilio_notify (from OpenSRE app.tools.TwilioNotifyTool)."""

from __future__ import annotations

from typing import Any

from twilio_plugin.config import _available, _extract_params
from opensre_plugin.bridge import delegate_to_opensre
from opensre_plugin.decorators import plugin_tool


@plugin_tool(
    name='twilio_notify',
    source='twilio',
    description='Send a short SMS notification via the configured Twilio integration. Only available when a Twilio integration with the SMS channel enabled exists.',
    input_schema={'type': 'object', 'properties': {'to': {'type': 'string', 'description': 'Recipient phone number in E.164 (e.g. +14155551234). Defaults to the channel default_to when omitted.'}, 'body': {'type': 'string', 'description': 'SMS body (truncated to the SMS limit).'}}, 'required': ['body']},
    is_available=_available,
    extract_params=_extract_params,
    injected_params=('account_sid', 'auth_token'),
    requires=['twilio'],
    use_cases=['Paging an on-call recipient with a one-line incident summary via SMS', 'Sending a follow-up SMS when a critical-severity alert escalates'],
)
def twilio_notify(**kwargs: Any) -> dict[str, Any]:
    payload = {**_extract_params({}), **kwargs}
    try:
        return delegate_to_opensre(
            module='app.tools.TwilioNotifyTool',
            attr='twilio_notify',
            kwargs=payload,
        )
    except Exception as exc:
        from opensre_plugin.exceptions import OpensreNotInstalledError

        if isinstance(exc, OpensreNotInstalledError):
            return {"error": str(exc)}
        return {"error": f"twilio_notify failed: {exc}"}
