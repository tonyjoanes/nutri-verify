# NutriVerify

NutriVerify is an AI-powered platform designed to analyze scientific nutrition research and fact-check dietary claims. The platform combines cutting-edge AI technology with evidence-based nutrition science to help users make informed decisions about diet and nutrition.

## 🚀 Features

- Scientific paper analysis and data extraction
- Evidence-based claim verification
- Nutrition research database
- Social media claim fact-checking
- API access for researchers and healthcare professionals

## 🛠️ Tech Stack

- **Backend**: C# (.NET Core Web API)
- **Data Processing**: Python (AI/ML components)
- **Frontend**: React
- **Database**: [Your choice - e.g., PostgreSQL, SQL Server]
- **AI/ML**: Integration with LLMs for paper analysis and claim verification
- **Authentication**: [Your choice - e.g., JWT, OAuth]

## 📋 Prerequisites

- .NET 7.0 or later
- Python 3.8 or later
- Node.js 16.x or later
- [Database system]

## 🏗️ Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nutriverify.git
cd nutriverify
```

2. Set up the backend:
```bash
cd src/NutriVerify.Api
dotnet restore
dotnet build
```

3. Set up the Python environment:
```bash
cd ../python
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
pip install -r requirements.txt
```

4. Set up the frontend:
```bash
cd ../frontend
npm install
```

5. Configure your environment variables (create a `.env` file in each project root)

## 🚀 Running the Project

1. Start the backend:
```bash
cd src/NutriVerify.Api
dotnet run
```

2. Start the Python services:
```bash
cd src/python
python main.py
```

3. Start the frontend:
```bash
cd src/frontend
npm start
```

## 🧪 Testing

```bash
# Run backend tests
dotnet test

# Run Python tests
pytest

# Run frontend tests
npm test
```

## 📦 Project Structure

```
nutriverify/
├── src/
│   ├── NutriVerify.Api/     # C# Web API
│   ├── NutriVerify.Core/    # Core business logic
│   ├── NutriVerify.Data/    # Data access layer
│   ├── python/              # Python services
│   └── frontend/            # React frontend
└── tests/                   # Test projects
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- PubMed Central for research data access
- National Institutes of Health (NIH) databases
- USDA FoodData Central

## 📬 Contact

[Tony Joanes] - [tonyjoanes@outlook.com]

Project Link: https://github.com/tonyjoanes/nutriverify