# Django Constitution RAG System

A powerful **Retrieval-Augmented Generation (RAG)** system built with Django that allows users to upload Constitution PDFs and query them using AI-powered semantic search.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-v5.0.6-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🚀 Features

### Core RAG Functionality
- **PDF Processing**: Upload and extract text from Constitution PDFs using PyPDF2
- **Intelligent Chunking**: Split documents into manageable chunks using LangChain
- **Vector Embeddings**: Generate semantic embeddings using SentenceTransformers
- **Similarity Search**: Fast similarity search using FAISS (Facebook AI Similarity Search)
- **Contextual Answers**: Get relevant context snippets for your queries

### User Management
- **Custom Authentication**: Secure login, logout, and registration system
- **User-Specific Data**: Personal document libraries and query history
- **Protected Access**: All features require authentication

### Web Interface
- **Modern UI**: Responsive design with clean, intuitive interface
- **Document Management**: Upload, view, and manage your PDF documents
- **Query Interface**: Ask questions and get AI-powered answers
- **History Tracking**: View your previous queries and results

## 🛠️ Tech Stack

- **Backend**: Django 5.0.6
- **Database**: SQLite (development)
- **AI/ML**: 
  - SentenceTransformers (all-MiniLM-L6-v2)
  - FAISS for vector similarity search
  - LangChain for text processing
- **PDF Processing**: PyPDF2
- **Frontend**: HTML, CSS, Django Templates

## 📋 Prerequisites

- Python 3.8+
- pip package manager

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/django-constitution-rag.git
   cd django-constitution-rag
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv vrt
   
   # On Windows
   vrt\Scripts\activate
   
   # On Linux/Mac
   source vrt/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   cd ML
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:8000/`

## 🎯 Usage

1. **Register/Login**: Create an account or login to access the system
2. **Upload Documents**: Upload Constitution PDF files through the web interface
3. **Wait for Processing**: The system will automatically process and index your documents
4. **Query Documents**: Ask questions about the Constitution in natural language
5. **View Results**: Get relevant answers with source context from the documents
6. **History**: Review your previous queries and results

## 📁 Project Structure

```
├── ML/                          # Django project root
│   ├── ML/                      # Project configuration
│   │   ├── settings.py          # Django settings
│   │   ├── urls.py              # Main URL routing
│   │   └── wsgi.py              # WSGI configuration
│   ├── model/                   # RAG application
│   │   ├── models.py            # Database models
│   │   ├── views.py             # View functions
│   │   ├── urls.py              # App URL routing
│   │   ├── rag_processor.py     # Core RAG functionality
│   │   └── templates/           # HTML templates
│   ├── authentication/          # Authentication app
│   │   ├── views.py             # Auth views
│   │   ├── forms.py             # Custom forms
│   │   ├── urls.py              # Auth URLs
│   │   └── templates/           # Auth templates
│   └── manage.py                # Django management script
├── requirements.txt             # Python dependencies
├── CLAUDE.md                   # Development documentation
└── README.md                   # This file
```

## 🔑 Key Components

### RAG Processor (`ML/model/rag_processor.py`)
- Handles PDF text extraction
- Manages text chunking and embedding generation
- Implements similarity search functionality

### Models (`ML/model/models.py`)
- `Document`: Stores uploaded PDF information
- `DocumentChunk`: Individual text chunks with embeddings
- `Query`: User query history
- `RAGIndex`: FAISS index management

### Authentication System
- Custom user registration with extended fields
- Secure login/logout functionality
- User-specific data isolation

## 🚀 API Endpoints

- `/` - Home page with document list
- `/upload/` - Upload new documents
- `/query/` - Query interface
- `/history/` - Query history
- `/auth/login/` - User login
- `/auth/register/` - User registration
- `/auth/logout/` - User logout

## 🔒 Security Features

- User authentication required for all operations
- CSRF protection on all forms
- Secure file upload handling
- User data isolation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Django](https://djangoproject.com/) - Web framework
- [SentenceTransformers](https://www.sbert.net/) - Semantic embeddings
- [FAISS](https://faiss.ai/) - Similarity search
- [LangChain](https://langchain.com/) - Text processing
- [PyPDF2](https://pypdf2.readthedocs.io/) - PDF processing

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Built with ❤️ using Django and AI**