import anthropic
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
        _client = anthropic.Anthropic()
    return _client


def _write(label: str) -> None:
    TPS_FILE.write_text(label)


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
    _write("...")
    start = time.perf_counter()

    with _client_instance().messages.stream(
        model=model,
        max_tokens=max_tokens,
        messages=messages,
        **kwargs,
    ) as s:
        estimated_tokens = 0.0
        for text in s.text_stream:
            estimated_tokens += len(text) / 4
            elapsed = time.perf_counter() - start
            _write(f"{estimated_tokens / elapsed:.1f} t/s ({int(estimated_tokens)} tok) ...")
            yield text

        msg = s.get_final_message()
        output_tokens = msg.usage.output_tokens
        elapsed = time.perf_counter() - start
        final_label = f"{output_tokens / elapsed:.1f} t/s ({output_tokens} tok)"

    t = threading.Thread(target=_persist, args=(final_label, _PERSIST_SECONDS), daemon=False)
    t.start()


if __name__ == "__main__":
    import sys

    prompt = " ".join(sys.argv[1:]) or "Say hello in 3 sentences."
    print(f"Prompt: {prompt}\n")
    for chunk in stream([{"role": "user", "content": prompt}]):
        print(chunk, end="", flush=True)
    print(f"\n\nSee {TPS_FILE} for final t/s.")
