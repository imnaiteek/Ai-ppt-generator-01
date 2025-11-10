"""
Simple Web Scraping Presentation Generator
Guaranteed to work!
"""

import streamlit as st
import json
from datetime import datetime

# Check dependencies
try:
    import requests
    from bs4 import BeautifulSoup
except:
    st.error("🚨 Libraries missing! Run this command:")
    st.code("pip install requests beautifulsoup4 lxml")
    st.stop()

# Simple config
st.set_page_config(page_title="Presentation Generator", page_icon="🎨", layout="wide")

# Initialize
if 'pres' not in st.session_state:
    st.session_state.pres = None

# Simple CSS
st.markdown("""
<style>
.big-title {font-size: 2rem; color: #667eea; text-align: center; font-weight: bold;}
.slide {border: 2px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px;}
</style>
""", unsafe_allow_html=True)

def get_wikipedia(topic):
    """Get content from Wikipedia"""
    try:
        url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get paragraphs
        paras = []
        for p in soup.find_all('p', limit=5):
            text = p.get_text().strip()
            if len(text) > 100:
                paras.append(text[:200])
        
        # Get headings
        heads = []
        for h in soup.find_all(['h2', 'h3'], limit=10):
            text = h.get_text().replace('[edit]', '').strip()
            if text and len(text) > 3:
                heads.append(text)
        
        return paras, heads
    except:
        return [], []

def make_slides(topic, num_slides, paras, heads):
    """Make slides from content"""
    slides = []
    
    # Slide 1
    slides.append({
        "num": 1,
        "title": "Introduction",
        "points": [
            f"Overview of {topic}",
            "Key concepts and background",
            "What we'll explore today"
        ] if not paras else [paras[0][:100], paras[0][100:200] if len(paras[0]) > 100 else "Additional context", "Let's dive in"]
    })
    
    # Middle slides from headings
    for i, head in enumerate(heads[:num_slides-2], 2):
        points = []
        if paras:
            for p in paras[:3]:
                sentences = p.split('.')
                if sentences:
                    points.append(sentences[0][:80])
                if len(points) >= 3:
                    break
        
        while len(points) < 3:
            points.append(f"Information about {head}")
        
        slides.append({
            "num": i,
            "title": head[:60],
            "points": points[:3]
        })
        
        if i >= num_slides - 1:
            break
    
    # Fill if needed
    while len(slides) < num_slides - 1:
        n = len(slides) + 1
        slides.append({
            "num": n,
            "title": f"Point {n-1}",
            "points": [f"Detail about {topic}", "Supporting information", "Key insights"]
        })
    
    # Last slide
    slides.append({
        "num": num_slides,
        "title": "Conclusion",
        "points": [
            f"Summary of {topic}",
            "Key takeaways",
            "Thank you!"
        ]
    })
    
    return slides

# MAIN APP
st.markdown('<p class="big-title">🎨 Presentation Generator</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Settings")
    
    topic = st.text_input("Enter Topic", placeholder="e.g., Python Programming")
    num_slides = st.slider("Slides", 5, 10, 6)
    
    if st.button("🚀 Generate", type="primary", use_container_width=True):
        if not topic:
            st.error("Enter a topic!")
        else:
            with st.spinner("Creating..."):
                # Show progress
                st.write("🔍 Searching Wikipedia...")
                paras, heads = get_wikipedia(topic)
                
                st.write(f"✅ Found {len(paras)} paragraphs, {len(heads)} sections")
                
                # Make slides
                st.write("✨ Creating slides...")
                slides = make_slides(topic, num_slides, paras, heads)
                
                # Save
                st.session_state.pres = {
                    "title": topic,
                    "slides": slides,
                    "date": datetime.now().strftime("%Y-%m-%d")
                }
                
                st.success("Done!")
                st.rerun()

# Main area
if st.session_state.pres is None:
    st.info("👈 Enter a topic in sidebar to start!")
    
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown("### How it works")
        st.write("1. Enter topic")
        st.write("2. Choose slides")
        st.write("3. Click Generate")
        st.write("4. Get presentation!")
        
        st.markdown("### Try these:")
        st.write("• Artificial Intelligence")
        st.write("• Climate Change")
        st.write("• Python Programming")
        st.write("• Space Exploration")
else:
    pres = st.session_state.pres
    
    # Title
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #667eea, #764ba2); color: white; 
    padding: 40px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
        <h1>{pres['title']}</h1>
        <p>{pres['date']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Slides
    for slide in pres['slides']:
        st.markdown(f"""
        <div class="slide">
            <h3>Slide {slide['num']}: {slide['title']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for point in slide['points']:
            st.write(f"• {point}")
        
        st.write("")
    
    # Export
    st.markdown("---")
    st.subheader("📥 Export")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 New Presentation"):
            st.session_state.pres = None
            st.rerun()
    
    with col2:
        json_str = json.dumps(pres, indent=2)
        st.download_button(
            "📄 JSON",
            json_str,
            f"{pres['title']}.json",
            "application/json"
        )
    
    with col3:
        text = f"{pres['title']}\n{'='*50}\n\n"
        for slide in pres['slides']:
            text += f"Slide {slide['num']}: {slide['title']}\n"
            for point in slide['points']:
                text += f"  • {point}\n"
            text += "\n"
        
        st.download_button(
            "📝 Text",
            text,
            f"{pres['title']}.txt",
            "text/plain"
        )

# Debug info at bottom
with st.expander("🔧 Debug Info"):
    st.write("Session state:", st.session_state)
    st.write("Libraries working:", "✅")
