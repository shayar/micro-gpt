from __future__ import annotations

import argparse
import json
import time

from microgpt.platform.microlake.events import event_store
from microgpt.platform.runtime.factory import get_runtime


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark the active MicroGPT runtime.")
    parser.add_argument("--prompt", default="Explain MicroGPT in one short paragraph.")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--max-tokens", type=int, default=128)
    args = parser.parse_args()

    runtime = get_runtime()
    results: list[dict[str, object]] = []
    for run in range(args.runs):
        started = time.perf_counter()
        result = runtime.generate(args.prompt, max_tokens=args.max_tokens)
        elapsed = time.perf_counter() - started
        tokens_per_second = result.tokens_generated / elapsed if elapsed > 0 else 0.0
        row = {
            "run": run + 1,
            "runtime": result.runtime,
            "model_id": result.model_id,
            "fallback_used": result.fallback_used,
            "latency_seconds": round(elapsed, 4),
            "tokens_generated": result.tokens_generated,
            "tokens_per_second": round(tokens_per_second, 4),
        }
        results.append(row)
        print(json.dumps(row, indent=2))

    event_store.append(
        "benchmark_runs",
        {
            "prompt": args.prompt,
            "runs": args.runs,
            "max_tokens": args.max_tokens,
            "results": results,
        },
    )


if __name__ == "__main__":
    main()
