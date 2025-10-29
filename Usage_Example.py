# """
# Usage Example - How to use the RAG System
# """
# from rag_service import rag_retrieve

# question = "Find documents on AI-based platforms: Excelinsight for automated large‑scale Excel analysis, Fintellix for generative AI chatbots delivering RBI/FED/APRA regulatory updates to banks, and AeginaCo for real‑time investment analytics using live data feeds, statistical modeling, Monte Carlo simulation, and interactive dashboards"

# result = rag_retrieve(question)
# print(f"💡 Answer:\n type{type(result)} \n{result}\n")
# #git -m commit "add keyword extraction, but not use at retrieve"

# #answer = rag_retrieve(generated_queries)






"""
Usage Example - How to use the RAG System
"""
from rag_service import rag_retrieve

question =" Retrieve documents on the following projects: DORIS (digital oncology platform built with Django, Langchain, AWS for agentic workflow), Videochef (video analysis platform enabling search and interaction within videos), Volar Alta (AI‑driven drone surveillance for cement industry and warehouses), Fintellix (generative AI chatbot providing regulatory updates from RBI, FED, APRA for banks), Socketmobile (intelligent agentic code debugging tool with data pipeline and web crawler), Excelinsight (AI‑powered platform for large Excel file insights, automation, reporting, enrichment, and discrepancy detection)"

result = rag_retrieve(question)
print(f"💡 Answer:\n{result}\n")