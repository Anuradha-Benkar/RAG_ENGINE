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
        
         # Define project type rules - NOW SUPPORTS MULTIPLE LABELS
        self.project_type_rules = {
            "AI / Generative AI Platforms": [
                "generative ai", "llm", "chatbot", "conversational", "nlp", 
                "natural language", "gpt", "claude", "ai platform", "agentic", 
                "langchain", "openai"
            ],
            "Data Analytics / Predictive Modeling": [
                "analytics", "predictive", "forecasting", "time series", 
                "monte carlo", "simulation", "statistical", "modeling", 
                "data insight", "reporting", "dashboard"
            ],
            "Healthcare": [
                "healthcare", "medical", "cancer", "oncology", "diagnostic", 
                "patient", "clinical", "health", "disease"
            ],
            "Agentic Workflow Systems": [
                "agentic", "workflow", "automation", "orchestration", 
                "pipeline", "etl", "batch processing", "task management"
            ],
            "Video Analytics / Computer Vision": [
                "video", "computer vision", "image recognition", "multimedia", 
                "content analysis", "visual", "cv", "detection", "frame"
            ],
            "AI-Based Surveillance / Drone Solutions": [
                "drone", "surveillance", "inspection", "monitoring", 
                "warehouse", "uav", "aerial", "security", "iot"
            ],
            "Fintech / Banking Analytics": [
                "fintech", "banking", "finance", "investment", "stock", 
                "trading", "portfolio", "regulatory", "compliance", 
                "rbi", "fed", "apra", "excel"
            ],
            "Media Technology": [
                "media", "entertainment", "production technology", 
                "hybrid site operations", "vmware", "infrastructure", 
                "network architecture", "data center", "security vulnerability",
                "resilience engineering", "it policy", "technology strategy"
            ]
        }
            
        # Define common technical keywords
        self.tech_keywords = [
            # AI/ML Core
            "AI", "machine learning", "deep learning", "neural network", 
            "generative AI", "LLM", "GPT", "transformer", "NLP",
            
            # Data & Analytics
            "data pipeline", "ETL", "analytics", "predictive modeling", 
            "forecasting", "Monte Carlo", "statistical modeling",
            
            # Development
            "Django", "React", "API", "REST", "cloud", "AWS", 
            "deployment", "scalable", "microservices",
            
            # Specialized
            "chatbot", "conversational AI", "computer vision", 
            "image recognition", "video analytics", "drone technology",
            
            # Automation & Workflow
            "automation", "workflow", "agentic", "real-time", 
            "streaming", "batch processing", "orchestration",
            
            # Infrastructure & Operations
            "VMware", "infrastructure", "network architecture", 
            "data center", "security vulnerability", "resilience",
            
            # Business
            "recommendation", "personalization", "compliance", 
            "regulatory", "investment analytics", "Excel automation",
            "productivity enhancement"
        ]
    
    # def _extract_metadata_rule_based(self, text: str) -> Dict:
    #     """Extract project type and keywords using rules"""
    #     text_lower = text.lower()
        
    #     # Determine project type
    #     project_type = "General AI Solution"
    #     max_matches = 0
        
    #     for ptype, keywords in self.project_type_rules.items():
    #         matches = sum(1 for kw in keywords if kw in text_lower)
    #         if matches > max_matches:
    #             max_matches = matches
    #             project_type = ptype
        
    #     # Extract keywords
    #     found_keywords = []
    #     for keyword in self.tech_keywords:
    #         if keyword.lower() in text_lower:
    #             found_keywords.append(keyword)
        
    #     # Add domain-specific keywords from text
    #     words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
    #     for word in words[:10]:
    #         if len(word) > 3 and word not in found_keywords:
    #             found_keywords.append(word)
        
    #     # Limit to 7 keywords
    #     found_keywords = found_keywords[:7]
        
    #     if self.verbose:
    #         print(f"✅ Extracted: Type='{project_type}', Keywords={found_keywords[:3]}...\n")
        
    #     return {
    #         "project_type": project_type,
    #         "keywords": found_keywords
    #     }

    def _extract_metadata_rule_based(self, text: str) -> Dict:
        """Extract multiple project types and exactly 5 keywords using rules"""
        text_lower = text.lower()
        
        # Determine ALL matching project types (multi-label)
        matched_types = []
        type_scores = {}
        
        for ptype, keywords in self.project_type_rules.items():
            matches = sum(1 for kw in keywords if kw in text_lower)
            if matches > 0:
                type_scores[ptype] = matches
        
        # Sort by match count and take top matches
        sorted_types = sorted(type_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Take all types with at least 1 match, or default to first type
        if sorted_types:
            # Include all types with matches (you can limit to top 3 if needed)
            matched_types = [ptype for ptype, score in sorted_types if score > 0]
        else:
            matched_types = ["AI / Generative AI Platforms"]  # Default
        
        # Extract keywords with scoring
        keyword_scores = {}
        
        # Score technical keywords
        for keyword in self.tech_keywords:
            if keyword.lower() in text_lower:
                count = text_lower.count(keyword.lower())
                keyword_scores[keyword] = count
        
        # Sort by frequency and get top 5
        sorted_keywords = sorted(
            keyword_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        found_keywords = [kw for kw, score in sorted_keywords[:5]]
        
        # If less than 5, extract capitalized phrases
        if len(found_keywords) < 5:
            words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
            for word in words:
                if len(word) > 3 and word not in found_keywords:
                    found_keywords.append(word)
                    if len(found_keywords) == 5:
                        break
        
        # Ensure exactly 5 keywords
        while len(found_keywords) < 5:
            found_keywords.append(f"General_{len(found_keywords)}")
        
        found_keywords = found_keywords[:5]
        
        if self.verbose:
            print(f"✅ Extracted: Types={matched_types}, Keywords={found_keywords}\n")
        
        return {
            "project_type": matched_types,  # NOW A LIST!
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