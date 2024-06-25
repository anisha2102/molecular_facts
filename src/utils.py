from openai import OpenAI
import ast
from src.prompts.molecular_prompt import MOLECULAR_STAGE1_PROMPT, MOLECULAR_STAGE2_PROMPT


def generate_with_prompt_GPT(prompt, engine='gpt-4-turbo-2024-04-09', openai_key=None, max_tokens=2048):
    assert openai_key is not None

    client = OpenAI(api_key=openai_key)

    res = client.chat.completions.create(model=engine, max_tokens=max_tokens, temperature=0.75,
    messages=[{"role": "user", "content": f"{prompt}"}])
    res = res.choices[0].message.content.strip()
    
    return res, prompt

def ambiguity_check(claim, prompt=MOLECULAR_STAGE1_PROMPT, openai_key=None):
    prompt = prompt.replace("[claim]", claim)
    res, _ = generate_with_prompt_GPT(prompt, openai_key=openai_key)
    explanation, disambig_str = [x.strip() for x in res.split("##RESPONSE##:")]
    disambig_str = disambig_str.replace('\n','').strip()
    disambig_dict = ast.literal_eval(disambig_str)

    if disambig_dict['subject'] is not None:
        subject = disambig_dict['subject']

    return disambig_dict, disambig_str, explanation


def decontextualize_ambiguity(claim, disambig, context, prompt=MOLECULAR_STAGE2_PROMPT, openai_key=None):
    subject = disambig['subject']
    disambig_new = {"subject": subject, "disambiguation_criteria": subject}
    disambig = str(disambig_new)
    context = context.replace('<br>',' ').replace('\n',' ').replace('  ',' ')
    prompt = prompt.replace("[claim]", claim).replace("[disambiguation]", disambig).replace("[context]", context)
    res, _ = generate_with_prompt_GPT(prompt, engine="gpt-4-0125-preview", openai_key=openai_key)
    explanation, disambig_decontext = [x.strip() for x in res.split("##DECONTEXTUALIZED CLAIM##:")]
    return disambig_decontext, res, explanation







