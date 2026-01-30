import os
from langchain.chains import LLMChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from flask_caching import Cache

from src.constants import N_RESULTS


cache = Cache() 
import time
from langchain_community.chat_message_histories import ChatMessageHistory
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = ""

class OpenAIModelPromptTemplate():
    def __init__(self, clientdb) -> None:
        self.clientdb = clientdb
        self.template ="""You are a Chat customer support agent.
        Pay attention to not getting information outside the context. 
        \
        The following context:
        {context}
        -----------------------------
        \
        This is the current conversation:
        {chat_history}
        Human: {human_input}\
        \
       
        Answer: """


        self.model="gpt-4o-mini"
        self.client = OpenAI(
    api_key=os.environ.get(""),
)
        
    
   
    def get_answer(self, prompt: str, token, collection_name: str):
        query_reuslt = self.clientdb.query_collection(prompt=prompt, n_results=N_RESULTS, collection_name=collection_name)
        docs = query_reuslt["documents"]
        # transform list of lists to string
        docs_str = ".".join(".".join(sublist) if isinstance(sublist, list) else sublist for sublist in docs)

        # if cache.get(token) == None:
        #     chat_memory = []
        #     print("memory ", chat_memory)p
        #     cache.set(token, chat_memory, timeout=500)
        
        # chat_memory = cache.get(token)

        # Slice the chat_memory to include only the latest 2 messages
        # recent_messages = chat_memory[-2:] if len(chat_memory) > 2 else chat_memory

        # formatted_history = "\n".join(
        # f"{'human' if entry['role'] == 'user' else 'ai'}: {entry['content']}" for entry in recent_messages
        # )


        
        formatted_template = self.template.format(
            context=docs_str,
            chat_history="",
            human_input=prompt
        )

        chat_completion = self.client.chat.completions.create(
                messages =[{
                    "role": "assistant",
                    "content": formatted_template,
                }],
                model="gpt-4o",
                temperature=1.2
            )
        
        message_content = chat_completion.choices[0].message.content

        # Add the current user input to chat memory
        # chat_memory.append({
        #     "role": "user",
        #     "content": prompt,
        # })

        # # Append the assistant's response to chat memory
        # chat_memory.append({
        #     "role": "assistant",
        #     "content": message_content
        # })

        # cache.set(token, chat_memory, timeout=500)

        return message_content
       
   