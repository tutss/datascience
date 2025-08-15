# %%
# !pip install -qqq datasets transformers trl peft accelerate bitsandbytes --progress-bar off
# !pip install -qqq flash-attn --no-build-isolation --progress-bar off

# %%
import re
import torch
from pprint import pprint
import warnings

warnings.filterwarnings('ignore')

# %%
seed = 42
model_name = "HuggingFaceTB/SmolLM-135M-Instruct"
environment_name = "propositional_logic"
dataset_size = 10

SYSTEM_PROMPT = "---"

torch.manual_seed(seed);

# %% [markdown]
# ## Transformers

# %%
from transformers import AutoModelForCausalLM, AutoTokenizer

# %%
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print(f"Using MPS device: {device}")
else:
    device = torch.device("cpu")
    print(f"Using CPU device: {device}")

print("Loading model...")
lm = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# %%
lm = lm.to(device)
print(f"Model moved to {device}")

# Set padding token for tokenizer
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# %%
inputs = tokenizer("Hello world!", return_tensors='pt').to(device)
inputs

# %%
outputs = lm.generate(**inputs, max_new_tokens=50)
outputs

# %%
input_length = inputs.input_ids.shape[1]
print(tokenizer.batch_decode(outputs[:, input_length:])[0])

# %% [markdown]
# ## Reasoning Gym

# %%
from reasoning_gym import create_dataset, get_score_answer_fn

# %%
test_dataset = create_dataset(environment_name, seed=seed, size=2)
test_dataset

# %%
test_dataset[0]

# %%
score_fn = get_score_answer_fn(environment_name)
score_fn

# %%
score_fn("(R ∨ Q)", test_dataset[0])

# %%
score_fn("(P ∨ Q)", test_dataset[0])

# %%
score_fn("(P ∨ S)", test_dataset[0])

# %% [markdown]
# ## Dataset and Dataloader

# %%
from datasets import load_dataset, Dataset

# %%
hf_dataset = load_dataset("mlabonne/smoltldr")
hf_dataset

# %%
hf_dataset["train"][0]

# %%
rg_dataset = create_dataset(environment_name, seed=seed, size=dataset_size)
split = int(len(rg_dataset) * .8)
split
    

# %%
rg_dataset[0]

# %%
train = []
val = []
for i, x in enumerate(rg_dataset):
    if i < split:
        train.append(x)
    else:
        val.append(x)

# %%
train_data = {
    'prompt': [item['question'] for item in train],
    'answer': [item['answer'] for item in train],
    'metadata': [item['metadata'] for item in train]
}

val_data = {
    'prompt': [item['question'] for item in val],
    'answer': [item['answer'] for item in val],
    'metadata': [item['metadata'] for item in val]
}

train_data['prompt'][0]

# %%
dataset = Dataset.from_dict(train_data)
dataset

# %% [markdown]
# ## Fine-tune

# %%
from peft import LoraConfig, get_peft_model
from trl import GRPOConfig, GRPOTrainer

# %%
# Load LoRA
print("Setting up LoRA configuration...")
lora_config = LoraConfig(
    task_type="CAUSAL_LM",
    r=16,
    lora_alpha=32,
    target_modules="all-linear",
)
model = get_peft_model(lm, lora_config)
print("LoRA model created")
print(model.print_trainable_parameters())

# %%
def score_propositional_answer(prompts, completions, **kwargs):
    return score_fn(completions, prompts)


score_propositional_answer(test_dataset[0], "(P ∨ Q)")

# %%
training_args = GRPOConfig(
    output_dir="GRPO",
    learning_rate=2e-5,
    max_completion_length=96,
    optim="adamw_torch",  # Use torch optimizer instead of 8bit
    num_train_epochs=1,
    bf16=True,
    remove_unused_columns=False,
    logging_steps=1,
    dataloader_pin_memory=False,  # Disable pin memory for MPS
)

# %%
print("Creating GRPO trainer...")
trainer = GRPOTrainer(
    model=model,
    reward_funcs=[score_propositional_answer],
    args=training_args,
    train_dataset=dataset,
)
print("Trainer created successfully")

# %%
print("Starting training...")
trainer.train()
print("Training completed!")

# %%



