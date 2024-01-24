"""
This file containts system prompts for various agents.
"""

rag_user_proxy_prompt = """RAG_User_Proxy who has extra content retrieved
from given documents."""

answer_generator_prompt = """Answer_Generator who generates accurate answer based on
retrieved content."""

answer_evaluator_prompt = """Answer_Evaluator who evaluates the question's answer."""

retrieve_assistant_prompt = """Retrieve_Assistant who specializes in retrieving
the most relevant data from given documents."""
