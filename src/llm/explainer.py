import os
from typing import Optional

try:
    from transformers import pipeline  # type: ignore
except ImportError:  # pragma: no cover - optional
    pipeline = None

from ..config import LLMConfig


class LLMExplainer:
    def __init__(self, cfg: LLMConfig) -> None:
        self.cfg = cfg
        self._client = None
        api_key = os.getenv(cfg.api_key_env)
        if pipeline and api_key:
            # Lightweight default; replace with better local model for edge if desired
            model_name = cfg.model if cfg.provider == "huggingface" else "tiiuae/falcon-7b-instruct"
            self._client = pipeline("text-generation", model=model_name, device_map="auto", model_kwargs={"trust_remote_code": True})
        else:
            if not api_key:
                print("LLM API key missing; using stub explanations.")
            if not pipeline:
                print("Transformers not installed; LLM layer will emit stubs.")

    def explain(self, sign_label: str, confidence: float) -> str:
        prompt = (
            "You are a concise driving safety assistant for Indian roads. "
            f"Explain the sign '{sign_label}' with confidence {confidence:.2f}, "
            "then provide a short instruction for a cautious human driver."
        )
        if self._client is None:
            return f"Detected sign '{sign_label}'. Drive cautiously and obey posted rules."

        try:
            out = self._client(prompt, max_new_tokens=self.cfg.max_tokens, temperature=self.cfg.temperature)
            if isinstance(out, list) and out:
                return out[0]["generated_text"][-self.cfg.max_tokens :]
        except Exception:
            return f"Detected sign '{sign_label}'. Drive cautiously."
        return "Drive safely."
