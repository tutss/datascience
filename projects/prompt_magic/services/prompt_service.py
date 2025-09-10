import os
from typing import Optional
import anthropic


class PromptService:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-3-haiku-20240307"
    
    def _get_prompt_generation_instructions(self) -> str:
        return """You are a prompt engineering expert. Your task is to create high-quality, effective prompts based on user requests.

IMPORTANT RULES:
1. Always structure prompts with: ROLE + GOAL + INSTRUCTIONS + CHAIN OF THOUGHT
2. End every prompt with "Think carefully, step by step"
3. Make prompts clear, specific, and actionable
4. Include relevant context when needed
5. Use professional, direct language

PROMPT STRUCTURE TEMPLATE:
- Role: Define who the AI should act as
- Goal: State the main objective clearly  
- Instructions: Provide specific steps or guidelines
- Chain of thought: Add reasoning requirements
- End phrase: "Think carefully, step by step"

Generate a complete, ready-to-use prompt that accomplishes the user's request."""

    async def generate_prompt(self, user_request: str) -> str:
        system_instructions = self._get_prompt_generation_instructions()
        
        user_message = f"""Create a prompt for this request: "{user_request}"

Remember to include:
- Clear role definition
- Specific goal
- Step-by-step instructions
- Chain of thought reasoning
- End with "Think carefully, step by step"

Return only the generated prompt, nothing else."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                system=system_instructions,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            
            generated_prompt = response.content[0].text.strip()
            
            # TODO(human)
            
            return generated_prompt
            
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")
    
    def validate_prompt_structure(self, prompt: str) -> dict:
        checks = {
            "has_role": any(word in prompt.lower() for word in ["you are", "act as", "role", "assistant"]),
            "has_goal": any(word in prompt.lower() for word in ["goal", "objective", "task", "help"]),
            "has_instructions": len(prompt.split('.')) > 3,
            "has_step_by_step": "step by step" in prompt.lower(),
            "appropriate_length": 50 < len(prompt) < 800
        }
        
        return {
            "valid": all(checks.values()),
            "checks": checks,
            "score": sum(checks.values()) / len(checks)
        }