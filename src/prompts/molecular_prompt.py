MOLECULAR_STAGE1_PROMPT = '''\
AMBIGUITY CRITERIA: Ambiguity manifests in diverse forms, including:
- Similar names denoting distinct entities.
- Varied interpretations stemming from insufficient information.
- Multiple understandings arising from vague or unclear information.

Instructions:
- Identify the main SUBJECT within the claim.
- Determine if the SUBJECT is ambiguous according to the provided AMBIGUITY CRITERIA.
- Utilize your world knowledge to enumerate potential DISAMBIGUATIONS for the identified SUBJECT.
- Specify the TYPE of information employed for disambiguation based on the list of DISAMBIGUATIONS.
- If the SUBJECT does not have ambiguous interpretations, return None
- Provide an explanation of the method used to arrive at the final response.

Format your response as a combination of explanation and a dictionary with the following structure: 
##EXPLANATION##:
<step-by-step-explanations>
##RESPONSE##:
{"subject": <subject>, "disambiguation_criteria": <type>}

Example 1:
##CLAIM##: David Heyman, born in 1961 in England, is the founder of Heyday Films.
##EXPLANATION##:
1. SUBJECT of the claim is "David Heyman"
2. DISAMBIGUATIONS for "David Heyman" based on my world knowledge:
  - David Heyman (born 1961) is an English film producer.
  - David M. Heyman (1891–1984), American financier, health services leader, philanthropist, and art collector
  - David Hayman (disease ecologist), New Zealand-based epizootic epidemiologist and disease ecologist
  - David Hayman (born 1948) is a Scottish film, television, and stage actor and director.
3. BEST DISAMBIGUATION CRITERIA for unique identification of the SUBJECT "David Heyman" is his nationality or occupation.
##RESPONSE##:
{"subject": "David Heyman", "disambiguation_criteria": "Occupation or Nationality"}

Example 2:
##CLAIM##: Ruth Bader Ginsburg served as a Supreme Court justice.
##EXPLANATION##:
1. SUBJECT of the claim is "Ruth Bader Ginsburg". 
2. DISAMBIGUATIONS for "Ruth Bader Ginsburg" based on my world knowledge:
  - Ruth Bader Ginsburg (1933–2020), Associate Justice of the Supreme Court of the United States
3. BEST DISAMBIGUATION CRITERIA for unique identification of the SUBJECT "Ruth Bader Ginsburg" is None as the SUBJECT name refers to a unique individual.
##RESPONSE##:
{"subject": "Ruth Bader Ginsburg", "disambiguation_criteria": None}

Example 3:
##CLAIM##: Charles Osgood, the American television commentator, is best known for hosting CBS News Sunday Morning.
##EXPLANATION##:
1. SUBJECT of the claim is "Charles Osgood"
2. DISAMBIGUATIONS for "Charles Osgood" based on my world knowledge:
  - Charles Osgood (1933–2024) was an American writer and commentator.
  - Charles E. Osgood (1916–1991), American psychologist
  - Charles Osgood (artist) (1809–1890), American painter
  - Charlie Osgood (1926–2014), Major League Baseball pitcher
3. BEST DISAMBIGUATION CRITERIA for unique identification of the SUBJECT "Charles Osgood" is profession or lifespan.
##RESPONSE##:
{"subject": "Charles Osgood", "disambiguation_criteria": "Profession or Lifespan"}

Similarly, disambiguate the following claim by detecting the main SUBJECT and disambiguation information for the SUBJECT using your world knowledge. \
Generate an ##EXPLANATION## followed by dictionary-formatted ##RESPONSE##.
##CLAIM##: [claim]
##EXPLANATION##:'''


MOLECULAR_STAGE2_PROMPT = """\
DECONTEXTUALIZATION CRITERIA: Decontextualization adds the right type of information to a CLAIM to make it standalone \
and contain relevant disambiguating information. This process can modify the original CLAIM in the following manners:
- Substituting pronouns or incomplete names with the specific subject being referred to.
- Incorporating the most important distinguishing details such as location/profession/time period to distinguish the subject from others who might share similar names.
- Should not omit information from the original CLAIM.
- Should only minimally modify the original CLAIM.

Instructions:\
- Use the "subject" and the CONTEXT to substitute any incomplete names or pronouns in the CLAIM.
- If the information suggested in "disambiguation_criteria" is available in the CONTEXT, use it resolve the ambiguity of the SUBJECT by adding clarification phrases about the SUBJECT to the claim.
- If information from disambiguation_criteria is already present in the CLAIM, no disambiguation is necessary.
- If multiple options are available in the disambiguation_criteria, then choose ONE information type that is emphasized in the SUBJECT's introduction in the CONTEXT.

Example 1:
##CLAIM:##: He is best known for hosting CBS News Sunday Morning.
##DISAMBIGUATION GUIDELINE##:  {"subject": "Charles Osgood", "disambiguation_criteria": "Profession or Lifespan"}
##CONTEXT##: Charles Osgood, a renowned American radio and television commentator and writer, was born on January 8, 1933, in the Bronx, \
New York City. He is best known for hosting "CBS News Sunday Morning" for over 22 years and "The Osgood File" radio commentaries for over 40 years. \
Osgood also authored several books, including "The Osgood Files", "See You on the Radio", and "Defending Baltimore Against Enemy Attack". He was born \
to Charles Osgood Wood, III and his wife Jean Crafton, and grew up with five siblings. Osgood graduated from Fordham University in 1954 with a bachelor \
of science degree in economics.
##EXPLANATION##: 
1. The SUBJECT "He" refers to "Charles Osgood".
2. The DISAMBIGUATION GUIDELINE says the SUBJECT is ambiguous and needs information about "Profession or Lifespan" for disambiguation.
3. The CONTEXT provides details about both the profession and birth year of the SUBJECT. Tthe \
introduction of the SUBJECT in the CONTEXT emphasizes the SUBJECT's profession as the primary identifier over birth year. \
Therefore, we select the profession, specifically described as 'television commentator', for \
decontextualization to ensure minimal changes.
##DECONTEXTUALIZED CLAIM##: Charles Osgood, the television commentator, is best known for hosting CBS News Sunday Morning.

Example 2:
##CLAIM:##: She served as a Supreme Court justice.
##DISAMBIGUATION GUIDELINE##: {"subject": "Ruth Bader Ginsburg", "disambiguation_criteria": None}
##CONTEXT##: Ruth Bader Ginsburg (March 15, 1933 – September 18, 2020) was an American lawyer and jurist who became an \
associate justice of the Supreme Court of the United States in 1993. Appointed by President Bill Clinton, she served on the \
Court until her death in 2020 and was celebrated for her advocacy for gender equality and civil liberties.
##EXPLANATION##: 
1. The SUBJECT "She" refers to "Ruth Bader Ginsburg".
2. The DISAMBIGUATION GUIDELINE is empty meaning SUBJECT is unambiguous.
##DECONTEXTUALIZED CLAIM##: Ruth Bader Ginsburg served as a Supreme Court justice.

Example 3:
##CLAIM:##: Heyman is the founder of Heyday Films.
##DISAMBIGUATION GUIDELINE##:  {"subject": "David Heyman", "disambiguation_criteria": "Nationality or Occupation"}
##CONTEXT##: David Heyman is a renowned film producer and founder of Heyday Films, known for producing the entire \
"Harry Potter" film series and collaborating with director Alfonso Cuarón on "Harry Potter and the Prisoner of Azkaban" \
and "Gravity". He was born on July 26, 1961, in London. His family has a background in the film industry, with his parents\
 being a producer and actress. Heyman studied Art History at Harvard University and began his career in the film industry\
  as a production assistant. Throughout his career, he has received numerous awards and nominations, including an Academy \
  Award nomination for Best Picture and a BAFTA Award for Best British Film.
##EXPLANATION##: 
1. The SUBJECT "Heyman" refers to "David Heyman".
2. The DISAMBIGUATION GUIDELINE says the SUBJECT is ambiguous and needs information about "Nationality or Occupation" for disambiguation.
3. The CONTEXT provides details about both City of Birth and Occupation as per the DISAMBIGUATION GUIDELINE. \
The introduction of the SUBJECT in the CONTEXT specifically emphasizes the SUBJECT's Occupation over Nationality, \
describing him as a 'film producer'. Therefore, we select Occupation for decontextualization to ensure minimal changes.
##DECONTEXTUALIZED CLAIM##: David Heyman, the film producer, is the founder of Heyday Films.

Now generate an EXPLANATION and DECONTEXTUALIZED CLAIM for the following. Ensure the DECONTEXTUALIZED \
CLAIM adds minimal information to resolve ambiguity, such as adjusting pronouns or including clarifying details \
about the SUBJECT. The DECONTEXTUALIZED CLAIM should be coherent and must avoid repetition. \
It should retain the same structural format as the original CLAIM."

##CLAIM:##: [claim]
##DISAMBIGUATION GUIDELINE##:[disambiguation]
##CONTEXT##: [context]
##EXPLANATION##:
"""
