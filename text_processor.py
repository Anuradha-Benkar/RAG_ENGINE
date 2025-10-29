# """
# Text Processing and Chunking Module

# """
# import os  # 🟢 Added
# import re
# import json  # 🟢 Added
# from typing import List, Dict
# from langchain_core.documents import Document


# class TextProcessor:
#     """Handles text processing and chunking"""
    
#     def __init__(self, spacy_model: str = "en_core_web_sm", verbose: bool = True):
#         self.verbose = verbose
#         self._load_spacy_model(spacy_model)

#         # 🟢 Added: Directory to store processed chunk info
#         self.processed_dir = "processed_chunks"
#         os.makedirs(self.processed_dir, exist_ok=True)
    
#     def _load_spacy_model(self, model_name: str):
#         """Load spaCy model for NER"""
#         try:
#             self.nlp = spacy.load(model_name)
#             if self.verbose:
#                 print("✅ spaCy model loaded")
#         except:
#             if self.verbose:
#                 print("📥 Downloading spaCy model...")
#             import subprocess
#             subprocess.run(
#                 ["python", "-m", "spacy", "download", model_name],
#                 stdout=subprocess.DEVNULL,
#                 stderr=subprocess.DEVNULL
#             )
#             self.nlp = spacy.load(model_name)
#             if self.verbose:
#                 print("✅ spaCy model loaded")
    
#     def extract_keywords_from_text(self, text: str) -> List[str]:
#         """Extract keywords using spaCy NER"""
#         doc = self.nlp(text)
#         keywords = set()
        
#         # Extract named entities
#         for ent in doc.ents:
#             keywords.add(ent.text)
        
#         # Extract noun chunks
#         for chunk in doc.noun_chunks:
#             if len(chunk.text.split()) <= 3:
#                 keywords.add(chunk.text)
        
#         return list(keywords)
    
#     def _extract_projects(self, text: str) -> List[Dict]:
#         """Extract projects from text"""
#         projects = []
#         lines = text.split('\n')
#         current_project = []
#         project_num = None
        
#         for line in lines:
#             # Check if line starts a new project
#             if line.strip() and (
#                 (line.strip()[0].isdigit() and '.' in line.split()[0]) or
#                 line.strip().startswith('###')
#             ):
#                 # Save previous project
#                 if current_project:
#                     content = '\n'.join(current_project).strip()
#                     if content:
#                         keywords = self.extract_keywords_from_text(content)
#                         projects.append({
#                             'number': project_num,
#                             'content': content,
#                             'keywords': keywords
#                         })
                
#                 # Start new project
#                 current_project = [line]
#                 match = re.search(r'(\d+)', line)
#                 if match:
#                     project_num = int(match.group(1))
#             else:
#                 if current_project or line.strip():
#                     current_project.append(line)
        
#         # Save last project
#         if current_project:
#             content = '\n'.join(current_project).strip()
#             if content:
#                 keywords = self.extract_keywords_from_text(content)
#                 projects.append({
#                     'number': project_num,
#                     'content': content,
#                     'keywords': keywords
#                 })
        
#         return projects
    
#     def process_file(self, filepath: str, filename: str) -> List[Document]:
#         """Process a single file and return chunks"""
#         file_chunks = []

#         # 🟢 Added: Check if this file's chunks are already created
#         processed_file_path = os.path.join(self.processed_dir, f"{filename}_chunks.json")
#         if os.path.exists(processed_file_path):
#             if self.verbose:
#                 print(f"⚠️  Skipping {filename} — chunks already exist.")
#             with open(processed_file_path, 'r', encoding='utf-8') as f:
#                 data = json.load(f)
#                 for doc_data in data:
#                     file_chunks.append(Document(**doc_data))
#             return file_chunks
        
        
#         try:
#             with open(filepath, 'r', encoding='utf-8') as f:
#                 text = f.read()
                
#                 if self.verbose:
#                     print(f"\n{'='*100}")
#                     print(f"📄 PROCESSING FILE: {filename}")
#                     print(f"{'='*100}")
                
#                 projects = self._extract_projects(text)
#                 if self.verbose:
#                     print(f"  ✅ Found {len(projects)} projects in {filename}")
                
#                 for project in projects:
#                     doc = Document(
#                         page_content=project['content'],
#                         metadata={
#                             'source': filename,
#                             'project_number': project['number'],
#                             'file_specific_id': f"{filename}_{project['number']}",
#                             'keywords': project['keywords']
#                         }
#                     )
#                     file_chunks.append(doc)
                
#                  # 🟢 Added: Save chunks so next time we skip this file
#                 with open(processed_file_path, 'w', encoding='utf-8') as f:
#                     json.dump([{
#                         "page_content": d.page_content,
#                         "metadata": d.metadata
#                     } for d in file_chunks], f, ensure_ascii=False, indent=2)

#                 if self.verbose:
#                     print(f"  ✅ Completed processing {filename}\n")
        
#         except Exception as e:
#             if self.verbose:
#                 print(f"  ❌ Error processing {filename}: {e}\n")
        
#         return file_chunks




#######################################################################################################
# """
# Text Processing and Chunking Module
# """
# import os
# import re
# import json
# from typing import List, Dict
# from langchain_core.documents import Document
# from groq import Groq


# class TextProcessor:
#     """Handles text processing and chunking"""
    
#     def __init__(self, groq_api_key: str = None, verbose: bool = True):
#         self.verbose = verbose
#         self.groq_api_key = groq_api_key
        
#         # Initialize Groq client for LLM-based metadata extraction
#         if self.groq_api_key:
#             self.groq_client = Groq(api_key=self.groq_api_key)
#             if self.verbose:
#                 print("✅ Groq LLM initialized for metadata extraction")
#         else:
#             self.groq_client = None
#             if self.verbose:
#                 print("⚠️  No Groq API key provided. Metadata extraction disabled.")

#         # Directory to store processed chunk info
#         self.processed_dir = "processed_chunks"
#         os.makedirs(self.processed_dir, exist_ok=True)
    
#     def _extract_metadata_with_llm(self, text: str) -> Dict:
#         """Extract project type and keywords using LLM"""
#         if not self.groq_client:
#             return {"project_type": "Unknown", "keywords": []}
        
#         try:
#             prompt = f"""Analyze the following project description and extract:
# 1. Project Type (e.g., Healthcare AI, Financial Analytics, Legal Tech,AI,DataSCience, Data Analytics etc.)
# 2. 5-7 meaningful keywords (technical terms, domains, technologies)

# Project Description:
# {text[:1500]}

# Respond in JSON format:
# {{
#   "project_type": "...",
#   "keywords": ["...", "...", ...]
# }}"""

#             response = self.groq_client.chat.completions.create(
#                 messages=[{"role": "user", "content": prompt}],
#                 model="llama-3.1-8b-instant",
#                 temperature=0.1,
#                 max_tokens=200
#             )
            
#             result = response.choices[0].message.content.strip()
            
#             # Parse JSON response
#             if "```json" in result:
#                 result = result.split("```json")[1].split("```")[0].strip()
#             elif "```" in result:
#                 result = result.split("```")[1].split("```")[0].strip()
            
#             metadata = json.loads(result)
#             return metadata
        
#         except Exception as e:
#             if self.verbose:
#                 print(f"⚠️  LLM metadata extraction failed: {e}")
#             return {"project_type": "Unknown", "keywords": []}
    
#     def _extract_projects(self, text: str) -> List[Dict]:
#         """Extract projects from text"""
#         projects = []
#         lines = text.split('\n')
#         current_project = []
#         project_num = None
        
#         for line in lines:
#             # Check if line starts a new project
#             if line.strip() and (
#                 (line.strip()[0].isdigit() and '.' in line.split()[0]) or
#                 line.strip().startswith('###')
#             ):
#                 # Save previous project
#                 if current_project:
#                     content = '\n'.join(current_project).strip()
#                     if content:
#                         # Extract metadata using LLM
#                         metadata = self._extract_metadata_with_llm(content)
#                         projects.append({
#                             'number': project_num,
#                             'content': content,
#                             'project_type': metadata.get('project_type', 'Unknown'),
#                             'keywords': metadata.get('keywords', [])
#                         })
                
#                 # Start new project
#                 current_project = [line]
#                 match = re.search(r'(\d+)', line)
#                 if match:
#                     project_num = int(match.group(1))
#             else:
#                 if current_project or line.strip():
#                     current_project.append(line)
        
#         # Save last project
#         if current_project:
#             content = '\n'.join(current_project).strip()
#             if content:
#                 metadata = self._extract_metadata_with_llm(content)
#                 projects.append({
#                     'number': project_num,
#                     'content': content,
#                     'project_type': metadata.get('project_type', 'Unknown'),
#                     'keywords': metadata.get('keywords', [])
#                 })
        
#         return projects
    
#     def process_file(self, filepath: str, filename: str) -> List[Document]:
#         """Process a single file and return chunks"""
#         file_chunks = []

#         # Check if this file's chunks are already created
#         processed_file_path = os.path.join(self.processed_dir, f"{filename}_chunks.json")
#         if os.path.exists(processed_file_path):
#             if self.verbose:
#                 print(f"⚠️  Skipping {filename} — chunks already exist.")
#             with open(processed_file_path, 'r', encoding='utf-8') as f:
#                 data = json.load(f)
#                 for doc_data in data:
#                     file_chunks.append(Document(**doc_data))
#             return file_chunks
        
#         try:
#             with open(filepath, 'r', encoding='utf-8') as f:
#                 text = f.read()
                
#                 if self.verbose:
#                     print(f"\n{'='*100}")
#                     print(f"📄 PROCESSING FILE: {filename}")
#                     print(f"{'='*100}")
                
#                 projects = self._extract_projects(text)
#                 if self.verbose:
#                     print(f"  ✅ Found {len(projects)} projects in {filename}")
                
#                 for project in projects:
#                     doc = Document(
#                         page_content=project['content'],
#                         metadata={
#                             'source': filename,
#                             'project_number': project['number'],
#                             'file_specific_id': f"{filename}_{project['number']}",
#                             'project_type': project['project_type'],
#                             'keywords': project['keywords']
#                         }
#                     )
#                     file_chunks.append(doc)
                
#                 # Save chunks so next time we skip this file
#                 with open(processed_file_path, 'w', encoding='utf-8') as f:
#                     json.dump([{
#                         "page_content": d.page_content,
#                         "metadata": d.metadata
#                     } for d in file_chunks], f, ensure_ascii=False, indent=2)

#                 if self.verbose:
#                     print(f"  ✅ Completed processing {filename}\n")
        
#         except Exception as e:
#             if self.verbose:
#                 print(f"  ❌ Error processing {filename}: {e}\n")
        
#         return file_chunks
    #######################################################################################################



"""
Text Processing and Chunking Module - Simple Rule-Based Version
"""
import os
import re
import json
from typing import List, Dict
from langchain_core.documents import Document


class TextProcessor:
    """Handles text processing and chunking with rule-based metadata"""
    
    def __init__(self, groq_api_key: str = None, verbose: bool = True):
        self.verbose = verbose
        self.groq_api_key = groq_api_key
        
        if self.verbose:
            print("✅ Text Processor initialized (Rule-based metadata extraction)")

        # Directory to store processed chunk info
        self.processed_dir = "processed_chunks"
        os.makedirs(self.processed_dir, exist_ok=True)
        
        # Define project type rules
        self.project_type_rules = {
            "Healthcare AI": ["healthcare", "medical", "cancer", "oncology", "diagnostic", "patient", "clinical"],
            "Financial Analytics": ["finance", "investment", "stock", "trading", "portfolio", "monte carlo", "analytics"],
            "Entertainment AI": ["celebrity", "talent", "entertainment", "event", "hosting"],
            "Surveillance & Inspection": ["drone", "surveillance", "inspection", "monitoring", "warehouse"],
            "Data Analytics": ["excel", "spreadsheet", "data insight", "reporting", "automation"],
            "Video Analytics": ["video", "multimedia", "content analysis"],
            "Legal Tech": ["legal", "document", "contract", "compliance", "regulation"],
            "Developer Tools": ["code", "debugging", "developer", "api", "sdk"],
            "Chatbot & NLP": ["chatbot", "conversational", "nlp", "natural language"],
            "RegTech": ["regulatory", "compliance", "rbi", "fed", "apra"],
        }
        
        # Define common technical keywords
        self.tech_keywords = [
            "AI", "machine learning", "deep learning", "neural network",
            "data pipeline", "ETL", "analytics", "predictive",
            "generative AI", "LLM", "chatbot", "NLP",
            "cloud", "AWS", "deployment", "scalable",
            "Django", "React", "API", "REST",
            "automation", "workflow", "agentic",
            "real-time", "streaming", "batch processing",
            "recommendation", "personalization",
            "computer vision", "image recognition",
            "time series", "forecasting"
        ]
    
    def _extract_metadata_rule_based(self, text: str) -> Dict:
        """Extract project type and keywords using rules"""
        text_lower = text.lower()
        
        # Determine project type
        project_type = "General AI Solution"
        max_matches = 0
        
        for ptype, keywords in self.project_type_rules.items():
            matches = sum(1 for kw in keywords if kw in text_lower)
            if matches > max_matches:
                max_matches = matches
                project_type = ptype
        
        # Extract keywords
        found_keywords = []
        for keyword in self.tech_keywords:
            if keyword.lower() in text_lower:
                found_keywords.append(keyword)
        
        # Add domain-specific keywords from text
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        for word in words[:10]:
            if len(word) > 3 and word not in found_keywords:
                found_keywords.append(word)
        
        # Limit to 7 keywords
        found_keywords = found_keywords[:7]
        
        if self.verbose:
            print(f"✅ Extracted: Type='{project_type}', Keywords={found_keywords[:3]}...\n")
        
        return {
            "project_type": project_type,
            "keywords": found_keywords
        }
    
    def _extract_projects(self, text: str) -> List[Dict]:
        """Extract projects from text"""
        projects = []
        lines = text.split('\n')
        current_project = []
        project_num = None
        
        for line in lines:
            # Check if line starts a new project
            if line.strip() and (
                (line.strip()[0].isdigit() and '.' in line.split()[0]) or
                line.strip().startswith('###')
            ):
                # Save previous project
                if current_project:
                    content = '\n'.join(current_project).strip()
                    if content:
                        # Extract metadata using rules
                        metadata = self._extract_metadata_rule_based(content)
                        projects.append({
                            'number': project_num,
                            'content': content,
                            'project_type': metadata.get('project_type', 'General AI Solution'),
                            'keywords': metadata.get('keywords', [])
                        })
                
                # Start new project
                current_project = [line]
                match = re.search(r'(\d+)', line)
                if match:
                    project_num = int(match.group(1))
            else:
                if current_project or line.strip():
                    current_project.append(line)
        
        # Save last project
        if current_project:
            content = '\n'.join(current_project).strip()
            if content:
                metadata = self._extract_metadata_rule_based(content)
                projects.append({
                    'number': project_num,
                    'content': content,
                    'project_type': metadata.get('project_type', 'General AI Solution'),
                    'keywords': metadata.get('keywords', [])
                })
        
        return projects
    
    def process_file(self, filepath: str, filename: str) -> List[Document]:
        """Process a single file and return chunks"""
        file_chunks = []

        # Check if this file's chunks are already created
        processed_file_path = os.path.join(self.processed_dir, f"{filename}_chunks.json")
        if os.path.exists(processed_file_path):
            if self.verbose:
                print(f"⚠️  Skipping {filename} — chunks already exist.")
            with open(processed_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for doc_data in data:
                    file_chunks.append(Document(**doc_data))
            return file_chunks
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
                
                if self.verbose:
                    print(f"\n{'='*100}")
                    print(f"📄 PROCESSING FILE: {filename}")
                    print(f"{'='*100}")
                
                projects = self._extract_projects(text)
                if self.verbose:
                    print(f"  ✅ Found {len(projects)} projects in {filename}")
                
                for project in projects:
                    doc = Document(
                        page_content=project['content'],
                        metadata={
                            'source': filename,
                            'project_number': project['number'],
                            'file_specific_id': f"{filename}_{project['number']}",
                            'project_type': project['project_type'],
                            'keywords': project['keywords']
                        }
                    )
                    file_chunks.append(doc)
                
                # Save chunks so next time we skip this file
                with open(processed_file_path, 'w', encoding='utf-8') as f:
                    json.dump([{
                        "page_content": d.page_content,
                        "metadata": d.metadata
                    } for d in file_chunks], f, ensure_ascii=False, indent=2)

                if self.verbose:
                    print(f"  ✅ Completed processing {filename}\n")
        
        except Exception as e:
            if self.verbose:
                print(f"  ❌ Error processing {filename}: {e}\n")
        
        return file_chunks