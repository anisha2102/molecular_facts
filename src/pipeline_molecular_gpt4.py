import os
import json
import ast
import copy
import random
random.seed(29)
from openai import OpenAI
import pandas as pd
from prompts.molecular_prompt import MOLECULAR_STAGE1_PROMPT, MOLECULAR_STAGE2_PROMPT


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

global_disambig_dict = {}

def generate_with_prompt_GPT(prompt, engine='gpt-4-turbo-2024-04-09', max_tokens=2048):

    res = client.chat.completions.create(model=engine, max_tokens=max_tokens, temperature=0.75,
    messages=[{"role": "user", "content": f"{prompt}"}])
    res = res.choices[0].message.content.strip()
    
    return res, prompt

def decontextualize_ambiguity(claim, disambig, context):
    subject = disambig['subject']
    if subject not in global_disambig_dict:
        global_disambig_dict[subject] = None 

    disambig_new = {"subject": subject, "disambiguation_criteria":global_disambig_dict[subject]}
    disambig = str(disambig_new)
    prompt = MOLECULAR_STAGE2_PROMPT
    context = context.replace('<br>',' ').replace('\n',' ').replace('  ',' ')
    prompt = prompt.replace("[claim]", claim).replace("[disambiguation]", disambig).replace("[context]", context)
    res, _ = generate_with_prompt_GPT(prompt, engine="gpt-4-0125-preview")
    try:
        explanation, disambig_decontext = [x.strip() for x in res.split("##DECONTEXTUALIZED CLAIM##:")]
    except:
        import ipdb;ipdb.set_trace()
    return res, explanation, disambig_decontext


def ambiguity_check(claim, prompt=MOLECULAR_STAGE1_PROMPT):
    prompt = prompt.replace("[claim]", claim)

    res, _ = generate_with_prompt_GPT(prompt)
    try:
        explanation, disambig_str = [x.strip() for x in res.split("##RESPONSE##:")]
        disambig_str = disambig_str.replace('\n','').strip()
        disambig_dict = ast.literal_eval(disambig_str)
    except:
        print("Error in literal eval")

        import ipdb;ipdb.set_trace()
    if disambig_dict['subject'] is not None:
        subject = disambig_dict['subject']
        if subject not in global_disambig_dict:
            global_disambig_dict[subject] = None
        if disambig_dict['disambiguation_criteria']!='None' and disambig_dict['disambiguation_criteria'] is not None: 
            global_disambig_dict[subject] = disambig_dict['disambiguation_criteria']

    print("\n\nSTAGE 1\n")
    print(res)
    return disambig_str, explanation, disambig_dict


if __name__ == '__main__':

    gen = [json.loads(x) for x in open("./gen_gpt4/gpt4_simple_decontext_800_supunsup_decontext+safe_multiple_entities.jsonl")]

    filename = "./gen_gpt4/molecular_pipeline_generation.jsonl" #GPT4 for safe and decontext
    fp = open(filename, 'w')

    selected_facts = pd.read_csv("./gen_gpt4/benchmark_facts_supunsup_800.csv") #supported and unsupported
    selected_facts = list(selected_facts[selected_facts.columns[0]])

    count, total, fact_count = 0, 0, 0
    for i, elem in enumerate(gen):

        context = elem['llm_gen']
        topic = elem['topic']

        docs_set = set([x-1 for x in elem['supporting_docs']])
        doc_set = list(set(elem['supporting_docs']))
        total+=1
        if "molecular_gpt4" not in elem:
            elem["molecular_gpt4"] = {}
        count+=1
        idx = 0
        for fact in elem['decontext_gpt4'].keys(): #for safe
            if fact not in selected_facts:
                continue

            fact_count+=1
            decontext = elem['decontext_gpt4'][fact] 
            disambig_str, explanation_disambig, disambig_dict = ambiguity_check(decontext)
            decontext_raw, explanation, disambig_decontext = decontextualize_ambiguity(fact, disambig_dict, context)
            elem["molecular_gpt4"][fact] = disambig_decontext        
        fp.write(json.dumps(elem)+'\n')


