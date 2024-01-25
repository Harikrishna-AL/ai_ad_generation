from langchain import PromptTemplate, LLMChain
from model import init_and_load
from model import init_and_load
from rag import load_data
from langchain.chains import RetrievalQA
from fastapi import FastAPI
from pydantic import BaseModel
from urlextract import URLExtract
import requests
from bs4 import BeautifulSoup as bs
from urlextract import URLExtract
# import runpod

app = FastAPI()

llm = init_and_load()
retriever = load_data("/workspace/mistral_deployment/ai_ad_generation/flipkart_products.csv")
print("loaded csv data")

def extract_links_from_text(text):
    # Create an instance of URLExtract
    extractor = URLExtract()

    # Use the extractor to find all URLs in the text
    links = extractor.find_urls(text)

    return links[0]

def scrape_product_description(product_link):
    try:
        product_page = requests.get(product_link)
        product_soup = bs(product_page.text, "html.parser")
        print(product_soup)

        description_tag = product_soup.find("div", class_="_1mXcCf RmoJUa")
        print(description_tag)
        product_description = description_tag.get_text(strip=True) if description_tag else "N/A"

        return product_description
    except Exception as e:
        print(f"Error scraping product description for {product_link}: {str(e)}")
        return "N/A"

def scrape_product_name(link):
    try:
      product_page = requests.get(link)
      print(link)
      print(product_page)
          
      product_soup = bs(product_page.text, "html.parser")
      
      name_tag = product_soup.find("span", class_="B_NuCI")
      description_tag = product_soup.find("div", class_="_1mXcCf RmoJUa")
        
      product_name = description_tag.get_text(strip=True) if name_tag else "N/A"
      product_description = description_tag.get_text(strip=True) if description_tag else "N/A"

      return product_name, product_description
    except Exception as e:
      print(f"Error scraping product description for {link}: {str(e)}")
      return "N/A"
    
class Query(BaseModel):
    prompt : str

@app.post("/generate")
def generate(query:Query):
    # llm_chain = LLMChain(llm=llm)
    # query = query["prompt"]
    prompt = query.prompt
    print(prompt)
    links = extract_links_from_text(prompt)
    product_name, product_description = scrape_product_name(links)
#    product_desc = scrape_product_description(links)
    
    qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    verbose=True)

    custom_prompt = f"""You are an e-commerce marketer who can generate outstanding taglines for products
        The name of the product is: {product_name}
        The description of the product is: {product_description}
        Pick out the most outstanding feature of this product and use that in the tagline.
        Create a tagline within 10 words.
    """
    print(custom_prompt)
    result = qa.run(custom_prompt)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
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