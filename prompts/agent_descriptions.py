"""
This file containts descriptions for various agents.
These descriptions help GroupChat choosing which agents should speak next.
"""

rag_user_proxy_desc = """Manager_Assistant with additional content retrieved
from provided documents."""

answer_generator_desc = """Answer_Generator capable of producing concise and accurate answer
to the question based on the retrieved contents.
Reply `TERMINATE` in the end when everything is done."""

answer_evaluator_desc = """Answer_Evaluator assesses the conciseness and accuracy of answer
based on the user's given question. Ideal answer should be short and accurate.
Reply `TERMINATE` in the end when everything is done."""
