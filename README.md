openai
langchain
streamlit

# Langchain==0.3.13
# langchain-core==0.3.28
# langchain-community==0.3.13
# langchain-openai==0.2.14

# how to run this app
#uvicorn backend:app --reload
#streamlit run app-py
check : curreent directory is: cd

# for creatig environment
conda create -n lang6 python=3.11 -y
conda activate lang6
pip install -r requirements.txt