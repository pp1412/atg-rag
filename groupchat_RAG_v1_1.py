"""
This script performs RAG via multi-agent groupchat.
There are 3 agents employed in this script:
1. Manager_Assistant
2. Answer_Generator
3. Answer_Evaluator
"""

import autogen
from autogen import AssistantAgent
from autogen.agentchat.groupchat import GroupChat, GroupChatManager
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import chromadb
import time

# Local packages
from prompts import agent_prompts, agent_descriptions

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    file_location=".",
    filter_dict={
        "model": ["mistral"],
    },
)

print("LLM models: ", [config_list[i]["model"] for i in range(len(config_list))])

llm_config = {
    # "timeout": 60,
    "cache_seed": 42,
    "config_list": config_list,
    "temperature": 0,
}


def termination_msg(x):
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()


# ----------------------- Construct Agents ------------------------ #
rag_user_proxy = RetrieveUserProxyAgent(
    name="RAG_User_Proxy",
    is_termination_msg=termination_msg,
    system_message=agent_prompts.rag_user_proxy_prompt,
    description=agent_descriptions.rag_user_proxy_desc,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    retrieve_config={
        "task": "qa",
        "docs_path": "docs",
        "chunk_token_size": 500,
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path="/tmp/chromadb"),
        "collection_name": "groupchat",
        "get_or_create": True,
    },
    code_execution_config=False,  # we don't want to execute code in this case.
)

answer_generator = AssistantAgent(
    name="Answer_Generator",
    is_termination_msg=termination_msg,
    system_message=agent_prompts.answer_generator_prompt,
    description=agent_descriptions.answer_generator_desc,
    llm_config=llm_config,
    code_execution_config=False,
)

answer_evaluator = AssistantAgent(
    name="Answer_Evaluator",
    is_termination_msg=termination_msg,
    system_message=agent_prompts.answer_evaluator_prompt,
    description=agent_descriptions.answer_evaluator_desc,
    llm_config=llm_config,
    code_execution_config=False,
)


def _reset_agents():
    rag_user_proxy.reset()
    answer_generator.reset()
    answer_evaluator.reset()


def rag_chat(query):
    _reset_agents()
    groupchat = GroupChat(
        agents=[rag_user_proxy, answer_generator, answer_evaluator],
        messages=[],
        max_round=12,
        speaker_selection_method="auto",
    )
    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config,
    )

    # Start chatting with the RetrieveUserProxyAgent.
    rag_user_proxy.initiate_chat(
        manager,
        problem=query,
        n_results=8,
    )


if __name__ == "__main__":
    QUESTION = input("Enter your question: ")
    st = time.time()
    rag_chat(query=QUESTION)
    et = time.time()
    exec_time = et - st
    print(f'Time : {exec_time:.2f} sec')
