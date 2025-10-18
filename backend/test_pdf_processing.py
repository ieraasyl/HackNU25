#!/usr/bin/env python3
"""
PDF Processing Test Script for Dolphin ByteDance Integration

This script demonstrates how to send PDF files and receive data from ByteDance Dolphin.
"""

import os
import asyncio
import httpx
import json
from pathlib import Path

# Test PDF content (simple text-based PDF)
SAMPLE_PDF_CONTENT = """
Test Document for Analysis

This is a sample document that contains the following information:

1. Introduction
   This document serves as a test case for PDF processing capabilities.

2. Main Content
   - Key Point A: Important information about topic A
   - Key Point B: Critical details about topic B  
   - Key Point C: Essential facts about topic C

3. Data Analysis
   The document contains statistical information:
   - Revenue: $1,000,000
   - Growth: 25% year-over-year
   - Market Share: 15%

4. Conclusion
   Based on the analysis, the company shows strong performance indicators
   and positive growth trends.

Contact Information:
Email: test@example.com
Phone: +1-555-0123
"""

async def test_pdf_endpoints():
    """Test all PDF processing endpoints"""
    
    print("🔍 Testing PDF Processing with Dolphin ByteDance")
    print("=" * 60)
    
    # Check if server is running
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get("http://127.0.0.1:8001/api/v1/health")
            if response.status_code != 200:
                print("❌ Dolphin server not running on port 8001")
                print("💡 Start server with: python dolphin_server.py")
                return
            
            health_data = response.json()
            print(f"✅ Server Status: {health_data.get('status')}")
            print(f"🔑 API Key Configured: {health_data.get('api_key_configured')}")
            print(f"📄 PDF Support: {health_data.get('pdf_support')}")
            print()
            
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return
    
    # Create a sample PDF file for testing
    test_pdf_path = create_sample_pdf()
    
    if not test_pdf_path.exists():
        print("❌ Could not create test PDF file")
        return
    
    print(f"📄 Created test PDF: {test_pdf_path}")
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            
            # Test 1: Get PDF Metadata
            print("\n🔍 Test 1: Getting PDF Metadata")
            print("-" * 40)
            
            with open(test_pdf_path, 'rb') as pdf_file:
                files = {"file": ("test_document.pdf", pdf_file, "application/pdf")}
                response = await client.post(
                    "http://127.0.0.1:8001/api/v1/pdf-metadata",
                    files=files
                )
            
            if response.status_code == 200:
                metadata = response.json()
                print("✅ Metadata extraction successful!")
                print(f"📊 Metadata: {json.dumps(metadata['metadata'], indent=2)}")
                print(f"✔️  Validation: {metadata['validation']['valid']}")
            else:
                print(f"❌ Metadata extraction failed: {response.status_code}")
                print(f"Response: {response.text}")
            
            # Test 2: Analyze PDF
            print("\n📋 Test 2: PDF Analysis")
            print("-" * 40)
            
            with open(test_pdf_path, 'rb') as pdf_file:
                files = {"file": ("test_document.pdf", pdf_file, "application/pdf")}
                data = {
                    "analysis_prompt": "Please provide a detailed analysis of this business document, focusing on key metrics and insights.",
                    "extract_text": True
                }
                response = await client.post(
                    "http://127.0.0.1:8001/api/v1/analyze-pdf",
                    files=files,
                    data=data
                )
            
            if response.status_code == 200:
                analysis = response.json()
                print("✅ PDF analysis successful!")
                
                if analysis.get('success'):
                    print(f"📄 Pages: {analysis.get('metadata', {}).get('num_pages', 'N/A')}")
                    print(f"📏 Size: {analysis.get('metadata', {}).get('size_kb', 'N/A')} KB")
                    
                    if analysis.get('extracted_text'):
                        print(f"📝 Extracted Text: {analysis['extracted_text'][:200]}...")
                    
                    if analysis.get('analysis'):
                        print(f"🤖 AI Analysis: {analysis['analysis']}")
                    else:
                        print("⚠️  No AI analysis (likely missing API key)")
                else:
                    print(f"❌ Analysis failed: {analysis.get('error')}")
            else:
                print(f"❌ PDF analysis failed: {response.status_code}")
                print(f"Response: {response.text}")
            
            # Test 3: Ask Question about PDF
            print("\n❓ Test 3: Ask Question about PDF")
            print("-" * 40)
            
            with open(test_pdf_path, 'rb') as pdf_file:
                files = {"file": ("test_document.pdf", pdf_file, "application/pdf")}
                data = {
                    "question": "What are the key financial metrics mentioned in this document?",
                    "include_context": True
                }
                response = await client.post(
                    "http://127.0.0.1:8001/api/v1/ask-pdf",
                    files=files,
                    data=data
                )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ PDF question successful!")
                
                if result.get('success'):
                    print(f"❓ Question: {result['question']}")
                    print(f"🤖 Answer: {result.get('answer', 'No answer (likely missing API key)')}")
                    print(f"📄 Used Context: {result.get('used_context', False)}")
                else:
                    print(f"❌ Question failed: {result.get('error')}")
            else:
                print(f"❌ PDF question failed: {response.status_code}")
                print(f"Response: {response.text}")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    finally:
        # Clean up test file
        if test_pdf_path.exists():
            test_pdf_path.unlink()
            print(f"\n🗑️  Cleaned up test file: {test_pdf_path}")

def create_sample_pdf():
    """Create a sample PDF file for testing"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        
        # Create PDF file
        test_pdf_path = Path("test_document.pdf")
        doc = SimpleDocTemplate(str(test_pdf_path), pagesize=letter)
        
        # Create content
        styles = getSampleStyleSheet()
        story = []
        
        for line in SAMPLE_PDF_CONTENT.strip().split('\n'):
            if line.strip():
                if line.strip().startswith(('1.', '2.', '3.', '4.')):
                    story.append(Paragraph(line, styles['Heading2']))
                else:
                    story.append(Paragraph(line, styles['Normal']))
                story.append(Spacer(1, 6))
        
        doc.build(story)
        return test_pdf_path
        
    except ImportError:
        print("📦 reportlab not installed, creating simple text file as PDF simulation...")
        # Create a text file as fallback (won't be a real PDF but good for basic testing)
        test_pdf_path = Path("test_document.txt")
        with open(test_pdf_path, 'w') as f:
            f.write(SAMPLE_PDF_CONTENT)
        return test_pdf_path

async def demonstrate_direct_api():
    """Demonstrate direct API usage without server"""
    
    print("\n🔧 Direct API Usage Demo")
    print("=" * 60)
    
    try:
        # Import PDF processor
        from dolphin.pdf_processor import PDFProcessor
        from dolphin.service import get_dolphin_service
        
        # Create sample content as bytes (simulating PDF)
        sample_content = SAMPLE_PDF_CONTENT.encode('utf-8')
        
        print("📄 Testing PDF processor directly...")
        
        # Test metadata extraction
        metadata = PDFProcessor.get_pdf_metadata(sample_content)
        print(f"📊 Metadata: {json.dumps(metadata, indent=2)}")
        
        # Test validation
        validation = PDFProcessor.validate_pdf(sample_content)
        print(f"✔️  Validation: {validation}")
        
        # Test with service (if API key available)
        api_key = os.getenv("DOLPHIN_API_KEY")
        if api_key:
            print("\n🤖 Testing with Dolphin service...")
            service = get_dolphin_service()
            
            # This would work with a real PDF, but our sample is just text
            # result = await service.analyze_pdf(sample_content)
            # print(f"Analysis: {result}")
            print("📝 Service available - would analyze real PDF files")
        else:
            print("⚠️  No API key - skipping AI analysis")
            
    except Exception as e:
        print(f"❌ Direct API demo failed: {e}")

def show_usage_examples():
    """Show usage examples for PDF processing"""
    
    print("\n📚 PDF Processing Usage Examples")
    print("=" * 60)
    
    examples = {
        "Upload and Analyze PDF": """
curl -X POST "http://127.0.0.1:8001/api/v1/analyze-pdf" \\
  -H "accept: application/json" \\
  -H "Content-Type: multipart/form-data" \\
  -F "file=@document.pdf" \\
  -F "analysis_prompt=Summarize the key points" \\
  -F "extract_text=true"
        """,
        
        "Ask Question about PDF": """
curl -X POST "http://127.0.0.1:8001/api/v1/ask-pdf" \\
  -H "accept: application/json" \\
  -H "Content-Type: multipart/form-data" \\
  -F "file=@document.pdf" \\
  -F "question=What are the main conclusions?" \\
  -F "include_context=true"
        """,
        
        "Get PDF Metadata": """
curl -X POST "http://127.0.0.1:8001/api/v1/pdf-metadata" \\
  -H "accept: application/json" \\
  -H "Content-Type: multipart/form-data" \\
  -F "file=@document.pdf"
        """,
        
        "Python Direct Usage": """
from dolphin.service import get_dolphin_service

# Load PDF file
with open('document.pdf', 'rb') as f:
    pdf_content = f.read()

# Analyze PDF
service = get_dolphin_service(api_key="your-key")
result = await service.analyze_pdf(pdf_content)
print(result['analysis'])

# Ask question
question_result = await service.ask_about_pdf(
    pdf_content, 
    "What are the key findings?"
)
print(question_result['answer'])
        """
    }
    
    for title, example in examples.items():
        print(f"\n📝 {title}:")
        print(example.strip())
    
    print(f"\n🌐 Interactive API Documentation:")
    print("http://127.0.0.1:8001/docs")

if __name__ == "__main__":
    print("🐬 Dolphin ByteDance PDF Processing Test Suite")
    print("=" * 70)
    
    # Check if API key is configured
    api_key = os.getenv("DOLPHIN_API_KEY")
    if not api_key:
        print("⚠️  DOLPHIN_API_KEY not configured")
        print("   Set it with: export DOLPHIN_API_KEY='your-key'")
        print("   PDF processing will work but AI analysis will be limited\n")
    else:
        print("✅ DOLPHIN_API_KEY configured\n")
    
    print("Choose test mode:")
    print("1. 🌐 Test API endpoints (requires running server)")
    print("2. 🔧 Direct API usage demo")
    print("3. 📚 Show usage examples")
    print("4. 🚀 Run all tests")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        asyncio.run(test_pdf_endpoints())
    elif choice == "2":
        asyncio.run(demonstrate_direct_api())
    elif choice == "3":
        show_usage_examples()
    elif choice == "4":
        asyncio.run(test_pdf_endpoints())
        asyncio.run(demonstrate_direct_api())
        show_usage_examples()
    else:
        print("❌ Invalid choice")
        show_usage_examples()