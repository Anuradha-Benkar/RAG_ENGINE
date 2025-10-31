# """
# Main RAG Service - Orchestrates all components
# """
# import os
# from typing import Dict, List
# from datetime import datetime
# import json

# from config import Config
# from text_processor import TextProcessor
# from vector_store import VectorStore
# from llm_answer import LLMAnswer
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# class ProjectRAG:
#     """Main RAG Service"""
    
#     def __init__(self, verbose: bool = True):
#         """Initialize RAG System"""
#         self.verbose = verbose
        
        
        
#         # Initialize components
#         self.text_processor = TextProcessor(
#             spacy_model=os.getenv('SPACY_MODEL'),
#             verbose=verbose
#         )
        
#         self.vector_store = VectorStore(
#             qdrant_url= os.getenv('QDRANT_URL'),
#             qdrant_key=os.getenv('QDRANT_API_KEY'),
#             collection_name=os.getenv('COLLECTION_NAME'),
#             embedding_model= "sentence-transformers/all-MiniLM-L6-v2",
#             verbose=verbose
#         )
        
#         self.llm_answer = LLMAnswer(
#             groq_api_key= os.getenv('GROQ_API_KEY'),
#             verbose=verbose
#         )
        
#         if self.verbose:
#             print("✅ RAG System initialized\n")

#     def create_embeddings(
#         self,
#         data_folder: str,
#         force_recreate: bool = False,
#         save_chunks: bool = True
#     ) -> bool:
#         """Create embeddings from documents"""
#         if not os.path.exists(data_folder):
#             print(f"❌ Data folder not found: {data_folder}")
#             return False
        
#         if self.verbose:
#             print(f"\n{'='*100}")
#             print(f"📂 LOADING DOCUMENTS FROM: {data_folder}")
#             print(f"{'='*100}\n")
        
#         all_chunks = []
#         file_stats = {}
        
#         txt_files = sorted([f for f in os.listdir(data_folder) if f.endswith('.txt')])
        
#         if self.verbose:
#             print(f"📋 Found {len(txt_files)} text files to process\n")
        
#         # Process each file
#         for file in txt_files:
#             path = os.path.join(data_folder, file)
#             file_chunks = self.text_processor.process_file(path, file)
#             file_stats[file] = len(file_chunks)
#             all_chunks.extend(file_chunks)
            
#         if not all_chunks:
#             print("❌ No chunks created")
#             return False
        
#         if self.verbose:
#             print(f"\n{'='*100}")
#             print("📊 PROCESSING SUMMARY")
#             print(f"{'='*100}\n")
#             for file, count in file_stats.items():
#                 print(f"  📄 {file}: {count} chunks")
#             print(f"\n  ✅ TOTAL CHUNKS: {len(all_chunks)}")
#             print(f"{'='*100}\n")
        
#         # Upload to Qdrant
#         return self.vector_store.create_embeddings(all_chunks, force_recreate)
    
#     def retrieve(self, query: str, top_k: int = None) -> Dict:
#         """Retrieve relevant documents"""
#         if top_k is None:
#             top_k = Config.DEFAULT_TOP_K
#         return self.vector_store.retrieve(query, top_k)
    
#     def query(self, question: str, top_k: int = None) -> str:
#         """Query the RAG system"""
#         if top_k is None:
#             top_k = Config.DEFAULT_TOP_K
        
#         if self.verbose:
#             print(f"\n{'='*80}")
#             print(f"🔍 Query: {question}")
#             print(f"{'='*80}\n")
        
#         try:
#             # Retrieve relevant documents
#             retrieval = self.retrieve(question, top_k)
            
#             # Generate answer
#             answer = "\n\n".join(retrieval['documents']) #self.llm_answer.generate_answer(question, retrieval)
            
#             if self.verbose:
#                 # print(f"💡 Answer:\n{answer}\n")
#                 print(f"{'-'*80}")
#                 print(f"📚 Sources:")
#                 for i, (proj, src, sim) in enumerate(
#                     zip(retrieval['projects'], retrieval['sources'], 
#                         retrieval['similarities']), 1
#                 ):
#                     print(f"  {i}. {proj} (from {src}) - Similarity: {sim:.4f}")
#                 print(f"{'='*80}\n")
            
#             return answer
#         except Exception as e:
#             print(f"❌ Error: {e}")
#             raise


# def rag_retrieve(question):
#     try:
#         # Initialize RAG System
#         rag = ProjectRAG(verbose=True)
        
#         # Step 1: Create embeddings (auto-skips if exists)
#         print("="*100)
#         print("STEP 1: CREATING/LOADING EMBEDDINGS")
#         print("="*100 + "\n")
        
#         try:
#             success = rag.create_embeddings(
#                 data_folder=Config.RAG_DATA_FOLDER,
#                 save_chunks=True,
#                 force_recreate=False  # Only recreate if necessary
#             )
#             if not success:
#                 print("✅ Using existing collection (skipped recreation).")
#         except Exception as e:
#             print(f"❌ Error during embedding creation: {e}")
#             import traceback
#             traceback.print_exc()
#             return str(e)

#         try:
#             question = question #input("❓ Your query: ").strip()
            
#             if question:
#                 result = rag.query(question)
#                 # print(f"Result rag_retrieve : {result}")
#             else:
#                 print("⚠️  Please enter a valid query\n")

#         except Exception as e:
#             print(f"❌ Error: {e}\n")

#         return result
    
#     except Exception as e:
#         print(f"❌ Fatal error: {e}")
#         import traceback
#         traceback.print_exc()
#         return str(e)






"""
Main RAG Service - Orchestrates all components
"""
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import os
from typing import Dict, List, Optional
from datetime import datetime
import json

from config import Config
from text_processor import TextProcessor
from vector_store import VectorStore
from llm_answer import LLMAnswer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ProjectRAG:
    """Main RAG Service"""
    
    def __init__(self, verbose: bool = True):
        """Initialize RAG System"""
        self.verbose = verbose
        
        # Initialize components
        self.text_processor = TextProcessor(
            groq_api_key=os.getenv('GROQ_API_KEY'),
            verbose=verbose
        )
        
        self.vector_store = VectorStore(
            qdrant_url=os.getenv('QDRANT_URL'),
            qdrant_key=os.getenv('QDRANT_API_KEY'),
            collection_name=os.getenv('COLLECTION_NAME'),
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
            verbose=verbose
        )
        
        self.llm_answer = LLMAnswer(
            groq_api_key=os.getenv('GROQ_API_KEY'),
            verbose=verbose
        )
        
        if self.verbose:
            print("✅ RAG System initialized\n")

    def create_embeddings(
        self,
        data_folder: str,
        force_recreate: bool = False,
        save_chunks: bool = True
    ) -> bool:
        """Create embeddings from documents"""
        if not os.path.exists(data_folder):
            print(f"❌ Data folder not found: {data_folder}")
            return False
        
        if self.verbose:
            print(f"\n{'='*100}")
            print(f"📂 LOADING DOCUMENTS FROM: {data_folder}")
            print(f"{'='*100}\n")
        
        all_chunks = []
        file_stats = {}
        
        txt_files = sorted([f for f in os.listdir(data_folder) if f.endswith('.txt')])
        
        if self.verbose:
            print(f"📋 Found {len(txt_files)} text files to process\n")
        
        # Process each file
        for file in txt_files:
            path = os.path.join(data_folder, file)
            file_chunks = self.text_processor.process_file(path, file)
            file_stats[file] = len(file_chunks)
            all_chunks.extend(file_chunks)
            
        if not all_chunks:
            print("❌ No chunks created")
            return False
        
        if self.verbose:
            print(f"\n{'='*100}")
            print("📊 PROCESSING SUMMARY")
            print(f"{'='*100}\n")
            for file, count in file_stats.items():
                print(f"  📄 {file}: {count} chunks")
            print(f"\n  ✅ TOTAL CHUNKS: {len(all_chunks)}")
            print(f"{'='*100}\n")
        
        # Upload to Qdrant
        return self.vector_store.create_embeddings(all_chunks, force_recreate)
    
    def retrieve(
        self, 
        query: str, 
        top_k: int = None,
        project_types: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None
    ) -> Dict:
        """
        Retrieve relevant documents with optional filtering
        
        Args:
            query: Search query
            top_k: Number of results
            project_types: Filter by project types
            keywords: Filter by keywords
        """
        if top_k is None:
            top_k = Config.DEFAULT_TOP_K
        return self.vector_store.retrieve(query, top_k, project_types, keywords)
    
    def query(
        self, 
        question: str, 
        top_k: int = None,
        project_types: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None
    ) -> str:
        """
        Query the RAG system with optional filtering
        
        Args:
            question: User question
            top_k: Number of results
            project_types: Filter by project types (e.g., ["Healthcare AI"])
            keywords: Filter by keywords (e.g., ["machine learning"])
        """
        if top_k is None:
            top_k = Config.DEFAULT_TOP_K
        
        if self.verbose:
            print(f"\n{'='*80}")
            print(f"🔍 Query: {question}")
            print(f"{'='*80}\n")
        
        try:
            # Retrieve relevant documents
            retrieval = self.retrieve(question, top_k, project_types, keywords)
            
            # Generate answer
            answer = "\n\n".join(retrieval['documents'])
            
            if self.verbose:
                print(f"{'-'*80}")
                print(f"📚 Sources:")
                for i, (proj, src, sim, ptype) in enumerate(
                    zip(
                        retrieval['projects'], 
                        retrieval['sources'], 
                        retrieval['similarities'],
                        retrieval['project_types']
                    ), 1
                ):
                    print(f"  {i}. {proj} (from {src}) - Type: {ptype} - Similarity: {sim:.4f}")
                print(f"{'='*80}\n")
            
            return answer
        except Exception as e:
            print(f"❌ Error: {e}")
            raise


# def rag_retrieve(question, project_types=None, keywords=None):
#     """
#     Retrieve documents for a question with optional metadata filtering
    
#     Args:
#         question: User query
#         project_types: Optional list of project types to filter
#         keywords: Optional list of keywords to filter
    
#     Example:
#         rag_retrieve("AI healthcare projects", project_types=["Healthcare AI"])
#         rag_retrieve("machine learning projects", keywords=["machine learning", "AI"])
#     """
#     try:
#         # Initialize RAG System
#         rag = ProjectRAG(verbose=True)
        
#         # Step 1: Create embeddings (auto-skips if exists)
#         print("="*100)
#         print("STEP 1: CREATING/LOADING EMBEDDINGS")
#         print("="*100 + "\n")
        
#         try:
#             success = rag.create_embeddings(
#                 data_folder=Config.RAG_DATA_FOLDER,
#                 save_chunks=True,
#                 force_recreate=False
#             )
#             if not success:
#                 print("✅ Using existing collection (skipped recreation).")
#         except Exception as e:
#             print(f"❌ Error during embedding creation: {e}")
#             import traceback
#             traceback.print_exc()
#             return str(e)

#         try:
#             if question:
#                 result = rag.query(question, project_types=project_types, keywords=keywords)
#             else:
#                 print("⚠️  Please enter a valid query\n")
#                 return None

#         except Exception as e:
#             print(f"❌ Error: {e}\n")
#             return None

#         return result
    
#     except Exception as e:
#         print(f"❌ Fatal error: {e}")
#         import traceback
#         traceback.print_exc()
#         return str(e)


def rag_retrieve(input_data=None, question=None, project_types=None, keywords=None):
    """
    Retrieve documents with flexible input formats
    
    Args:
        input_data: Dict with 'Query' and 'project_types' keys
        OR
        question: Direct query string
        project_types: List or single string of project types
        keywords: List of keywords
    
    Examples:
        # Method 1: Dict input
        input_data = {
            'Query': "Find AI projects...",
            'project_types': 'media_technology'
        }
        result = rag_retrieve(input_data=input_data)
        
        # Method 2: Direct parameters
        result = rag_retrieve(
            question="Find AI projects...",
            project_types=["Healthcare", "Fintech / Banking Analytics"]
        )
    """
    try:
        # Parse input
        if input_data:
            query = input_data.get('Query', '')
            filter_types = input_data.get('project_types')
            # filter_keywords = input_data.get('keywords')
            filter_keywords = input_data.get('keywords') or input_data.get('Keywords')  # ← Support both
        else:
            query = question
            filter_types = project_types
            filter_keywords = keywords
        
        # Normalize project_types to list
        if filter_types:
            if isinstance(filter_types, str):
                # Map common aliases
                type_mapping = {
                    'media_technology': ['Media Technology'],
                    'healthcare': ['Healthcare'],
                    'fintech': ['Fintech / Banking Analytics'],
                    'ai_platforms': ['AI / Generative AI Platforms'],
                    'data_analytics': ['Data Analytics / Predictive Modeling'],
                    'video_analytics': ['Video Analytics / Computer Vision'],
                    'drone': ['AI-Based Surveillance / Drone Solutions'],
                    'workflow': ['Agentic Workflow Systems']
                }
                filter_types = type_mapping.get(filter_types.lower(), [filter_types])
            elif not isinstance(filter_types, list):
                filter_types = [filter_types]
        
        # Normalize keywords to list
        if filter_keywords and not isinstance(filter_keywords, list):
            filter_keywords = [filter_keywords]
        
        # Initialize RAG System
        rag = ProjectRAG(verbose=True)
        
        # Step 1: Create embeddings (auto-skips if exists)
        print("="*100)
        print("STEP 1: CREATING/LOADING EMBEDDINGS")
        print("="*100 + "\n")
        
        try:
            success = rag.create_embeddings(
                data_folder=Config.RAG_DATA_FOLDER,
                save_chunks=True,
                force_recreate=False
            )
            if not success:
                print("✅ Using existing collection (skipped recreation).\n")
        except Exception as e:
            print(f"❌ Error during embedding creation: {e}")
            import traceback
            traceback.print_exc()
            return str(e)
        
        # Step 2: Query with filters
        print("="*100)
        print("STEP 2: QUERYING WITH FILTERS")
        print("="*100 + "\n")
        
        if query:
            result = rag.query(
                question=query,
                project_types=filter_types,
                keywords=filter_keywords
            )
            return result
        else:
            print("⚠️ Please enter a valid query\n")
            return None
            
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return str(e)