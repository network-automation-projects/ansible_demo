
from typing import Any
import asyncio

def get_person():
    return "Angela", 28, "Florida"

person = get_person()
print (person)

name, age, state = get_person()
print (name, age, state)

#----------------

point = (10, 20, 30)

def draw(x,y,z):
    print (f"Drawing at {x},{y},{z}")

draw(*point)

#----------------

def log(*messages):
    print("Log: ", " → ".join(messages))

log("AI call", "processing", "epoch 7")

#----------------

# So the * unpacks a list into its pieces.
# A ** unpacks a dictionary into key="value" pairs in a 

def describe_person(**info):
    print("Description:")
    print (info)  # the whole dictionary in braces
    print (*info) # just the keys
    #print (**info) --error
    for k, v in info.items():
        print(f"  {k:>12}: {v}")
        


describe_person(name="Bob", age=34, city="Brandon", hobby="AI tinkering")









def print_person(**personalinfo):
    for k,v in personalinfo.items():
        print(f"{k:<15} : {v:>15}")

print_person(name="Jane", pet="cat", age=50)

# if you needed a two word key...
print_person(**{"name": "Jane", "pet type": "cat", "age": 50})   




def train_model(**settings):
    pass

settings = {
    "rate" : 2.5,
    "batch_size" : 3,
    "epochs" : 15,
}

train_model(**settings)  # equivalent of (rate=2.5, batch_size=3, epochs=15)


#---------------

def train_orchestrator(
    model_name,               # required positional
    dataset_path,             # required positional
    *extra_tags,              # 0..N positional tags ("v1.2", "experiment-7", …)
    learning_rate=3e-5,       # optional keyword
    epochs=10,
    **hyperparams             # any other hyperparameters
):
    print(f"Training {model_name} on {dataset_path}")
    print("Tags:", extra_tags)
    print("LR:", learning_rate)
    print("Extra hypers:", hyperparams)

train_orchestrator(
    "Llama-3.1-8B",
    "/data/finance-corpus",
    "finance-tuned", "low-rank",           # → extra_tags
    epochs=5,
    warmup_ratio=0.1,                       #picked up by **hyperparams  
    max_grad_norm=1.0,                      #picked up by **hyperparams
    quantize="4bit"                         #picked up by **hyperparams
)


#-------------

# Typical pattern in an AI orchestrator / agent framework

SYSTEM_PROMPT = "You are a helpful assistant."

def some_provider_client()-> Any:
    pass

async def run_agent(
    user_query: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
    tools: list | None = None,
    **provider_specific_kwargs   # api_key, base_url, timeout, max_tokens, etc.
) -> dict:
    # 1. Prepare messages (very common pattern)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
    ]

    # 2. Merge default + user overrides
    call_kwargs = {
        "model": model,
        "temperature": temperature,
        "messages": messages,
        **provider_specific_kwargs   # ← merge everything!
    }

    if tools:
        call_kwargs["tools"] = tools            # adss to dictionary called call_kwargs with 1 item - key- tools value- the list of tools 
        call_kwargs["tool_choice"] = "auto"     # adds another dictionary item key- tool_choice value - auto

    # 3. Call can go to OpenAI / Anthropic / Groq / Together / local vLLM / etc.
    response = await some_provider_client.chat.completions.create(**call_kwargs)

    return response

result = asyncio.rum( run_agent(
    "Summarize this document",
    model="gpt-4o",
    api_key="sk-...",
    base_url="https://api.openai.com/v1",
))


#---------

# for merging configs

default_config = {
    "max_new_tokens": 2048,
    "do_sample": True,
    "top_p": 0.95,
    "repetition_penalty": 1.05
}

user_overrides = {"temperature": 0.9, "max_new_tokens": 4096}

generation_config = {**default_config, **user_overrides}   # ← clean merge

# here is the other way without packing/unpacking
generation_config = {}
generation_config.update(default_config)
generation_config.update(user_overrides)

#---------------------------


# Unpack and capture rest: head + tail (middle gets the rest)

lst = [10, 20, 30, 40, 50]
first, *middle, last = lst

print(first)   # 10
print(middle)  # [20, 30, 40]
print(last)    # 50


# Just head and rest
head, *rest = [1, 2, 3, 4]       # head=1, rest=[2, 3, 4]

# Just rest and tail
*beg, tail = [1, 2, 3, 4]       # beg=[1, 2, 3], tail=4


#---------------------------
# cheatsheet

# Goal                        Syntax              Result type   Most common context
# ──────────────────────────  ──────────────────  ───────────  ────────────────────────────────
# Collect positional args     def f(*args)         tuple        flexible inputs, logging, forwarding
# Collect keyword args        def f(**kwargs)     dict         config, hyperparams, provider settings
# Unpack list into args       f(*lst)             —            pass params from list
# Unpack dict into kwargs     f(**dct)            —            pass config/hyperparameters
# Merge dictionaries          {**a, **b}          new dict     config + overrides (very common in AI)
# Unpack and capture rest     a, *middle, b = lst list (middle) head + tail patterns