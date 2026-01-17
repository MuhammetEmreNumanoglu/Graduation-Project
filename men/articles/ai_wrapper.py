import os
import requests

class LLMClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or os.getenv("AUTH_API_KEY")

    def generate(
        self,
        history,
        model,
        tools=None,
        provider=None,
        stream=False,
        temperature=1.0,
        max_tokens=1024,
        agent_type="FEEL_GOOD_LIMITED_AGENT",
        max_tool_usage=5,
        output_type=None,
        output_structure=None,
        output_validation=None
    ):
        payload = {
            # ESKİ HALİ (Hatalı):
            # "history": history,
            
            # YENİ ve DOĞRU HALİ (DeepSeek Dokümantasyonuna Göre):
            "messages": history,

            "model": model,
            "tools": tools or [],
            "provider": provider,
            "stream": stream,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "agent_type": agent_type,
            "max_tool_usage": max_tool_usage,
            "output_type": output_type,
            "output_structure": output_structure,
            "output_validation": output_validation
        }

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "X-API-KEY": f"{self.api_key}"
        }

        try:
            response = requests.post(self.base_url, json=payload, headers=headers, stream=stream, timeout=60)
            response.raise_for_status()

            if stream:
                return self._stream_response(response)
            else:
                return response.json()

        except requests.exceptions.RequestException as e:
            return {"status": "error", "error": str(e)}

    def _stream_response(self, response):
        for line in response.iter_lines(decode_unicode=True):
            if line:
                yield line
