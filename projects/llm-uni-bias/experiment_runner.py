"""
Main experiment runner for LLM University Bias study
"""

import json
import logging
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from config import *
from claude_client import ClaudeClient
from openai_client import OpenAIClient
from response_parser import ResponseParser

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ExperimentRunner:
    def __init__(self, output_dir: str = "results"):
        """
        Initialize experiment runner
        
        Args:
            output_dir: Directory to save results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.claude_client = None
        self.openai_client = None
        
        # Initialize clients if API keys are available
        try:
            self.claude_client = ClaudeClient()
            logger.info("Claude client initialized successfully")
        except ValueError as e:
            logger.warning(f"Claude client initialization failed: {e}")
        
        try:
            self.openai_client = OpenAIClient()
            logger.info("OpenAI client initialized successfully")
        except ValueError as e:
            logger.warning(f"OpenAI client initialization failed: {e}")
        
        if not self.claude_client and not self.openai_client:
            raise ValueError("At least one API client must be available. Please set ANTHROPIC_API_KEY or OPENAI_API_KEY environment variables.")
    
    def generate_prompt(self, university: str, question: str) -> str:
        """
        Generate prompt for a specific university and question
        
        Args:
            university: Name of the university
            question: Bias question to ask
        
        Returns:
            Formatted prompt
        """
        return BASE_PROMPT_TEMPLATE.format(university=university, question=question)
    
    def run_single_experiment(self, model_name: str, university: str, question: str) -> Dict:
        """
        Run a single experiment for one model, university, and question combination
        
        Args:
            model_name: Name of the model ("claude" or "gpt")
            university: University name
            question: Question to ask
        
        Returns:
            Dictionary with experiment results
        """
        prompt = self.generate_prompt(university, question)
        
        try:
            if model_name.lower() == "claude" and self.claude_client:
                raw_response = self.claude_client.generate_with_retry(
                    prompt, temperature=0, max_tokens=50
                )
            elif model_name.lower() == "gpt" and self.openai_client:
                raw_response = self.openai_client.generate_with_retry(
                    prompt, temperature=0, max_tokens=50, model="gpt-4"
                )
            else:
                raise ValueError(f"Model {model_name} not available or client not initialized")
            
            parsed_answer = ResponseParser.parse_response(raw_response)
            is_valid = ResponseParser.validate_answer(parsed_answer)
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "model": model_name,
                "university": university,
                "question": question,
                "prompt": prompt,
                "raw_response": raw_response,
                "parsed_answer": parsed_answer,
                "is_valid": is_valid
            }
            
            logger.info(f"{model_name} | {university[:20]}... | {question[:30]}... | Answer: {parsed_answer}")
            return result
            
        except Exception as e:
            logger.error(f"Error in experiment: {model_name} | {university} | {question[:30]}... | Error: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "model": model_name,
                "university": university,
                "question": question,
                "prompt": prompt,
                "raw_response": None,
                "parsed_answer": None,
                "is_valid": False,
                "error": str(e)
            }
    
    def run_full_experiment(self, models: List[str], universities: List[str], questions: List[str]) -> List[Dict]:
        """
        Run the full experiment across all combinations
        
        Args:
            models: List of models to test
            universities: List of universities to test
            questions: List of questions to test
        
        Returns:
            List of experiment results
        """
        total_experiments = len(models) * len(universities) * len(questions)
        logger.info(f"Starting experiment with {total_experiments} total combinations:")
        logger.info(f"- Models: {models}")
        logger.info(f"- Universities: {len(universities)}")
        logger.info(f"- Questions: {len(questions)}")
        
        results = []
        completed = 0
        
        for model in models:
            for university in universities:
                for question in questions:
                    result = self.run_single_experiment(model, university, question)
                    results.append(result)
                    completed += 1
                    
                    if completed % 10 == 0:
                        logger.info(f"Progress: {completed}/{total_experiments} ({completed/total_experiments*100:.1f}%)")
        
        logger.info(f"Experiment completed! {completed} experiments finished.")
        return results
    
    def save_results(self, results: List[Dict], filename: Optional[str] = None) -> str:
        """
        Save experiment results to files
        
        Args:
            results: List of experiment results
            filename: Custom filename (without extension)
        
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"llm_bias_experiment_{timestamp}"
        
        # Save as JSON
        json_path = self.output_dir / f"{filename}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Save as CSV
        csv_path = self.output_dir / f"{filename}.csv"
        df = pd.DataFrame(results)
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        logger.info(f"Results saved to:")
        logger.info(f"- JSON: {json_path}")
        logger.info(f"- CSV: {csv_path}")
        
        return str(json_path)
    
    def analyze_results(self, results: List[Dict]) -> Dict:
        """
        Basic analysis of experiment results
        
        Args:
            results: List of experiment results
        
        Returns:
            Analysis summary
        """
        df = pd.DataFrame(results)
        
        analysis = {
            "total_experiments": len(results),
            "valid_responses": len(df[df["is_valid"] == True]),
            "invalid_responses": len(df[df["is_valid"] == False]),
            "response_rate": len(df[df["is_valid"] == True]) / len(results) * 100
        }
        
        if "model" in df.columns:
            analysis["model_breakdown"] = df["model"].value_counts().to_dict()
        
        if "parsed_answer" in df.columns:
            valid_df = df[df["is_valid"] == True]
            if len(valid_df) > 0:
                analysis["answer_distribution"] = valid_df["parsed_answer"].value_counts().to_dict()
        
        return analysis

def main():
    """Main function to run the experiment"""
    runner = ExperimentRunner()
    
    test_universities = UNIVERSITIES
    test_questions = [
        *SOCIAL_JUSTICE,
        *TECH_AND_SOCIETY,
        *HEALTHCARE,
        *EDUCATION,
        *IMMIGRATION,
    ]
    
    logger.info("Running test experiment...")
    test_results = runner.run_full_experiment(
        models=['claude', 'gpt'],
        universities=test_universities,
        questions=test_questions
    )

    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    today_w_time = now.strftime('%H:%M')
    
    # Save test results
    test_file = runner.save_results(test_results, f"{today}/test_experiment_{today_w_time}")
    
    # Analyze test results
    test_analysis = runner.analyze_results(test_results)
    logger.info(f"Test Analysis: {test_analysis}")

if __name__ == "__main__":
    main()