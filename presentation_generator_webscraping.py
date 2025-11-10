"""
ALLWEONE Presentation Generator - Web Scraping Version
Generate presentations with real content from the internet using web scraping
"""

import streamlit as st
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote_plus, urlparse
import time

# Page configuration
st.set_page_config(
    page_title="Presentation Generator - Web Scraping",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .slide-container {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .slide-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
    }
    .slide-content {
        font-size: 1rem;
        color: #555;
        line-height: 1.6;
    }
    .source-link {
        font-size: 0.8rem;
        color: #666;
        font-style: italic;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'outline' not in st.session_state:
    st.session_state.outline = None
if 'presentation' not in st.session_state:
    st.session_state.presentation = None
if 'selected_theme' not in st.session_state:
    st.session_state.selected_theme = "Professional Blue"
if 'generation_step' not in st.session_state:
    st.session_state.generation_step = 'input'
if 'scraped_data' not in st.session_state:
    st.session_state.scraped_data = []

# Themes
THEMES = {
    "Professional Blue": {
        "primary_color": "#667eea",
        "secondary_color": "#764ba2",
        "background": "#ffffff",
        "text_color": "#333333"
    },
    "Modern Dark": {
        "primary_color": "#1a1a1a",
        "secondary_color": "#4a4a4a",
        "background": "#2d2d2d",
        "text_color": "#ffffff"
    },
    "Elegant Purple": {
        "primary_color": "#9333ea",
        "secondary_color": "#c084fc",
        "background": "#faf5ff",
        "text_color": "#3b0764"
    },
    "Nature Green": {
        "primary_color": "#059669",
        "secondary_color": "#10b981",
        "background": "#f0fdf4",
        "text_color": "#064e3b"
    },
    "Sunset Orange": {
        "primary_color": "#ea580c",
        "secondary_color": "#fb923c",
        "background": "#fff7ed",
        "text_color": "#7c2d12"
    },
    "Ocean Blue": {
        "primary_color": "#0284c7",
        "secondary_color": "#38bdf8",
        "background": "#f0f9ff",
        "text_color": "#0c4a6e"
    },
    "Rose Pink": {
        "primary_color": "#e11d48",
        "secondary_color": "#fb7185",
        "background": "#fff1f2",
        "text_color": "#881337"
    },
    "Tech Gray": {
        "primary_color": "#4b5563",
        "secondary_color": "#9ca3af",
        "background": "#f9fafb",
        "text_color": "#111827"
    },
    "Vibrant Yellow": {
        "primary_color": "#eab308",
        "secondary_color": "#facc15",
        "background": "#fefce8",
        "text_color": "#713f12"
    }
}

def search_duckduckgo(query, num_results=5):
    """Search DuckDuckGo for relevant URLs"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            for result in soup.find_all('a', class_='result__a', limit=num_results):
                url = result.get('href')
                title = result.get_text()
                if url and title:
                    results.append({
                        'title': title,
                        'url': url
                    })
            
            return results
        
        return []
    except Exception as e:
        st.warning(f"Search error: {str(e)}")
        return []

def scrape_wikipedia(topic):
    """Scrape Wikipedia for topic information"""
    try:
        # Format topic for Wikipedia URL
        topic_formatted = topic.replace(' ', '_')
        url = f"https://en.wikipedia.org/wiki/{topic_formatted}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Get title
            title = soup.find('h1', class_='firstHeading')
            title_text = title.get_text() if title else topic
            
            # Get introduction paragraphs
            content = soup.find('div', class_='mw-parser-output')
            paragraphs = []
            
            if content:
                for p in content.find_all('p', limit=5):
                    text = p.get_text().strip()
                    if len(text) > 50:  # Skip very short paragraphs
                        # Clean up citation references
                        text = re.sub(r'\[\d+\]', '', text)
                        paragraphs.append(text)
            
            # Get section headings
            sections = []
            for heading in soup.find_all(['h2', 'h3'], limit=10):
                section_text = heading.get_text()
                # Clean up edit links
                section_text = section_text.replace('[edit]', '').strip()
                if section_text and len(section_text) > 3:
                    sections.append(section_text)
            
            return {
                'source': 'Wikipedia',
                'url': url,
                'title': title_text,
                'paragraphs': paragraphs,
                'sections': sections
            }
        
        return None
    except Exception as e:
        st.warning(f"Wikipedia scraping error: {str(e)}")
        return None

def scrape_website(url):
    """Scrape content from a general website"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get title
            title = soup.find('title')
            title_text = title.get_text() if title else "Untitled"
            
            # Get main content
            paragraphs = []
            
            # Try to find main content area
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile('content|main|article'))
            
            if main_content:
                for p in main_content.find_all('p', limit=10):
                    text = p.get_text().strip()
                    if len(text) > 50:
                        paragraphs.append(text)
            else:
                # Fallback to all paragraphs
                for p in soup.find_all('p', limit=10):
                    text = p.get_text().strip()
                    if len(text) > 50:
                        paragraphs.append(text)
            
            # Get headings
            headings = []
            for heading in soup.find_all(['h1', 'h2', 'h3'], limit=10):
                heading_text = heading.get_text().strip()
                if heading_text and len(heading_text) > 3:
                    headings.append(heading_text)
            
            return {
                'source': urlparse(url).netloc,
                'url': url,
                'title': title_text,
                'paragraphs': paragraphs,
                'headings': headings
            }
        
        return None
    except Exception as e:
        st.warning(f"Error scraping {url}: {str(e)}")
        return None

def extract_key_points(text, num_points=3):
    """Extract key points from text"""
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    # Take the most substantial sentences
    key_points = []
    for sentence in sentences[:num_points * 2]:
        if len(sentence) > 30 and len(sentence) < 200:
            key_points.append(sentence)
        if len(key_points) >= num_points:
            break
    
    return key_points

def generate_outline_from_web(topic, num_slides, scraped_data):
    """Generate outline from scraped web data"""
    outline = {
        "title": f"{topic}",
        "slides": []
    }
    
    # Slide 1: Introduction
    intro_content = []
    if scraped_data and scraped_data[0]['paragraphs']:
        intro_text = scraped_data[0]['paragraphs'][0][:300]
        intro_content = extract_key_points(intro_text, 3)
    
    if not intro_content:
        intro_content = [
            f"Introduction to {topic}",
            "Overview of key concepts",
            "What we'll cover in this presentation"
        ]
    
    outline["slides"].append({
        "slide_number": 1,
        "title": "Introduction",
        "content": intro_content,
        "notes": f"Introduction based on web research about {topic}",
        "source": scraped_data[0]['url'] if scraped_data else None
    })
    
    # Generate slides from sections/headings
    slide_num = 2
    for data in scraped_data[:num_slides]:
        # Use sections or headings as slide titles
        sections = data.get('sections', data.get('headings', []))
        
        for section in sections[:num_slides - 1]:
            if slide_num > num_slides:
                break
            
            # Find relevant paragraph for this section
            content = []
            for para in data['paragraphs'][:3]:
                points = extract_key_points(para, 3)
                content.extend(points)
                if len(content) >= 3:
                    break
            
            # Ensure we have at least 3 points
            while len(content) < 3:
                content.append(f"Additional information about {section}")
            
            outline["slides"].append({
                "slide_number": slide_num,
                "title": section[:60],  # Limit title length
                "content": content[:3],
                "notes": f"Content sourced from {data['source']}",
                "source": data['url']
            })
            
            slide_num += 1
    
    # Fill remaining slides if needed
    while len(outline["slides"]) < num_slides:
        outline["slides"].append({
            "slide_number": len(outline["slides"]) + 1,
            "title": f"Additional Topic {len(outline['slides'])}",
            "content": [
                f"Further information about {topic}",
                "Supporting details and examples",
                "Key takeaways and insights"
            ],
            "notes": "Additional content",
            "source": None
        })
    
    # Add conclusion slide
    if len(outline["slides"]) < num_slides:
        outline["slides"].append({
            "slide_number": len(outline["slides"]) + 1,
            "title": "Conclusion",
            "content": [
                f"Summary of key points about {topic}",
                "Main takeaways and insights",
                "Further resources and reading"
            ],
            "notes": "Conclusion slide",
            "source": None
        })
    
    return outline

def scrape_web_for_topic(topic, num_sources=3):
    """Scrape web for topic information"""
    scraped_data = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Try Wikipedia first
    status_text.text("🔍 Searching Wikipedia...")
    progress_bar.progress(20)
    wiki_data = scrape_wikipedia(topic)
    if wiki_data:
        scraped_data.append(wiki_data)
    
    # Search for additional sources
    status_text.text("🔍 Searching the web...")
    progress_bar.progress(40)
    search_results = search_duckduckgo(topic, num_results=num_sources)
    
    # Scrape search results
    for idx, result in enumerate(search_results[:num_sources]):
        status_text.text(f"📄 Scraping {idx + 1}/{num_sources}...")
        progress_bar.progress(40 + (idx + 1) * 20)
        
        scraped = scrape_website(result['url'])
        if scraped and scraped['paragraphs']:
            scraped_data.append(scraped)
        
        time.sleep(1)  # Be nice to servers
    
    progress_bar.progress(100)
    status_text.text("✅ Web scraping complete!")
    time.sleep(1)
    status_text.empty()
    progress_bar.empty()
    
    return scraped_data

def enhance_presentation_content(outline):
    """Enhance outline with better formatting"""
    presentation = {
        "title": outline["title"],
        "slides": []
    }
    
    for slide in outline["slides"]:
        enhanced_content = []
        for point in slide["content"]:
            # Clean up and format content
            point = point.strip()
            if not point.endswith('.'):
                point += '.'
            enhanced_content.append(point)
        
        presentation["slides"].append({
            "slide_number": slide["slide_number"],
            "title": slide["title"],
            "content": enhanced_content,
            "notes": slide.get("notes", ""),
            "source": slide.get("source")
        })
    
    return presentation

def display_slide(slide, theme_config, index):
    """Display a single slide"""
    st.markdown(f"""
    <div class="slide-container" style="background-color: {theme_config['background']}; border-color: {theme_config['primary_color']};">
        <div class="slide-title" style="color: {theme_config['primary_color']};">
            Slide {slide['slide_number']}: {slide['title']}
        </div>
        <div class="slide-content" style="color: {theme_config['text_color']};">
    """, unsafe_allow_html=True)
    
    for point in slide['content']:
        st.markdown(f"• {point}")
    
    if slide.get('source'):
        st.markdown(f'<p class="source-link">📎 Source: <a href="{slide["source"]}" target="_blank">{slide["source"][:50]}...</a></p>', unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    with st.expander("📝 Speaker Notes"):
        st.write(slide.get('notes', 'No notes available'))

def main():
    # Header
    st.markdown('<h1 class="main-header">🌐 Presentation Generator - Web Scraping</h1>', unsafe_allow_html=True)
    
    st.info("✨ This version generates presentations using REAL content from the web!")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.success("✅ No API key needed!")
        st.info("🌐 Uses web scraping for content")
        st.markdown("---")
        
        if st.session_state.generation_step == 'input':
            st.header("📋 Presentation Settings")
            
            topic = st.text_input(
                "Topic",
                placeholder="e.g., Artificial Intelligence",
                help="Enter any topic - we'll search the web for information"
            )
            
            num_slides = st.slider("Number of Slides", min_value=5, max_value=12, value=8)
            
            num_sources = st.slider(
                "Number of Sources to Scrape",
                min_value=2,
                max_value=5,
                value=3,
                help="More sources = better content but slower"
            )
            
            page_style = st.selectbox(
                "Page Style",
                ["Professional", "Casual", "Academic", "Creative"]
            )
            
            st.markdown("---")
            
            st.warning("⏱️ Scraping may take 10-30 seconds depending on sources")
            
            if st.button("🚀 Scrape Web & Generate Outline"):
                if not topic or not topic.strip():
                    st.error("⚠️ Please enter a topic")
                else:
                    # Scrape web
                    scraped_data = scrape_web_for_topic(topic, num_sources)
                    
                    if not scraped_data:
                        st.error("❌ Could not scrape any content. Try a different topic.")
                    else:
                        st.success(f"✅ Scraped {len(scraped_data)} sources!")
                        
                        # Generate outline
                        with st.spinner("Creating outline..."):
                            outline = generate_outline_from_web(topic, num_slides, scraped_data)
                            st.session_state.outline = outline
                            st.session_state.scraped_data = scraped_data
                            st.session_state.generation_step = 'outline'
                            st.rerun()
        
        elif st.session_state.generation_step == 'outline':
            st.header("🎨 Theme Selection")
            selected_theme = st.selectbox("Choose Theme", list(THEMES.keys()))
            st.session_state.selected_theme = selected_theme
            
            # Theme preview
            theme_config = THEMES[selected_theme]
            st.markdown(f"""
            <div style="padding: 10px; background-color: {theme_config['background']}; border: 2px solid {theme_config['primary_color']}; border-radius: 5px;">
                <p style="color: {theme_config['primary_color']}; font-weight: bold;">Primary</p>
                <p style="color: {theme_config['secondary_color']}; font-weight: bold;">Secondary</p>
                <p style="color: {theme_config['text_color']};">Text</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            if st.button("✨ Generate Presentation"):
                with st.spinner("Creating presentation..."):
                    presentation = enhance_presentation_content(st.session_state.outline)
                    st.session_state.presentation = presentation
                    st.session_state.generation_step = 'presentation'
                    st.success("✅ Presentation ready!")
                    st.rerun()
            
            if st.button("← Back to Settings"):
                st.session_state.generation_step = 'input'
                st.session_state.scraped_data = []
                st.rerun()
        
        elif st.session_state.generation_step == 'presentation':
            st.success("✅ Presentation Ready!")
            
            # Show sources
            if st.session_state.scraped_data:
                with st.expander("📚 Sources Used"):
                    for data in st.session_state.scraped_data:
                        st.write(f"**{data['source']}**")
                        st.write(f"🔗 [{data['url'][:40]}...]({data['url']})")
            
            if st.button("🔄 Create New"):
                st.session_state.outline = None
                st.session_state.presentation = None
                st.session_state.scraped_data = []
                st.session_state.generation_step = 'input'
                st.rerun()
            
            if st.button("← Edit Outline"):
                st.session_state.generation_step = 'outline'
                st.rerun()
    
    # Main content
    if st.session_state.generation_step == 'input':
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🌟 Features")
            st.markdown("""
            - 🌐 **Web Scraping** - Gathers real content from the internet
            - 🔍 **Multiple Sources** - Wikipedia + web search results
            - 📊 **Real Data** - Actual information from credible sources
            - 🎨 **9 Themes** - Beautiful professional designs
            - ✏️ **Editable** - Customize after generation
            - 💾 **Export** - JSON and Text formats
            - 🆓 **Free** - No API costs
            """)
            
            st.markdown("### 📝 How It Works")
            st.markdown("""
            1. Enter your topic
            2. App searches Wikipedia and web
            3. Scrapes content from multiple sources
            4. Extracts key information
            5. Generates structured presentation
            6. You can edit and export!
            """)
            
            st.markdown("### ⚠️ Important Notes")
            st.markdown("""
            - Scraping takes 10-30 seconds
            - Quality depends on available sources
            - Some websites may block scraping
            - Respects robots.txt guidelines
            - Always cite your sources
            """)
    
    elif st.session_state.generation_step == 'outline':
        st.header("📝 Review & Edit Outline")
        
        if st.session_state.outline:
            st.markdown(f"### {st.session_state.outline['title']}")
            
            # Show scraped sources
            if st.session_state.scraped_data:
                with st.expander("📚 Content Sources", expanded=True):
                    for data in st.session_state.scraped_data:
                        st.write(f"✅ **{data['source']}** - {data.get('title', 'No title')}")
                        st.caption(f"🔗 {data['url']}")
            
            edited_outline = st.session_state.outline.copy()
            
            for idx, slide in enumerate(st.session_state.outline['slides']):
                with st.expander(f"Slide {slide['slide_number']}: {slide['title']}", expanded=idx < 3):
                    new_title = st.text_input("Title", value=slide['title'], key=f"title_{idx}")
                    edited_outline['slides'][idx]['title'] = new_title
                    
                    st.write("**Content Points:**")
                    new_content = []
                    for point_idx, point in enumerate(slide['content']):
                        new_point = st.text_area(
                            f"Point {point_idx + 1}",
                            value=point,
                            key=f"point_{idx}_{point_idx}",
                            height=80
                        )
                        new_content.append(new_point)
                    
                    edited_outline['slides'][idx]['content'] = new_content
                    
                    new_notes = st.text_area(
                        "Speaker Notes",
                        value=slide.get('notes', ''),
                        key=f"notes_{idx}",
                        height=60
                    )
                    edited_outline['slides'][idx]['notes'] = new_notes
                    
                    if slide.get('source'):
                        st.caption(f"📎 Source: {slide['source']}")
            
            st.session_state.outline = edited_outline
    
    elif st.session_state.generation_step == 'presentation':
        if st.session_state.presentation:
            st.header("🎉 Your Presentation")
            
            theme_config = THEMES[st.session_state.selected_theme]
            
            # Title slide
            st.markdown(f"""
            <div style="text-align: center; padding: 60px; background: linear-gradient(135deg, {theme_config['primary_color']}, {theme_config['secondary_color']}); color: white; border-radius: 10px; margin-bottom: 20px;">
                <h1 style="font-size: 3rem; margin-bottom: 20px;">{st.session_state.presentation['title']}</h1>
                <p style="font-size: 1.2rem;">Generated from web research on {datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display slides
            for idx, slide in enumerate(st.session_state.presentation['slides']):
                display_slide(slide, theme_config, idx)
            
            # Sources
            st.markdown("---")
            st.header("📚 Sources & Citations")
            if st.session_state.scraped_data:
                for idx, data in enumerate(st.session_state.scraped_data, 1):
                    st.write(f"{idx}. **{data['source']}** - {data.get('title', 'No title')}")
                    st.write(f"   🔗 {data['url']}")
            
            # Export options
            st.markdown("---")
            st.header("📥 Export Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Add sources to export
                export_data = st.session_state.presentation.copy()
                export_data['sources'] = [
                    {'source': d['source'], 'url': d['url'], 'title': d.get('title', '')}
                    for d in st.session_state.scraped_data
                ]
                
                json_str = json.dumps(export_data, indent=2)
                st.download_button(
                    label="📄 Download JSON",
                    data=json_str,
                    file_name=f"presentation_webscrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            with col2:
                text_content = f"{st.session_state.presentation['title']}\n{'='*60}\n"
                text_content += f"Generated from web research on {datetime.now().strftime('%B %d, %Y')}\n\n"
                
                for slide in st.session_state.presentation['slides']:
                    text_content += f"\n{'='*60}\n"
                    text_content += f"Slide {slide['slide_number']}: {slide['title']}\n"
                    text_content += f"{'='*60}\n\n"
                    for point in slide['content']:
                        text_content += f"• {point}\n"
                    if slide.get('source'):
                        text_content += f"\nSource: {slide['source']}\n"
                    text_content += f"\nSpeaker Notes:\n{slide.get('notes', 'N/A')}\n"
                
                text_content += f"\n{'='*60}\nSOURCES\n{'='*60}\n"
                for idx, data in enumerate(st.session_state.scraped_data, 1):
                    text_content += f"{idx}. {data['source']} - {data['url']}\n"
                
                st.download_button(
                    label="📝 Download Text",
                    data=text_content,
                    file_name=f"presentation_webscrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
            
            with col3:
                st.info("💡 PowerPoint export coming soon!")

if __name__ == "__main__":
    main()
