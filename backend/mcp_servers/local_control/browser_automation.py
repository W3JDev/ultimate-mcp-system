"""
Browser Automation - Control web browsers programmatically
"""

from typing import Any, Dict, Optional

from loguru import logger
from playwright.sync_api import sync_playwright


class BrowserAutomation:
    """Browser automation using Playwright"""

    def __init__(self):
        """Initialize browser automation"""
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        logger.info("🌐 Browser automation initialized")

    def start_browser(self, headless: bool = True) -> Dict[str, Any]:
        """
        Start browser instance

        Args:
            headless: Run in headless mode

        Returns:
            Operation result
        """
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=headless)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()

            logger.info("✅ Browser started successfully")
            return {"success": True, "message": "Browser started"}

        except Exception as e:
            logger.error(f"Browser start error: {e}")
            return {"success": False, "error": str(e)}

    def navigate(self, url: str) -> Dict[str, Any]:
        """
        Navigate to URL

        Args:
            url: Target URL

        Returns:
            Navigation result
        """
        try:
            if not self.page:
                self.start_browser()

            self.page.goto(url, wait_until="domcontentloaded")
            logger.info(f"📍 Navigated to {url}")

            return {
                "success": True,
                "url": self.page.url,
                "title": self.page.title(),
            }

        except Exception as e:
            logger.error(f"Navigation error: {e}")
            return {"success": False, "error": str(e)}

    def screenshot(self, path: Optional[str] = None) -> Dict[str, Any]:
        """
        Take page screenshot

        Args:
            path: Optional save path

        Returns:
            Screenshot result
        """
        try:
            if not self.page:
                return {"success": False, "error": "No browser page active"}

            if not path:
                path = "screenshot.png"

            self.page.screenshot(path=path)
            logger.info(f"📸 Screenshot saved to {path}")

            return {"success": True, "path": path}

        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            return {"success": False, "error": str(e)}

    def click_element(self, selector: str) -> Dict[str, Any]:
        """
        Click element by selector

        Args:
            selector: CSS selector

        Returns:
            Operation result
        """
        try:
            if not self.page:
                return {"success": False, "error": "No browser page active"}

            self.page.click(selector)
            logger.info(f"👆 Clicked element: {selector}")

            return {"success": True, "message": f"Clicked {selector}"}

        except Exception as e:
            logger.error(f"Click error: {e}")
            return {"success": False, "error": str(e)}

    def fill_form(self, selector: str, value: str) -> Dict[str, Any]:
        """
        Fill form field

        Args:
            selector: CSS selector
            value: Value to fill

        Returns:
            Operation result
        """
        try:
            if not self.page:
                return {"success": False, "error": "No browser page active"}

            self.page.fill(selector, value)
            logger.info(f"✍️  Filled {selector} with value")

            return {"success": True, "message": f"Filled {selector}"}

        except Exception as e:
            logger.error(f"Fill error: {e}")
            return {"success": False, "error": str(e)}

    def get_text(self, selector: str) -> Dict[str, Any]:
        """
        Extract text from element

        Args:
            selector: CSS selector

        Returns:
            Extracted text
        """
        try:
            if not self.page:
                return {"success": False, "error": "No browser page active"}

            text = self.page.text_content(selector)
            logger.info(f"📝 Extracted text from {selector}")

            return {"success": True, "text": text}

        except Exception as e:
            logger.error(f"Text extraction error: {e}")
            return {"success": False, "error": str(e)}

    def execute_script(self, script: str) -> Dict[str, Any]:
        """
        Execute JavaScript in page

        Args:
            script: JavaScript code

        Returns:
            Script result
        """
        try:
            if not self.page:
                return {"success": False, "error": "No browser page active"}

            result = self.page.evaluate(script)
            logger.info("🔧 Executed JavaScript")

            return {"success": True, "result": result}

        except Exception as e:
            logger.error(f"Script execution error: {e}")
            return {"success": False, "error": str(e)}

    def close_browser(self) -> Dict[str, Any]:
        """
        Close browser and cleanup

        Returns:
            Operation result
        """
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()

            logger.info("✅ Browser closed")
            return {"success": True, "message": "Browser closed"}

        except Exception as e:
            logger.error(f"Browser close error: {e}")
            return {"success": False, "error": str(e)}
