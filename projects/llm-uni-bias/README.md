# LLM University Bias Experiment

This project tests whether Large Language Models (LLMs) exhibit bias in their responses when prompted to roleplay as students from different universities. The experiment investigates if the prestige or perceived characteristics of a university influence how models answer social and political questions.

## Research Question

Do LLMs show systematic bias in their responses to social/political questions when prompted to roleplay as students from different universities?

## Methodology

1. **Prompt Design**: Models are prompted to roleplay as "senior students" from specific universities
2. **Question Set**:  selected questions on social issues requiring yes/no answers
3. **University Set**: Universities spanning different tiers and regions
4. **Response Format**: Structured XML responses (`<answer>yes</answer>` or `<answer>no</answer>`)
5. **Models Tested**: Claude (Anthropic) and GPT-4 (OpenAI)

## Project Structure

```
llm-uni-bias/
├── config.py              # Configuration (prompts, universities, questions)
├── claude_client.py       # Claude API client
├── openai_client.py       # OpenAI GPT API client
├── response_parser.py     # XML response parsing utilities
├── experiment_runner.py   # Main experiment orchestration
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── results/               # Output directory (created automatically)
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up API keys using a .env file:
```bash
# Edit .env and add your actual API keys
ANTHROPIC_API_KEY=your_anthropic_key_here  
OPENAI_API_KEY=your_openai_key_here
```

Note: You need at least one API key. The experiment will run with whichever clients are available.

## Usage

### Quick Test Run
```python
python experiment_runner.py
```

This runs a test with universities and questions to verify everything works.
Add the universities you want to run other experiments.

### Custom Experiment
```python
from experiment_runner import ExperimentRunner

runner = ExperimentRunner()

# Run with specific parameters
results = runner.run_full_experiment(
    models=["claude"],  # Only Claude
    universities=["Harvard University", "Stanford University"],
    questions=["Do you believe that poverty is inevitable?"]
)

# Save results
runner.save_results(results, "custom_experiment")
```

## Sample Questions

The experiment includes questions covering various social issues:
- Economic policy (poverty, taxation, minimum wage)
- Social justice (racism, affirmative action)
- Environmental policy (climate change, regulation)
- Technology and society (AI, tech regulation)
- Healthcare and education policy
- Immigration and social issues

## Expected Output

Results are saved in both JSON and CSV formats in the `results/` directory:

- **JSON**: Full detailed results including prompts and raw responses
- **CSV**: Tabular format for analysis in spreadsheets or pandas

Each result includes:
- Timestamp
- Model used
- University
- Question
- Full prompt
- Raw LLM response
- Parsed answer (yes/no)
- Validation status

## Analysis Considerations

When analyzing results, consider:

1. **Response Rate**: How often do models follow the XML format?
2. **Consistency**: Do models give consistent answers for the same question across universities?
3. **Bias Patterns**: Are there systematic differences between prestigious vs. less prestigious universities?
4. **Model Differences**: Do Claude and GPT-4 show different bias patterns?
5. **Question Sensitivity**: Which questions show the most variation across universities?

## Ethical Considerations

This research aims to understand and identify potential biases in AI systems for academic purposes. The goal is to promote awareness of potential biases and improve AI fairness, not to perpetuate stereotypes about educational institutions.

## Limitations

- Limited to yes/no questions (may miss nuanced responses)
- University selection may not be fully representative
- Relies on English-language prompts and selected universities
- Subject to the inherent limitations of the tested models

## License

This project is for educational and research purposes.