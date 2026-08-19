"""Optional provider-neutral HTTP adapter for a candidate speech-to-text service.

The offline evaluation path does not require an external provider. This adapter
is intentionally generic: configure the endpoint and API key for a service that
accepts audio bytes and returns JSON containing a `transcript` field.
"""

from __future__ import annotations

import os
from pathlib import Path

import requests


def transcribe_file(path: str | Path) -> str:
    endpoint = os.getenv("STT_API_URL")
    api_key = os.getenv("STT_API_KEY")
    if not endpoint or not api_key:
        raise RuntimeError("Set STT_API_URL and STT_API_KEY for live transcription.")

    audio_path = Path(path)
    with audio_path.open("rb") as audio:
        response = requests.post(
            endpoint,
            headers={"Authorization": f"Bearer {api_key}"},
            files={"audio": (audio_path.name, audio)},
            timeout=120,
        )
    response.raise_for_status()
    payload = response.json()
    transcript = payload.get("transcript")
    if not isinstance(transcript, str):
        raise ValueError("Candidate STT response must contain a string `transcript` field.")
    return transcript
