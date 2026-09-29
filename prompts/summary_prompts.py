SHORT_SUMMARY_PROMPT = """
You are an AI study assistant.

Create a short student-friendly summary of the supplied study material.

STRICT RULES:
1. Use only the supplied study material.
2. Do not invent facts.
3. Keep important technical terminology.
4. Focus on concepts useful for exams.
5. Use simple language.
6. Write approximately 100-150 words.
7. Do not mention information that is absent from the material.

STUDY MATERIAL:
{context}
"""


DETAILED_SUMMARY_PROMPT = """
You are an AI study assistant helping a college student prepare for exams.

Create a detailed exam-oriented summary using ONLY the supplied study material.

Include, when present:
- Important concepts
- Definitions
- Key points
- Important examples
- Formulas
- Processes
- Comparisons
- Exam-relevant facts

Use:
- Clear headings
- Bullet points
- Simple explanations
- Technical terminology where necessary

Do NOT invent information.

If something is not present in the material, do not add it.

STUDY MATERIAL:
{context}
"""


MCQ_PROMPT = """
You are an AI study assistant.

Generate {count} multiple-choice questions from the supplied study material.

Rules:
- Use only the supplied material.
- Do not invent facts.
- Each question must have four options.
- Mark the correct answer.
- Add a short explanation.
- Keep questions suitable for college exam preparation.
- Mix conceptual and factual questions.

STUDY MATERIAL:
{context}
"""


FLASHCARD_PROMPT = """
Create useful study flashcards from the supplied study material.

Rules:
- Use only the material.
- Do not hallucinate.
- Focus on definitions, concepts, formulas and important facts.
- Use concise question-answer format.

STUDY MATERIAL:
{context}
"""


EXAM_QUESTIONS_PROMPT = """
You are preparing a student for an examination.

Generate important exam questions from the supplied material.

Organize them into:
1. Very Short Questions
2. Short Questions
3. Long Questions

Use only information present in the material.

STUDY MATERIAL:
{context}
"""