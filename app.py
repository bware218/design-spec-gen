#!/usr/bin/env python3
import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

def fetch_website_content(url):
    """Fetch and parse website content"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        st.error(f"Error fetching website: {str(e)}")
        return None

def extract_design_elements(soup, url):
    """Extract key design elements from the website"""
    if not soup:
        return {}
    
    # Extract navigation items
    nav_items = []
    nav_elements = soup.find_all(['nav', 'header'])
    for nav in nav_elements:
        links = nav.find_all('a')
        nav_items.extend([link.get_text().strip() for link in links if link.get_text().strip()])
    
    # Extract headings
    headings = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3']) if h.get_text().strip()]
    
    # Extract colors from CSS (basic)
    colors = []
    styles = soup.find_all('style')
    for style in styles:
        if style.string:
            color_matches = re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}', style.string)
            colors.extend(color_matches)
    
    # Extract button text
    buttons = [btn.get_text().strip() for btn in soup.find_all(['button', 'input']) if btn.get_text().strip()]
    
    return {
        'nav_items': nav_items[:10],  # Limit to first 10
        'headings': headings[:5],     # Limit to first 5
        'colors': list(set(colors))[:5],  # Unique colors, limit to 5
        'buttons': buttons[:5],       # Limit to first 5
        'title': soup.title.string if soup.title else 'Website'
    }

def generate_fun_facts(soup, url):
    """Generate interesting facts about the website"""
    if not soup:
        return "Unable to analyze website content."
    
    facts = []
    
    # Domain analysis
    from urllib.parse import urlparse
    domain = urlparse(url).netloc.replace('www.', '')
    facts.append(f"Domain: {domain}")
    
    # Page structure analysis
    total_links = len(soup.find_all('a'))
    if total_links > 0:
        facts.append(f"Contains {total_links} links")
    
    total_images = len(soup.find_all('img'))
    if total_images > 0:
        facts.append(f"Features {total_images} images")
    
    # Content analysis
    paragraphs = len(soup.find_all('p'))
    if paragraphs > 0:
        facts.append(f"Has {paragraphs} content paragraphs")
    
    # Technical insights
    if soup.find('meta', attrs={'name': 'viewport'}):
        facts.append("Mobile-optimized design")
    
    if soup.find_all(['script']):
        facts.append("Uses JavaScript for interactivity")
    
    # SEO elements
    if soup.find('meta', attrs={'name': 'description'}):
        facts.append("SEO-optimized with meta descriptions")
    
    return " • ".join(facts[:6]) if facts else "Clean, minimal website structure"

def generate_design_prompt(url, elements):
    """Generate design prompt based on extracted elements"""
    
    nav_section = f"- Navigation structure: {', '.join(elements['nav_items'][:8])}" if elements['nav_items'] else "- Clean navigation architecture"
    
    color_section = f"- Color palette: {', '.join(elements['colors'])}" if elements['colors'] else "- Sophisticated color scheme"
    
    button_section = f"- Interactive elements: {', '.join(elements['buttons'])}" if elements['buttons'] else "- Strategic call-to-action placement"
    
    prompt = f"""**PROFESSIONAL WEBSITE DESIGN SPECIFICATION**

**PROJECT OVERVIEW:**
Create a sophisticated website inspired by the design patterns and user experience of {elements['title']}.

**LAYOUT & ARCHITECTURE:**
{nav_section}
- Premium homepage layout with clear hierarchy
- Responsive grid system optimized for all devices
- Strategic content organization and flow
- Professional footer with essential information

**TYPOGRAPHY SYSTEM:**
- Modern, clean typeface selection
- Structured heading hierarchy (H1, H2, H3)
- Optimized readability and line spacing
- Consistent font weights and styling

**VISUAL DESIGN:**
{color_section}
- High-contrast elements for accessibility
- Consistent brand application throughout
- Subtle visual accents and highlights

**USER EXPERIENCE:**
- Intuitive navigation and user flow
- Strategic white space utilization
- Professional micro-interactions
- Seamless responsive behavior

**INTERACTIVE ELEMENTS:**
{button_section}
- Refined hover states and transitions
- Mobile-first responsive design
- Smooth animations and feedback
- Conversion-optimized user journey

**CONTENT STRATEGY:**
- Well-structured information architecture
- Strategic call-to-action placement
- Clear value proposition communication
- Mobile-optimized content presentation

**TECHNICAL REQUIREMENTS:**
Build as a modern, high-performance website optimized for user experience, accessibility, and conversion goals.

**REFERENCE SOURCE:** {url}

**IMPLEMENTATION READY:** Use this specification with AI design tools for professional results.
"""
    
    return prompt

# Streamlit App
st.set_page_config(
    page_title="PlayBook Pro - Design Intelligence", 
    page_icon="⬛",
    layout="wide"
)

# Custom CSS for luxury monochrome theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #000000 0%, #333333 100%);
        padding: 3rem;
        border-radius: 0;
        margin-bottom: 3rem;
        text-align: center;
        color: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        border-bottom: 1px solid #e0e0e0;
    }
    .luxury-card {
        background: #ffffff;
        padding: 2rem;
        border-radius: 0;
        border: 1px solid #e0e0e0;
        margin: 2rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    .champion-text {
        font-size: 2.5rem;
        font-weight: 300;
        letter-spacing: 2px;
        margin-bottom: 1rem;
        color: white;
    }
    .tagline {
        font-size: 1.1rem;
        opacity: 0.8;
        margin-bottom: 2rem;
        font-weight: 300;
        letter-spacing: 1px;
    }
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    .stat-box {
        text-align: center;
        padding: 1.5rem;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 0;
        min-width: 140px;
    }
    .stat-number {
        font-size: 1.5rem;
        font-weight: 300;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    .stat-label {
        font-size: 0.85rem;
        opacity: 0.7;
        font-weight: 300;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .fun-facts {
        background: #f8f8f8;
        padding: 1.5rem;
        border-left: 3px solid #000000;
        margin: 2rem 0;
        font-style: italic;
        color: #333333;
    }
    .stButton > button {
        background: #000000;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 300;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: #333333;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# Main header with luxury monochrome theme
st.markdown("""
<div class="main-header">
    <div class="champion-text">PLAYBOOK PRO</div>
    <div class="tagline">Precision Website Analysis & Design Intelligence</div>
    <div class="stats-container">
        <div class="stat-box">
            <div class="stat-number">FAST</div>
            <div class="stat-label">Analysis</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">PRECISE</div>
            <div class="stat-label">Extraction</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">INSIGHTFUL</div>
            <div class="stat-label">Results</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="luxury-card">
    <h3 style="color: #000000; font-weight: 300; letter-spacing: 1px;">INTELLIGENT DESIGN ANALYSIS</h3>
    <p style="color: #666666; line-height: 1.6;">Transform any website into actionable design intelligence. 
    Our sophisticated analysis engine extracts design patterns and generates professional-grade prompts for AI design tools.</p>
</div>
""", unsafe_allow_html=True)

# URL input with luxury theme
st.markdown("### Analyze a Website")
url = st.text_input(
    "Enter website URL:", 
    placeholder="https://example.com",
    help="Enter any website URL for intelligent design analysis"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_button = st.button(
        "ANALYZE DESIGN", 
        type="primary",
        use_container_width=True
    )

if analyze_button and url:
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    with st.spinner("Analyzing website architecture..."):
        soup = fetch_website_content(url)
        elements = extract_design_elements(soup, url)
        prompt = generate_design_prompt(url, elements)
        fun_facts = generate_fun_facts(soup, url)
    
    st.success("Analysis complete. Design specification ready.")
    
    # Fun Facts section
    st.markdown(f"""
    <div class="fun-facts">
        <strong>Website Overview:</strong> {fun_facts}
    </div>
    """, unsafe_allow_html=True)
    
    # Display extracted elements
    with st.expander("Technical Analysis Details"):
        st.json(elements)
    
    # Display the prompt
    st.markdown("### Design Specification")
    st.text_area(
        "Professional design specification:", 
        prompt, 
        height=400,
        help="Copy this specification to AI design tools for implementation"
    )
    
    # Download button
    st.download_button(
        label="Download Specification",
        data=prompt,
        file_name=f"design_spec_{elements['title'].replace(' ', '_')}.txt",
        mime="text/plain",
        help="Save specification for future reference"
    )

st.markdown("---")
st.markdown("""
<div class="luxury-card">
    <h3 style="color: #000000; font-weight: 300; letter-spacing: 1px;">COMPATIBLE AI DESIGN TOOLS</h3>
    <p style="color: #666666; line-height: 1.8; margin-bottom: 1rem;">
    <strong>Professional Implementation:</strong> Copy your generated specification and implement with leading AI design platforms.
    </p>
    <p style="color: #333333; font-weight: 300; letter-spacing: 0.5px;">
    <strong>Recommended Tools:</strong> Figma AI • Replit Agent • Lovable • v0.dev • Claude Artifacts • Kiro
    </p>
    <p style="color: #666666; font-style: italic; margin-top: 1rem;">
    <strong>Professional Tip:</strong> Each specification is crafted for precision implementation across multiple AI platforms.
    </p>
</div>
""", unsafe_allow_html=True)
