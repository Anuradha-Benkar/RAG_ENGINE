# """
# Usage Example - How to use the RAG System
# """
# from rag_service import rag_retrieve

# question = "Find documents on AI-based platforms: Excelinsight for automated large‑scale Excel analysis, Fintellix for generative AI chatbots delivering RBI/FED/APRA regulatory updates to banks, and AeginaCo for real‑time investment analytics using live data feeds, statistical modeling, Monte Carlo simulation, and interactive dashboards"

# result = rag_retrieve(question)
# print(f"💡 Answer:\n type{type(result)} \n{result}\n")
# #git -m commit "add keyword extraction, but not use at retrieve"

# #answer = rag_retrieve(generated_queries)






# """
# Usage Example - How to use the RAG System
# """
# from rag_service import rag_retrieve

# question ="Find projects related to Media & Entertainment IT, Production Technology, Hybrid Site Operations, IT Operations, Security Initiatives, Data Center Design, VMware Infrastructure, Network Architecture, Security Vulnerability Mitigation, Workflow Automation, Infrastructure Modernization, Resilience Engineering, IT Policy Development, Technology Strategy Alignment, and Productivity Enhancement."

# result = rag_retrieve(question)
# print(f"💡 Answer:\n{result}\n")




"""
Usage Example - How to use the RAG System
"""
from rag_service import rag_retrieve

# ============================================
# Simple Usage - Just pass your input dict
# ============================================

input_data = {
    'Query': "Find projects related to  Production Technology, Hybrid Site Operations, IT Operations, Security Initiatives, Data Center Design.",
    #'project_types': ['Fintech / Banking Analytics']
    'keywords': ['Data Security']
}

result = rag_retrieve(input_data=input_data)
print(f"💡 Answer:\n{result}\n")