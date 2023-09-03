import os
from apikey import apikey

# pip install streamlit langchain openai wikipedia (chromadb) tiktoken


import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

# SimpleSequentialChain provides only the last output so instead of it use SequentialChain only
os.environ['OPENAI_API_KEY'] = apikey


#App framework
st.title('YoutubeGPT')
prompt =st.text_input('Plug in your prompt here')


#prompt templates
title_template = PromptTemplate(
    input_variables = ['topic'],
    template = 'write me a youtube video title about {topic} '
)

#script templates
script_template = PromptTemplate(
    input_variables = ['title','wikipedia_research'],
    template = 'write me a youtube videoscript base on this TITLE : {title} while leveraging this wikipedia research:{wikipedia_research}'

)

#Memory
title_memory = ConversationBufferMemory(input_key ='topic',memory_key = 'chat history')
script_memory = ConversationBufferMemory(input_key ='title',memory_key = 'chat history')


#LLMs

llm = OpenAI(temperature=0.9)
title_chain =LLMChain(llm = llm, prompt = title_template,verbose = True,output_key = 'title',memory = title_memory)
script_chain =LLMChain(llm = llm, prompt = script_template,verbose = True,output_key = 'script',memory = script_memory)

#sequential_chain = SequentialChain(chains = [title_chain, script_chain ],input_variables = 'topic',output_variables = ['title','script'],verbose = True)

wiki = WikipediaAPIWrapper()
#showing ouput to screen
if prompt:
    # response = sequential_chain.run({'topic':prompt})
    title = title_chain.run(prompt)
    wiki_research = wiki.run(prompt)
    script = script_chain.run(title = title,wiki_research= wiki_research)

    st.write(title)
    st.write(script)


    with st.expander('Message History'):
        st.info(title_memory.buffer)

    with st.expander('Message History'):
        st.info(script_memory.buffer)

    with st.expander('Wikipedia Research'):
        st.info(wiki_research)