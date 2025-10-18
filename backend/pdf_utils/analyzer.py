"""
PDF Analyzer - Clean analysis logic moved from services
"""

import time
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


async def analyze_with_openai(text: str) -> str:
    """Analyze resume text using OpenAI GPT with predefined comprehensive analysis"""
    start_time = time.time()
    logger.info(f"🤖 Starting OpenAI analysis - Text length: {len(text)} chars")
    
    try:
        if not settings.openai_api_key or not settings.openai_client:
            logger.error("❌ OpenAI API key not configured")
            return "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        
        # Prepare prompt
        prompt_start = time.time()
        resume_analysis_prompt = f"""
Analyze this resume/CV document and provide a comprehensive structured analysis:

### 1. PERSONAL INFORMATION
- Full Name
- Contact Information (Phone, Email, Location)
- Professional Title/Position
- LinkedIn/Portfolio URLs

### 2. PROFESSIONAL SUMMARY
- Career level (Entry/Mid/Senior)
- Years of experience
- Key areas of expertise
- Professional strengths

### 3. WORK EXPERIENCE
For each position:
- Company Name & Position Title
- Employment Duration
- Key Responsibilities
- Notable Achievements (with quantifiable results)
- Technologies/Tools Used

### 4. EDUCATION
- Degree(s) & Institution(s)
- Graduation Date(s)
- GPA (if mentioned)
- Relevant Coursework
- Academic Honors/Awards

### 5. TECHNICAL SKILLS
- Programming Languages
- Frameworks/Libraries
- Databases
- Cloud Platforms
- Development Tools

### 6. SOFT SKILLS
- Leadership abilities
- Communication skills
- Problem-solving capabilities
- Teamwork experience

### 7. LANGUAGES
- Language name and proficiency level

### 8. PROJECTS (if applicable)
- Project Name, Duration, Technologies, Description, Role, Impact

### 9. CERTIFICATIONS & ACHIEVEMENTS
- Certifications, Awards, Publications

### 10. ADDITIONAL INFORMATION
- Volunteer Work, Professional Memberships, Conferences

Document Content:
{text}

Provide a detailed analysis in the format above. If any section is not present, mention "Not specified". Focus on extracting factual information and highlighting standout qualifications.
"""
        prompt_time = time.time() - prompt_start
        logger.info(f"📝 Prompt prepared in {prompt_time:.2f}s - Length: {len(resume_analysis_prompt)} chars")
        
        # Make API call
        api_start = time.time()
        logger.info("🌐 Making OpenAI API call...")
        
        response = settings.openai_client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "You are an expert HR professional and resume analyst. Provide detailed, structured analysis of resumes in a clear, organized format."},
                {"role": "user", "content": resume_analysis_prompt}
            ],
            max_tokens=settings.max_tokens,
            temperature=settings.temperature
        )
        
        api_time = time.time() - api_start
        total_time = time.time() - start_time
        
        response_text = response.choices[0].message.content
        logger.info(f"✅ OpenAI API call completed in {api_time:.2f}s")
        logger.info(f"📊 Response length: {len(response_text)} chars")
        logger.info(f"🏁 Total OpenAI analysis time: {total_time:.2f}s")
        
        return response_text
        
    except Exception as e:
        error_time = time.time() - start_time
        logger.error(f"❌ OpenAI analysis failed after {error_time:.2f}s: {str(e)}")
        return f"OpenAI analysis failed: {str(e)}. Please check your API key and network connection."