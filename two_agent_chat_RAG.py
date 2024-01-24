import autogen
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import chromadb
import time
# Local packages
from prompts import agent_prompts

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
    "cache_seed": 84,
    "config_list": config_list,
    "temperature": 0,
}

retrieve_assistant = RetrieveAssistantAgent(
    name="Retrieve_Assistant",
    system_message=agent_prompts.retrieve_assistant_prompt,
    llm_config=llm_config,
)

# ----------------------- Construct Agents ------------------------ #
rag_user_proxy = RetrieveUserProxyAgent(
    name="RAG_User_Proxy",
    system_message=agent_prompts.rag_user_proxy_prompt,
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    retrieve_config={
        "task": "qa",
        "docs_path": "docs",
        "chunk_token_size": 500,
        "model": config_list[0]["model"],
        "client": chromadb.PersistentClient(path="/tmp/chromadb"),
        "get_or_create": True,
    },
    code_execution_config=False,  # we don't want to execute code in this case.
)


def _reset_agents():
    retrieve_assistant.reset()
    rag_user_proxy.reset()


def basic_rag(question):
    _reset_agents()
    rag_user_proxy.initiate_chat(
        retrieve_assistant,
        problem=question,
        n_results=5,
    )


if __name__ == "__main__":
    QUESTION = input("Enter your question: ")
    st = time.time()
    basic_rag(question=QUESTION)
    et = time.time()
    exec_time = et - st
    print(f'Time : {exec_time:.2f} sec')
