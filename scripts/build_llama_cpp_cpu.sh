#!/usr/bin/env bash
set -euo pipefail

# Optional local build path when Docker image is not preferred.
# Requires: git, cmake, C++ compiler.

if [ ! -d llama.cpp ]; then
  git clone https://github.com/ggml-org/llama.cpp.git
fi
cd llama.cpp
cmake -B build -DGGML_NATIVE=ON -DLLAMA_BUILD_SERVER=ON
cmake --build build --config Release -j "$(nproc 2>/dev/null || sysctl -n hw.ncpu)"

echo "Built llama.cpp. Run: ./build/bin/llama-server -m ../models/model.gguf --host 0.0.0.0 --port 8080"
