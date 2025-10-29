# """
# Vector Store Management Module
# """
# from typing import Dict, List
# from qdrant_client import QdrantClient
# # from langchain_community.vectorstores import Qdrant
# from langchain_qdrant import Qdrant
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_core.documents import Document
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# class VectorStore:
#     """Manages Qdrant vector store operations"""
    
#     def __init__(
#         self,
#         qdrant_url: str,
#         qdrant_key: str,
#         collection_name: str,
#         embedding_model: str,
#         verbose: bool = True
#     ):
#         self.qdrant_url= os.getenv('QDRANT_URL')
#         self.qdrant_key=os.getenv('QDRANT_API_KEY')
#         self.collection_name=os.getenv('COLLECTION_NAME')
#         self.embedding_model=os.getenv('EMBEDDING_MODEL')
#         self.verbose=verbose

#         # Initialize vectorstore attribute
#         self.vectorstore = None
        
#         # Initialize embeddings
#         self._initialize_embeddings(self.embedding_model)
        
#         # Initialize Qdrant client
#         self._initialize_client()
        
#         # Auto-connect if collection exists
#         if self.collection_exists():
#             self._connect_to_collection()
#             if self.verbose:
#                 print(f"✅ Auto-connected to existing collection: {self.collection_name}")
    
#     def _initialize_embeddings(self, model_name: str):
#         """Initialize HuggingFace embeddings"""
#         try:
#             self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
#             if self.verbose:
#                 print("✅ Embeddings initialized")
#         except Exception as e:
#             print(f"❌ Embeddings error: {e}")
#             raise
    
#     def _initialize_client(self):
#         """Initialize Qdrant client"""
#         try:
#             print("DEBUG: Qdrant URL =", self.qdrant_url)
#             print("DEBUG: Qdrant KEY =", self.qdrant_key)
#             print("DEBUG: COLLECTION_NAME =", self.collection_name)

#             self.client = QdrantClient(url=self.qdrant_url, api_key=self.qdrant_key)
#             self.client.get_collections()
#             if self.verbose:
#                 print("✅ Qdrant connected")
#         except Exception as e:
#             print(f"❌ Qdrant connection error: {e}")
#             raise
    
#     def collection_exists(self) -> bool:
#         """Check if collection exists in Qdrant"""
#         try:
#             collections = self.client.get_collections().collections
#             return any(c.name == self.collection_name for c in collections)
#         except:
#             return False
    
#     def _connect_to_collection(self):
#         """Connect to existing collection"""
#         if self.vectorstore is None:
#             try:
#                 self.vectorstore = Qdrant(
#                     client=self.client,
#                     collection_name=self.collection_name,
#                     embeddings=self.embeddings
#                 )
#                 if self.verbose:
#                     print(f"✅ Connected to collection: {self.collection_name}\n")
#             except Exception as e:
#                 print(f"❌ Error connecting: {e}")
#                 raise
    
#     def create_embeddings(
#         self,
#         chunks: List[Document],
#         force_recreate: bool = False
#     ) -> bool:
#         """Create embeddings in Qdrant"""
#         # Check if collection exists
#         if self.collection_exists():
#             if not force_recreate:
#                 if self.verbose:
#                     print("✅ Collection already exists. Skipping creation.")
#                 self._connect_to_collection()
#                 return False
#             else:
#                 if self.verbose:
#                     print("⚠️  Force recreate enabled. Deleting existing collection...")
        
#         if not chunks:
#             print("❌ No chunks to upload")
#             return False
        
#         if self.verbose:
#             print(f"⬆️  Uploading {len(chunks)} chunks to Qdrant...\n")
        
#         try:
#             self.vectorstore = Qdrant.from_documents(
#                 chunks,
#                 self.embeddings,
#                 url=self.qdrant_url,
#                 api_key=self.qdrant_key,
#                 collection_name=self.collection_name,
#                 force_recreate=True
#             )
#             if self.verbose:
#                 print("✅ Embeddings uploaded to Qdrant successfully!\n")
#             return True
#         except Exception as e:
#             print(f"❌ Error creating embeddings: {e}")
#             return False
    
#     def retrieve(self, query: str, top_k: int = 3) -> Dict:
#         """Retrieve relevant documents"""
#         if self.vectorstore is None:
#             if not self.collection_exists():
#                 raise RuntimeError("❌ Embeddings not found! Create embeddings first.")
#             self._connect_to_collection()
        
#         try:
#             results = self.vectorstore.similarity_search_with_score(query, k=top_k)
            
#             documents = []
#             projects = []
#             similarities = []
#             sources = []
#             keywords_list = []
            
#             for doc, score in results:
#                 documents.append(doc.page_content)
#                 projects.append(f"Project {doc.metadata.get('project_number', 'Unknown')}")
#                 sources.append(doc.metadata.get('source', 'Unknown'))
#                 keywords_list.append(doc.metadata.get('keywords', []))
#                 similarities.append(float(score))
            
#             return {
#                 'documents': documents,
#                 'projects': projects,
#                 'sources': sources,
#                 'keywords': keywords_list,
#                 'similarities': similarities
#             }
#         except Exception as e:
#             print(f"❌ Error retrieving: {e}")
#             raise




"""
Vector Store Management Module
"""
from typing import Dict, List, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchAny
from langchain_qdrant import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VectorStore:
    """Manages Qdrant vector store operations"""
    
    def __init__(
        self,
        qdrant_url: str,
        qdrant_key: str,
        collection_name: str,
        embedding_model: str,
        verbose: bool = True
    ):
        self.qdrant_url = os.getenv('QDRANT_URL')
        self.qdrant_key = os.getenv('QDRANT_API_KEY')
        self.collection_name = os.getenv('COLLECTION_NAME')
        self.embedding_model = os.getenv('EMBEDDING_MODEL')
        self.verbose = verbose

        # Initialize vectorstore attribute
        self.vectorstore = None
        
        # Initialize embeddings
        self._initialize_embeddings(self.embedding_model)
        
        # Initialize Qdrant client
        self._initialize_client()
        
        # Auto-connect if collection exists
        if self.collection_exists():
            self._connect_to_collection()
            if self.verbose:
                print(f"✅ Auto-connected to existing collection: {self.collection_name}")
    
    def _initialize_embeddings(self, model_name: str):
        """Initialize HuggingFace embeddings"""
        try:
            self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
            if self.verbose:
                print("✅ Embeddings initialized")
        except Exception as e:
            print(f"❌ Embeddings error: {e}")
            raise
    
    def _initialize_client(self):
        """Initialize Qdrant client"""
        try:
            if self.verbose:
                print("DEBUG: Qdrant URL =", self.qdrant_url)
                print("DEBUG: COLLECTION_NAME =", self.collection_name)

            self.client = QdrantClient(url=self.qdrant_url, api_key=self.qdrant_key)
            self.client.get_collections()
            if self.verbose:
                print("✅ Qdrant connected")
        except Exception as e:
            print(f"❌ Qdrant connection error: {e}")
            raise
    
    def collection_exists(self) -> bool:
        """Check if collection exists in Qdrant"""
        try:
            collections = self.client.get_collections().collections
            return any(c.name == self.collection_name for c in collections)
        except:
            return False
    
    def _connect_to_collection(self):
        """Connect to existing collection"""
        if self.vectorstore is None:
            try:
                self.vectorstore = Qdrant(
                    client=self.client,
                    collection_name=self.collection_name,
                    embeddings=self.embeddings
                )
                if self.verbose:
                    print(f"✅ Connected to collection: {self.collection_name}\n")
            except Exception as e:
                print(f"❌ Error connecting: {e}")
                raise
    
    def create_embeddings(
        self,
        chunks: List[Document],
        force_recreate: bool = False
    ) -> bool:
        """Create embeddings in Qdrant"""
        # Check if collection exists
        if self.collection_exists():
            if not force_recreate:
                if self.verbose:
                    print("✅ Collection already exists. Skipping creation.")
                self._connect_to_collection()
                return False
            else:
                if self.verbose:
                    print("⚠️  Force recreate enabled. Deleting existing collection...")
        
        if not chunks:
            print("❌ No chunks to upload")
            return False
        
        if self.verbose:
            print(f"⬆️  Uploading {len(chunks)} chunks to Qdrant...\n")
        
        try:
            self.vectorstore = Qdrant.from_documents(
                chunks,
                self.embeddings,
                url=self.qdrant_url,
                api_key=self.qdrant_key,
                collection_name=self.collection_name,
                force_recreate=True
            )
            if self.verbose:
                print("✅ Embeddings uploaded to Qdrant successfully!\n")
            return True
        except Exception as e:
            print(f"❌ Error creating embeddings: {e}")
            return False
    
    def retrieve(
        self, 
        query: str, 
        top_k: int = 3,
        project_types: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None
    ) -> Dict:
        """
        Retrieve relevant documents with optional metadata filtering
        
        Args:
            query: Search query
            top_k: Number of results to return
            project_types: Filter by project types (e.g., ["Healthcare AI", "Financial Analytics"])
            keywords: Filter by keywords (e.g., ["machine learning", "data pipeline"])
        """
        if self.vectorstore is None:
            if not self.collection_exists():
                raise RuntimeError("❌ Embeddings not found! Create embeddings first.")
            self._connect_to_collection()
        
        try:
            # Build Qdrant filter if metadata filters are provided
            search_kwargs = {"k": top_k}
            
            if project_types or keywords:
                filter_conditions = []
                
                if project_types:
                    filter_conditions.append(
                        FieldCondition(
                            key="metadata.project_type",
                            match=MatchAny(any=project_types)
                        )
                    )
                
                if keywords:
                    filter_conditions.append(
                        FieldCondition(
                            key="metadata.keywords",
                            match=MatchAny(any=keywords)
                        )
                    )
                
                # Apply filter
                search_kwargs["filter"] = Filter(must=filter_conditions)
                
                if self.verbose:
                    print(f"🔍 Applying filters: project_types={project_types}, keywords={keywords}")
            
            results = self.vectorstore.similarity_search_with_score(query, **search_kwargs)
            
            documents = []
            projects = []
            similarities = []
            sources = []
            project_types_list = []
            keywords_list = []
            
            for doc, score in results:
                documents.append(doc.page_content)
                projects.append(f"Project {doc.metadata.get('project_number', 'Unknown')}")
                sources.append(doc.metadata.get('source', 'Unknown'))
                project_types_list.append(doc.metadata.get('project_type', 'Unknown'))
                keywords_list.append(doc.metadata.get('keywords', []))
                similarities.append(float(score))
            
            return {
                'documents': documents,
                'projects': projects,
                'sources': sources,
                'project_types': project_types_list,
                'keywords': keywords_list,
                'similarities': similarities
            }
        except Exception as e:
            print(f"❌ Error retrieving: {e}")
            raise