# Molecular Facts: Desiderata for Decontextualization in LLM Fact Verification 

Authors: Anisha Gunjal, Greg Durrett

Please check out our work [here]() 📃

<p align="center">
    <img src="./figs/intro.png" width="360">
</p>

### Description

This work evaluates the impact of context and granularity on the factual verification of atomic claims generated by large language models (LLMs). We introduce a framework termed molecular facts, which are optimized for both completeness and brevity. The molecular facts are characterized by two principal attributes:

1. Decontextuality - The ability of claims to be understood independently of additional contextual information.
2. Minimality - The minimum amount of information required to ensure claims are self-sufficient.

We quantify the impact of decontextualization on minimality, then present a baseline methodology for generating molecular facts automatically, aiming to add the right amount of information.


### Usage
An example of generating molecular fact is provided in demo.ipynb.
```
import os
openai_key = os.environ["OPENAI_API_KEY"]
```

1. Step 1: Check for Ambiguity in a claim
```
from src.utils import ambiguity_check
llm_response = <llm-response> # long form LLM response
claim = <claim> # extracted from LLM response
disambig_dict, _, _ = ambiguity_check(claim, openai_key=openai_key)

```
2. Step 2: Decontextualize to genererate Molecular Fact
```
from src.utils import decontextualize_ambiguity
disambig_decontext, _, _ = decontextualize_ambiguity(claim, disambig_dict, llm_response, openai_key=openai_key)

```



