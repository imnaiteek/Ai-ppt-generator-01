# 🌐 Presentation Generator - Web Scraping Version

**Generate presentations with REAL content from the internet!**

## 🎯 Overview

This version scrapes actual content from the web to create presentations with real, current information. No API keys required!

## ✨ Key Features

- 🌐 **Web Scraping** - Gathers real content from multiple sources
- 🔍 **Wikipedia Integration** - Automatically searches Wikipedia first
- 🌎 **Multiple Sources** - Scrapes 2-5 different websites
- 📊 **Real Data** - Actual information, not templates
- 🎨 **9 Themes** - Professional designs
- 📎 **Source Citations** - Automatically tracks and cites sources
- ✏️ **Fully Editable** - Customize after generation
- 💾 **Export Options** - JSON and Text with sources
- 🆓 **100% Free** - No API costs

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements_webscraping.txt

# Run the app
streamlit run presentation_generator_webscraping.py
```

Open `http://localhost:8501` and start creating!

## 📋 How It Works

### Step-by-Step Process

1. **Enter Topic**: Type any topic (e.g., "Artificial Intelligence")

2. **Web Scraping Begins**:
   - Searches Wikipedia for the topic
   - Searches DuckDuckGo for relevant URLs
   - Scrapes 2-5 websites for content
   - Takes 10-30 seconds depending on sources

3. **Content Extraction**:
   - Extracts paragraphs, headings, and sections
   - Identifies key points
   - Structures information into slides

4. **Outline Generation**:
   - Creates introduction from first paragraphs
   - Uses headings/sections as slide titles
   - Extracts 3 key points per slide
   - Tracks source URLs

5. **Review & Edit**:
   - Review generated outline
   - Edit any content
   - Modify slide titles
   - Update speaker notes

6. **Generate & Export**:
   - Apply theme
   - Generate final presentation
   - Export with source citations

## 🌟 What Makes This Special

### Real Content
Unlike template-based generators, this scrapes ACTUAL content from the web:
- Current information
- Real statistics and data
- Credible sources
- Up-to-date facts

### Source Tracking
Every slide tracks its source:
- URL attribution
- Automatic citations
- Source list at end
- Proper crediting

### Intelligent Extraction
Smart algorithms extract the best content:
- Identifies main content areas
- Filters out navigation/ads
- Extracts key sentences
- Prioritizes substantial paragraphs

## 🎯 Use Cases

### Students
- **Research Presentations**: Gather info from multiple sources
- **Quick Overviews**: Fast summary of any topic
- **Cited Content**: Automatic source tracking
- **Learning Tool**: See how information is structured

### Professionals
- **Market Research**: Gather current market data
- **Industry Reports**: Compile information from sources
- **Quick Briefs**: Fast background on new topics
- **Competitive Analysis**: Scrape competitor information

### Educators
- **Teaching Materials**: Create educational presentations
- **Current Events**: Up-to-date information
- **Topic Introductions**: Quick overviews for students
- **Resource Compilation**: Gather web resources

## 📊 Example Topics That Work Well

### Technology
- "Artificial Intelligence"
- "Blockchain Technology"
- "Quantum Computing"
- "5G Networks"

### Business
- "Digital Marketing Strategies"
- "Startup Funding"
- "Remote Work Trends"
- "E-commerce Growth"

### Science
- "Climate Change"
- "Space Exploration"
- "Renewable Energy"
- "Genetic Engineering"

### Health
- "Mental Health Awareness"
- "Nutrition Science"
- "Exercise Benefits"
- "Sleep Research"

### History & Culture
- "Ancient Egypt"
- "World War II"
- "Renaissance Art"
- "Cultural Diversity"

## ⚙️ Configuration Options

### Number of Slides
- Minimum: 5 slides
- Maximum: 12 slides
- Recommended: 8 slides

### Number of Sources
- Minimum: 2 sources
- Maximum: 5 sources
- More sources = Better content but slower
- Recommended: 3 sources for balance

### Themes
Choose from 9 professional themes:
1. Professional Blue
2. Modern Dark
3. Elegant Purple
4. Nature Green
5. Sunset Orange
6. Ocean Blue
7. Rose Pink
8. Tech Gray
9. Vibrant Yellow

## 📚 Sources Used

### Wikipedia
- First source checked
- Reliable, comprehensive
- Good structure (sections/headings)
- Often has introduction and overview

### DuckDuckGo Search
- Searches for additional sources
- Returns relevant URLs
- Privacy-focused search
- Good variety of sources

### General Websites
- News sites
- Educational sites
- Company websites
- Blog posts
- Research articles

## 🔧 Technical Details

### Web Scraping
```python
- Uses requests library
- BeautifulSoup for parsing
- Respects robots.txt
- User-Agent headers
- 1 second delay between requests
```

### Content Extraction
```python
- Removes scripts, styles, nav, footer
- Finds main content areas
- Extracts paragraphs (>50 chars)
- Gets headings (h1, h2, h3)
- Cleans citation references
```

### Key Point Extraction
```python
- Splits into sentences
- Filters by length (30-200 chars)
- Takes most substantial sentences
- Removes very short/long text
```

## ⚠️ Important Notes

### Ethical Use
- ✅ Always cite sources
- ✅ Respect copyright
- ✅ Use for educational/research purposes
- ✅ Add your own analysis
- ❌ Don't plagiarize
- ❌ Don't scrape restricted content
- ❌ Don't overload servers

### Limitations
- Some websites block scraping
- Content quality varies by source
- May not work for all topics
- Takes 10-30 seconds to generate
- Requires internet connection
- Not all sites are scrapeable

### Best Practices
1. **Review Content**: Always review scraped content
2. **Edit for Accuracy**: Verify information
3. **Add Context**: Add your own insights
4. **Cite Sources**: Use provided citations
5. **Respect Limits**: Don't scrape excessively

## 🆚 Comparison with Other Versions

| Feature | Web Scraping | API Version | Template |
|---------|--------------|-------------|----------|
| Cost | FREE | ~$0.06-$0.20 | FREE |
| Speed | 10-30 sec | 30-60 sec | Instant |
| Content | Real from web | AI-generated | Template-based |
| Quality | Good | Excellent | Basic |
| Sources | Cited | None | None |
| Internet | Required | Required | Optional |
| Unique | Varies | Always | No |
| Current Info | YES | Depends | NO |

## 🚀 Advanced Usage

### Custom Source Selection

You can modify the code to scrape specific websites:

```python
# Add your preferred sources
custom_urls = [
    "https://example.com/article1",
    "https://example.com/article2"
]

for url in custom_urls:
    data = scrape_website(url)
    scraped_data.append(data)
```

### Filtering Content

Adjust content extraction parameters:

```python
# Extract more/fewer points
key_points = extract_key_points(text, num_points=5)

# Adjust sentence length filters
if len(sentence) > 20 and len(sentence) < 150:
    key_points.append(sentence)
```

### Adding More Sources

Increase search results:

```python
search_results = search_duckduckgo(topic, num_results=10)
```

## 🐛 Troubleshooting

### "Could not scrape any content"
**Causes:**
- Topic too obscure
- Websites blocking access
- Network issues

**Solutions:**
- Try different topic wording
- Check internet connection
- Try again in a few minutes

### "Content quality is poor"
**Causes:**
- Limited sources available
- Low-quality websites scraped

**Solutions:**
- Increase number of sources
- Try more specific topic
- Edit content manually

### "Scraping is slow"
**Causes:**
- Many sources selected
- Slow website responses

**Solutions:**
- Reduce number of sources
- Check internet speed
- Be patient (10-30 sec is normal)

## 📊 Output Formats

### JSON Export
```json
{
  "title": "Your Topic",
  "slides": [...],
  "sources": [
    {
      "source": "Wikipedia",
      "url": "https://...",
      "title": "..."
    }
  ]
}
```

### Text Export
```
Title
==========
Generated from web research

Slide 1: Introduction
==========
• Point 1
• Point 2
• Point 3
Source: https://...

SOURCES
==========
1. Wikipedia - https://...
2. Example.com - https://...
```

## 🔐 Privacy & Security

- No personal data collected
- No tracking or analytics
- Sources are public websites
- Respects robots.txt
- User-Agent identifies as browser
- No cookies or sessions stored

## 🛣️ Roadmap

- [ ] PDF export with citations
- [ ] PowerPoint export
- [ ] Custom website selection
- [ ] Image scraping from sources
- [ ] Video content extraction
- [ ] Multi-language support
- [ ] Advanced filtering options
- [ ] Fact-checking integration
- [ ] Academic citation formats
- [ ] Bookmark favorite sources

## 📖 Example Workflow

```bash
# 1. Install
pip install -r requirements_webscraping.txt

# 2. Run
streamlit run presentation_generator_webscraping.py

# 3. In the app:
Topic: "Artificial Intelligence"
Sources: 3
Slides: 8

# 4. Wait 15-20 seconds for scraping

# 5. Review outline (edit if needed)

# 6. Choose theme and generate

# 7. Export with sources
```

## 🤝 Contributing

Want to improve web scraping?

**Ideas:**
- Add more search engines
- Improve content extraction
- Add more source types
- Better error handling
- Caching scraped content

## ⚖️ Legal Notice

This tool is for educational and research purposes. Users are responsible for:
- Respecting copyright laws
- Following website terms of service
- Proper citation of sources
- Ethical use of scraped content

Always review and verify scraped content before use.

## 🙏 Credits

- **BeautifulSoup**: HTML parsing
- **Requests**: HTTP library
- **Streamlit**: Web framework
- **Wikipedia**: Primary source
- **DuckDuckGo**: Search functionality

## 📞 Support

**Issues:**
- Content not scraping: Try different topic
- Slow performance: Reduce sources
- Poor quality: Manually edit content

**Tips:**
- Be specific with topics
- Use popular subjects
- Allow time for scraping
- Always review content

---

**🌐 Start creating presentations with real web content!**

```bash
streamlit run presentation_generator_webscraping.py
```
