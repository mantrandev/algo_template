import anthropic
import os
import sys
import threading
import time
from pathlib import Path
from collections.abc import Generator

TPS_FILE = Path("/tmp/llm_tps.txt")
_PERSIST_SECONDS = 30

_client: anthropic.Anthropic | None = None


def _client_instance() -> anthropic.Anthropic:
    global _client
    if _client is None:
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            sys.exit("Error: ANTHROPIC_API_KEY is not set")
        _client = anthropic.Anthropic(api_key=key)
    return _client


def _persist(label: str, seconds: int) -> None:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        TPS_FILE.write_text(label)
        time.sleep(1)
    TPS_FILE.unlink(missing_ok=True)


def stream(
    messages: list[dict],
    model: str = "claude-sonnet-4-6",
    max_tokens: int = 1024,
    **kwargs,
) -> Generator[str, None, None]:
    stream_start: float | None = None
    estimated_tokens = 0.0

    with _client_instance().messages.stream(
        model=model,
        max_tokens=max_tokens,
        messages=messages,
        **kwargs,
    ) as s:
        for text in s.text_stream:
            if stream_start is None:
                stream_start = time.perf_counter()
            estimated_tokens += len(text) / 4
            elapsed = time.perf_counter() - stream_start
            tps = estimated_tokens / elapsed if elapsed > 0 else 0
            TPS_FILE.write_text(f"{tps:.1f} t/s (~{int(estimated_tokens)} tok)")
            yield text

        msg = s.get_final_message()
        output_tokens = msg.usage.output_tokens
        elapsed = time.perf_counter() - (stream_start or time.perf_counter())
        final_label = f"{output_tokens / elapsed:.1f} t/s ({output_tokens} tok)"
        TPS_FILE.write_text(final_label)

    threading.Thread(target=_persist, args=(final_label, _PERSIST_SECONDS), daemon=False).start()
    return final_label


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) or "Say hello in 3 sentences."
    print(f"\nPrompt: {prompt}\n")

    for chunk in stream([{"role": "user", "content": prompt}]):
        print(chunk, end="", flush=True)

    print(f"\n\n⚡ {TPS_FILE.read_text()}")
