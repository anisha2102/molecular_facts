DECONTEXT_PROMPT = """\
DECONTEXTUALIZATION CRITERIA: Decontextualization adds the right type of information to a CLAIM to make it standalone. \
This process can modify the original CLAIM in the following manners:
- Substituting pronouns or incomplete names with the specific subject being referred to.
- Including contextual information to provide more context about the subject.

Instructions:\
- Identify the "subject" of the claim and locate the claim within the context.
- Use the CONTEXT to substitute any incomplete names or pronouns in the CLAIM.
- If there is no decontextualization necessary, return the original claim as is.
- The decontextualization should minimally modify the claim by only adding necessary contextual information.
- Refer to the following examples to understand the task and output formats.

Example 1:
CONTEXT: Almondbury Community School bullying incident: The clip shows the victim, with his arm in a cast, being dragged to the floor \
by his neck as his attacker says "I'll drown you" on a school playing field, while forcing water from a bottle into the victim's mouth, \
simulating waterboarding. The video was filmed in a lunch break. The clip shows the victim walking away, without reacting, as the attacker \
and others can be heard continuing to verbally abuse him. The victim, a Syrian refugee, had previously suffered a broken wrist; this had also been \
investigated by the police, who had interviewed three youths but took no further action.
CLAIM: The victim had previously suffered a broken wrist.
DECONTEXTUALIZED CLAIM: The Syrian refugee victim in the Almondbury Community School bullying incident had previously suffered a broken wrist.

Example 2:
CONTEXT: Isaiah Stewart: Stewart was born in Rochester, New York. He grew up playing soccer and boxing.
CLAIM: He grew up playing boxing.
DECONTEXTUALIZED CLAIM: Isaiah Stewart grew up playing boxing.

Example 3:
CONTEXT: Arab Serai: According to S.A.A. Naqvi, Mughal emperor Humayun's widow Haji Begum built this "serai" in c. 1560/61 to \
shelter three hundred Arab mullahs whom she was taking with her during her "hajj" to Mecca; however, Y.D. Sharma opines that the \
word Arab in the title is a misnomer as this building was built for the Persian craftsmen and workers who built the Humayun's Tomb. In \
January 2017, the Aga Khan Trust for Culture started a project to conserve the "serai". The restoration was  completed in November 2018. \
In March 2019, the trust announced a planned project to conserve the "baoli" (stepwell) of the serai with the help of funds from the \
embassy of Germany.
CLAIM: The planned project is to conserve the "baoli" (stepwell) of the serai.
DECONTEXTUALIZED CLAIM: The Aga Khan Trust for Culture's planned project in March 2019 is to conserve the "baoli" (stepwell) of the Arab Serai.

Example 4:
CONTEXT: Mason Warren: Warren was born in Doncaster, South Yorkshire and started his career with  Rotherham United, where he progressed from \
the youth team to sign a professional contract in May 2015. He was taken with the first team on the pre-season tour of Scotland and became a \
regular with the development squad before he was sent to NPL Division One South side Sheffield on a two-month youth loan deal. He was a prominent \
figure in the side making six appearances during his loan spell before he was recalled in early January 2016. In February 2016, he was loaned out \
again joining National League North side Harrogate Town on a one-month loan deal. After picking up the Player of the Month award for Harrogate during \
February, his loan was extended until April. He went on to make a total of eleven appearances for Town. Upon his return to Rotherham in April, \
he signed a new two-year contract extension until 2018.
CLAIM: He signed a new two-year contract extension until 2018.
DECONTEXTUALIZED CLAIM: Mason Warren Warren signed a new two-year contract extension until 2018 with Rotherham United.

Example 5:
CONTEXT: Lost Girls (band): Lost Girls is a band that primarily consists of Patrick Fitzgerald and Heidi Berry. They formed in 1998 after \
Fitzgerald left Kitchens of Distinction and Berry left 4AD, which had released three of her albums after her appearance on This Mortal Coil's 1991 \
album "Blood".
CLAIM: 4AD had released three of her albums.
DECONTEXTUALIZED CLAIM: 4AD had released three of Heidi Berry's albums before she left to form Lost Girls.

Example 6:
CONTEXT: Bernard Joseph (politician): He was a member of the Congress of the People before he joined the Economic Freedom Fighters. \
Joseph said that he left the party because he felt that the party lacked leadership and movement. He joined the Economic Freedom Fighters \
to implement the party's policies.
CLAIM: He joined the party to implement the party's policies.
DECONTEXTUALIZED CLAIM: Bernard Joseph joined the Economic Freedom Fighters to implement the party's policies.

Example 7:
CONTEXT: Ham Sandwich (song): On February 20, 2019, the song was self-released as a digital download on international digital stores, as well as \
being released through various music streaming services. The song was released partially as a response to fans who were displeased with Getter's \
album "Visceral", released in late 2018. It was also released shortly before the launch of his "Visceral Tour", based off of his album of the same name.
CLAIM: The album and tour are both named "Visceral".
DECONTEXTUALIZED CLAIM: Getter's album and tour are both named "Visceral".

Similarly, generate a decontextualized claim for the following pair of CLAIM and CONTEXT making minimal alterations to the original structure \
of the CLAIM while ensuring clarity and coherence.

CONTEXT: <context>
CLAIM: <claim>
DECONTEXTUALIZED CLAIM:
"""


SAFE_DECONTEXT_PROMPT = f"""\
Vague references include but are not limited to:
- Pronouns (e.g., "his", "they", "her")
- Unknown entities (e.g., "this event", "the research", "the invention")
- Non-full names (e.g., "Jeff..." or "Bezos..." when referring to Jeff Bezos)


Instructions:
1. The following STATEMENT has been extracted from the broader context of the \
given RESPONSE.
2. Modify the STATEMENT by replacing vague references with the proper entities \
from the RESPONSE that they are referring to.
3. You MUST NOT change any of the factual claims made by the original STATEMENT.
4. You MUST NOT add any additional factual claims to the original STATEMENT. \
For example, given the response "Titanic is a movie starring Leonardo \
DiCaprio," the statement "Titanic is a movie" should not be changed.
5. Before giving your revised statement, think step-by-step and show your \
reasoning. As part of your reasoning, be sure to identify the subjects in the \
STATEMENT and determine whether they are vague references. If they are vague \
references, identify the proper entity that they are referring to and be sure \
to revise this subject in the revised statement.
6. After showing your reasoning, provide the revised statement and wrap it in \
a markdown code block.
7. Your task is to do this for the STATEMENT and RESPONSE under "Your Task". \
Some examples have been provided for you to learn how to do this task.


Example 1:
STATEMENT:
Acorns is a company.

RESPONSE:
Acorns is a financial technology company founded in 2012 by Walter Cruttenden, \
Jeff Cruttenden, and Mark Dru that provides micro-investing services. The \
company is headquartered in Irvine, California.

REVISED STATEMENT:
The subject in the statement "Acorns is a company" is "Acorns". "Acorns" is \
not a pronoun and does not reference an unknown entity. Furthermore, "Acorns" \
is not further specified in the RESPONSE, so we can assume that it is a full \
name. Therefore "Acorns" is not a vague reference. Thus, the revised statement \
is:
```
Acorns is a company.
```


Example 2:
STATEMENT:
He teaches courses on deep learning.

RESPONSE:
After completing his Ph.D., Quoc Le joined Google Brain, where he has been \
working on a variety of deep learning projects. Le is also an adjunct \
professor at the University of Montreal, where he teaches courses on deep \
learning.

REVISED STATEMENT:
The subject in the statement "He teaches course on deep learning" is "he". \
From the RESPONSE, we can see that this statement comes from the sentence "Le \
is also an adjunct professor at the University of Montreal, where he teaches \
courses on deep learning.", meaning that "he" refers to "Le". From the \
RESPONSE, we can also see that "Le" refers to "Quoc Le". Therefore "Le" is a \
non-full name that should be replaced by "Quoc Le." Thus, the revised response \
is:
```
Quoc Le teaches courses on deep learning.
```


Example 3:
STATEMENT:
The television series is called "You're the Worst."

RESPONSE:
Xochitl Gomez began her acting career in theater productions, and she made her \
television debut in 2016 with a guest appearance on the Disney Channel series \
"Raven's Home." She has also appeared in the television series "You're the \
Worst" and "Gentefied."

REVISED STATEMENT:
The subject of the statement "The television series is called "You're the \
Worst."" is "the television series". This is a reference to an unknown entity, \
since it is unclear what television series is "the television series". From \
the RESPONSE, we can see that the STATEMENT is referring to the television \
series that Xochitl Gomez appeared in. Thus, "the television series" is a \
vague reference that should be replaced by "the television series that Xochitl \
Gomez appeared in". Thus, the revised response is:
```
The television series that Xochitl Gomez appeared in is called "You're the \
Worst."
```


Example 4:
STATEMENT:
Dean joined Google.

RESPONSE:
Jeff Dean is a Google Senior Fellow and the head of Google AI, leading \
research and development in artificial intelligence. Dean joined Google in \
1999 and has been essential to its continued development in the field.

REVISED STATEMENT:
The subject of the statement "Dean joined Google" is "Dean". From the \
response, we can see that "Dean" is the last name of "Jeff Dean". Therefore \
"Dean" is a non-full name, making it a vague reference. It should be replaced \
by "Jeff Dean", which is the full name. Thus, the revised response is:
```
Jeff Dean joined Google.
```


Your Task:
STATEMENT:
<claim>

RESPONSE:
<context>
"""
