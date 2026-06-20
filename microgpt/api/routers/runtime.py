from pathlib import Path

from fastapi import APIRouter, Depends

from microgpt.api.auth.security import get_current_user
from microgpt.api.config import get_settings
from microgpt.platform.runtime.factory import get_runtime
from microgpt.platform.runtime.model_registry import ModelRegistry, default_registry
from microgpt.platform.system.specs import collect_system_specs, recommend_model_tier

router = APIRouter(prefix="/runtime", tags=["runtime"])


def _active_model_summary() -> dict:
    settings = get_settings()
    model = ModelRegistry(settings.model_registry_path).get(settings.active_model_id or None)
    if model is None:
        return {"configured": False, "reason": "No active model found in registry"}
    resolved = model.resolved_path(settings.model_dir)
    return {
        "configured": True,
        "model_id": model.model_id,
        "name": model.name,
        "runtime": model.runtime,
        "path": str(resolved),
        "file_exists": resolved.exists(),
        "file_size_mb": round(resolved.stat().st_size / (1024 * 1024), 2) if resolved.exists() else None,
        "quantization": model.quantization,
        "context_length": model.context_length,
        "status": model.status,
    }


@router.get("/status")
def runtime_status(_: dict = Depends(get_current_user)) -> dict:
    settings = get_settings()
    runtime_error = None
    try:
        runtime = get_runtime()
        active_runtime = runtime.runtime_name
        fallback_reason = getattr(runtime, "reason", None)
    except Exception as exc:  # Status should report problems, not crash.
        active_runtime = "unavailable"
        fallback_reason = None
        runtime_error = f"{exc.__class__.__name__}: {exc}"

    return {
        "configured_runtime_mode": settings.runtime_mode,
        "active_runtime": active_runtime,
        "active_model_id": settings.active_model_id or None,
        "model_registry_path": str(settings.model_registry_path),
        "model_registry_exists": Path(settings.model_registry_path).exists(),
        "model_dir": str(settings.model_dir),
        "model_dir_exists": Path(settings.model_dir).exists(),
        "fallback_enabled": settings.runtime_fallback_enabled,
        "fallback_reason": fallback_reason,
        "runtime_error": runtime_error,
        "active_model": _active_model_summary(),
        "llama_settings": {
            "n_ctx": settings.llama_n_ctx,
            "n_threads": settings.llama_n_threads,
            "n_gpu_layers": settings.llama_n_gpu_layers,
            "max_tokens": settings.llama_max_tokens,
            "cli_path": settings.llama_cli_path,
            "cli_timeout_seconds": settings.llama_cli_timeout_seconds,
            "cli_single_turn": settings.llama_cli_single_turn,
            "cli_suppress_prompt": settings.llama_cli_suppress_prompt,
            "cli_show_timings": settings.llama_cli_show_timings,
            "cli_simple_io": settings.llama_cli_simple_io,
            "cli_log_disable": settings.llama_cli_log_disable,
            "reasoning": settings.llama_reasoning,
            "cli_extra_args": settings.llama_cli_extra_args,
        },
    }


@router.get("/models")
def list_models(_: dict = Depends(get_current_user)) -> list[dict]:
    return default_registry().list()


@router.get("/recommendations")
def runtime_recommendations(_: dict = Depends(get_current_user)) -> dict:
    specs = collect_system_specs()
    return {
        "system": specs,
        "recommendation": recommend_model_tier(specs),
    }
