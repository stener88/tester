import streamlit as st
import os
import openai
from langchain.chat_models import ChatOpenAI
from langchain.chains import GraphCypherQAChain
from langchain.graphs import Neo4jGraph
from dotenv import load_dotenv

# Set Variables
load_dotenv()

# Set up the OpenAI API key and Neo4j credentials
openai_api_key = os.getenv("OPENAI_API_KEY")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")

# Set OpenAI API key
openai.api_key = openai_api_key

# Create Neo4jGraph using environment variables
graph = Neo4jGraph(
    url="bolt://localhost:7687",
    username=neo4j_username,
    password=neo4j_password,
)

chain = GraphCypherQAChain.from_llm(
    ChatOpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=75),
    graph=graph,
    verbose=True,
    top_k=1,
)

# Set page configuration
st.set_page_config(
    page_title="ThunderCunt Beta",
    layout="wide",
)


st.markdown(
    "<h2 style='text-align: center;'>ThunderCunt Beta</h2>", unsafe_allow_html=True
)

st.sidebar.markdown(
    """
## How to Use ThunderCunt beta.

1. Enter your question in the input field. The-o

2. Click the "Punt it" button.
3. The answer will be displayed on the screen.


There is current support to answer questions about players statistics, fpl statistics,
season review, player comparison and position comparison. 

Dictionary:
- Value
- Expected points next round
- Expted points this round
- Creativity
- ICT
- ICT rank
- Influence
- Threat
- Creativity
and more...

Made with Langchain, GPT and NEO4j❤️


"""
)


# Create columns for layout
col1, col2, col3 = st.columns([1, 6, 1])

# Use the middle column for the input field and button
with col2:
    question = st.text_input("", value="How has Harry Kane's season been?")
    if st.button("Punt it!"):
        try:
            output = chain.run(question)
            st.write(output)
        except Exception as e:
            st.write(f"An error occurred: {e}")
            st.info(
                "Please try again with a different question or specify name/last name or metric"
            )

# Close the Neo4j driver
graph._driver.close()
