# sdk/response.py

class LLMResponse:
    """Standard response from any LLM provider."""
    
    def __init__(self, text, model_used, latency=0, success=True, error=None):
        self.text = text
        self.model_used = model_used
        self.latency = latency
        self.success = success
        self.error = error
    
    def __str__(self):
        if self.success:
            return f"LLMResponse(model={self.model_used}, latency={self.latency:.2f}s)"
        return f"LLMResponse(FAILED, error={self.error})"