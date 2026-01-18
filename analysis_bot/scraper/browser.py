from playwright.async_api import async_playwright
import asyncio

async def scrape_reviews(url: str):
    """
    Scrapes reviews from the given URL using Playwright.
    Handles dynamic content by scrolling to the bottom.
    """
    async with async_playwright() as p:
        # Launch browser (headless for performance)
        browser = await p.chromium.launch(headless=True)
        # Context to simulate a real user agent roughly
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            print(f"Navigating to {url}...")
            await page.goto(url, timeout=60000) # 60s timeout

            # Auto-scroll to load dynamic content (simulating review loading)
            # Scroll multiple times
            for _ in range(5): 
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(2) # Wait for content to load

            # Extract Text
            # Ideally, we'd target specific review containers based on the URL (Amazon vs TikTok)
            # For MVP, we'll try to get the main content or fall back to body text
            
            # Simple heuristic for Amazon review section (often #reviews-medley-footer or similar, but class names change)
            # Hooking into specific IDs is brittle. For MVP Generative UI, we'll strip scripts/styles and dump text.
            
            content = await page.evaluate("""() => {
                // clone body to avoid modifying page
                let body = document.body.cloneNode(true);
                // remove scripts and styles
                let scripts = body.getElementsByTagName('script');
                let i = scripts.length;
                while (i--) { scripts[i].parentNode.removeChild(scripts[i]); }
                let styles = body.getElementsByTagName('style');
                i = styles.length;
                while (i--) { styles[i].parentNode.removeChild(styles[i]); }
                
                return body.innerText;
            }""")
            
            return content

        except Exception as e:
            print(f"Scraping error: {e}")
            return None
        finally:
            await browser.close()
