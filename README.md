# 🚀 AI-Powered Offer Letter Generator

> **Intelligent offer letter generation powered by semantic search and AI**

An advanced HR automation tool that generates personalized offer letters by intelligently matching candidate data with company policies using vector embeddings and semantic search.

## ✨ Features

- 🤖 **AI-Powered Generation**: Natural language interface for generating offer letters
- 🔍 **Semantic Search**: ChromaDB with SentenceTransformer embeddings for intelligent policy matching
- 📄 **PDF Generation**: Professional offer letters with embedded policies and salary details
- 💬 **Chat Interface**: Intuitive conversational UI for easy interaction
- 📊 **Data Integration**: Seamless CSV employee data and PDF policy document processing
- ⚡ **Real-time Processing**: Fast generation with download links for both PDF and text formats

## 🏗️ Architecture

```
Frontend (Next.js + Vercel) → Backend (FastAPI) → ChromaDB → PDF and Text Generation
                                     ↓
                            Semantic Policy Matching
```

**Tech Stack:**
- **Frontend**: Next.js deployed on Vercel
- **Backend**: FastAPI (local development)
- **Vector Database**: ChromaDB with SentenceTransformer embeddings
- **PDF Generation**: Jinja2 templates + pdfkit
- **Data Sources**: Employee CSV + HR Policy PDFs

## 📁 Project Structure

```
agentic-letter-generator/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── generator/              # Letter generation logic
│   ├── embedding/              # Vector embedding handlers
│   ├── templates/              # Jinja2 offer letter templates
│   ├── parsing/                # Contains the parsing and chunker .py files
│   └── requirements.txt        # Python dependencies
│── frontend/
│   ├── src/app                 # Next.js source code
│   └── public/                 # Static assets
│── data/                   
│   │── employees/              # Data of the employees
│   │── policies/               # Company policies
│   └── sample/                 # Sample Policy
└── offers/                     # Storage space for the pdfs and text    
```

## 🚀 Quick Start

### Backend Setup (Local)

1. **Clone the repository**
   ```bash
   git clone https://github.com/frozenexplorer/agentic-letter-generator
   cd agentic-letter-generator/backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your data**
   - Place employee CSV file in `data/employees` directory
   - Add HR policy PDFs (Leave Policy, Travel Policy) to `data/policies` directory

4. **Start the FastAPI server**
   ```bash
   uvicorn main:app --reload
   ```
   
   Server will be available at `http://localhost:8000`

### Frontend (Vercel)

1. Just launch the [website](https://agentic-letter-generator.vercel.app/) 

## 💬 Usage Examples

### Chat Interface Commands

```
🗣️ User: "Generate offer for Martha Bennett"
🤖 AI: ✅ Offer letter generated successfully!
        📄 PDF Download: [link]
        📝 Text Download: [link]

🗣️ User: "Generate offer for John Smith"
🤖 AI: 🔄 Generating offer letter for John Smith...
        ❌ No employee found named "John Smith".

```


## 🧠 How Semantic Search Works

### 1. **Document Embedding**
```python
# HR policies are converted to vector embeddings
sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
policy_embeddings = model.encode(policy_documents)
```

### 2. **Query Processing**
```python
# User queries are embedded and matched against policy vectors
query_embedding = model.encode("Generate offer for John Smith")
similar_policies = chromadb.query(query_embedding, n_results=5)
```

### 3. **Context Assembly**
- Candidate data retrieved from CSV
- Relevant policies matched via cosine similarity
- Template populated with personalized information

### 4. **Generation Pipeline**
```
User Input → Embedding → Semantic Search → Data Retrieval → Template Rendering → PDF and Text Generation
```

## 🛠️ Development

### Local Development
```bash
# Backend (Terminal 1)
cd backend
uvicorn main:app --reload

# Frontend (Terminal 2)  
cd frontend
npm run dev
```

### Adding New Templates
1. Create Jinja2 template in `backend/templates/`
2. Update template selection logic in `generator/`
3. Test with sample candidate data

### Extending Policy Support
1. Add new policy PDFs to `data/policies` directory
2. Update embedding pipeline to include new documents
3. Modify template to incorporate new policy sections

## 📋 Requirements

### Backend Dependencies
```
fastapi>=0.104.1
uvicorn>=0.24.0
chromadb>=0.4.15
sentence-transformers>=2.2.2
jinja2>=3.1.2
pdfkit>=1.0.0
pandas>=2.1.3
python-multipart>=0.0.6
```

### System Requirements
- Python 3.8+
- Node.js 18+
- wkhtmltopdf (for PDF generation)


## 👨‍💻 Developer

**Built with ❤️ by [@frozenexplorer](https://github.com/frozenexplorer)**
