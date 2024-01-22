from langchain import PromptTemplate, LLMChain
from model import init_and_load
from model import init_and_load
from rag import load_data
from langchain.chains import RetrievalQA

llm = init_and_load()
retriever = load_data("/workspace/mistral_deployment/ai_ad_generation/flipkart_products.csv")

def generate_output(llm, retriever, query):
    # llm_chain = LLMChain(llm=llm)
    qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    verbose=True)

    result = qa.run(query)
    return result

out = generate_output(llm,retriever,"give my 5 taglines for iphone 15")
print(out)
# Answer the question below from context below :
# {context}
# {question} [/INST] </s>
# """
# question_p = """Which companies announced their mergers"""
# context_p = """ In a landmark fusion of tech titans, Cybervine and QuantumNet announced their merger today, promising to redefine the digital frontier with their combined innovation powerhouse, now known as CyberQuantum."""


# prompt = PromptTemplate(template=template, input_variables=["question","context"])
# llm_chain = LLMChain(prompt=prompt, llm=llm)
# response = llm_chain.run({"question":question_p,"context":context_p})
# print(response)