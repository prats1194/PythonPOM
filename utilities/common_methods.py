"""
Common Methods Utility
Reusable methods for Playwright automation
"""

import logging
import time
import re
from datetime import datetime
from playwright.sync_api import Page, expect, Locator
from typing import Optional, List


class CommonMethods:
    """Common reusable methods for test automation"""

    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(__name__)

    # ==================== WAIT METHODS ====================

    def wait_for_element_visible(self, locator: str, timeout: int = 30000) -> Locator:
        """Wait for element to be visible"""
        element = self.page.locator(locator)
        element.wait_for(state="visible", timeout=timeout)
        self.logger.info(f"Element visible: {locator}")
        return element

    def wait_for_element_hidden(self, locator: str, timeout: int = 30000):
        """Wait for element to be hidden"""
        element = self.page.locator(locator)
        element.wait_for(state="hidden", timeout=timeout)
        self.logger.info(f"Element hidden: {locator}")

    def wait_for_page_load(self, timeout: int = 30000):
        """Wait for page to fully load"""
        self.page.wait_for_load_state("networkidle", timeout=timeout)
        self.logger.info("Page fully loaded")

    def wait_for_url_contains(self, url_part: str, timeout: int = 30000):
        """Wait for URL to contain specific text"""
        self.page.wait_for_url(f"**/*{url_part}*", timeout=timeout)
        self.logger.info(f"URL contains: {url_part}")

    def explicit_wait(self, seconds: int):
        """Explicit wait (use sparingly)"""
        time.sleep(seconds)
        self.logger.info(f"Waited for {seconds} seconds")

    # ==================== CLICK METHODS ====================

    def click_element(self, locator: str, force: bool = False):
        """Click on element with logging"""
        self.page.locator(locator).click(force=force)
        self.logger.info(f"Clicked: {locator}")

    def double_click_element(self, locator: str):
        """Double click on element"""
        self.page.locator(locator).dblclick()
        self.logger.info(f"Double clicked: {locator}")

    def right_click_element(self, locator: str):
        """Right click on element"""
        self.page.locator(locator).click(button="right")
        self.logger.info(f"Right clicked: {locator}")

    def click_by_text(self, text: str):
        """Click element by visible text"""
        self.page.get_by_text(text).click()
        self.logger.info(f"Clicked by text: {text}")

    def click_by_role(self, role: str, name: str):
        """Click element by role and name"""
        self.page.get_by_role(role, name=name).click()
        self.logger.info(f"Clicked by role: {role}, name: {name}")

    # ==================== INPUT METHODS ====================

    def enter_text(self, locator: str, text: str, clear_first: bool = True):
        """Enter text into input field"""
        element = self.page.locator(locator)
        if clear_first:
            element.clear()
        element.fill(text)
        self.logger.info(f"Entered text in {locator}: {text[:20]}...")

    def type_text(self, locator: str, text: str, delay: int = 50):
        """Type text character by character"""
        self.page.locator(locator).type(text, delay=delay)
        self.logger.info(f"Typed text in {locator}")

    def clear_field(self, locator: str):
        """Clear input field"""
        self.page.locator(locator).clear()
        self.logger.info(f"Cleared field: {locator}")

    def press_key(self, key: str):
        """Press keyboard key"""
        self.page.keyboard.press(key)
        self.logger.info(f"Pressed key: {key}")

    # ==================== DROPDOWN METHODS ====================

    def select_dropdown_by_value(self, locator: str, value: str):
        """Select dropdown option by value"""
        self.page.locator(locator).select_option(value=value)
        self.logger.info(f"Selected dropdown value: {value}")

    def select_dropdown_by_label(self, locator: str, label: str):
        """Select dropdown option by visible label"""
        self.page.locator(locator).select_option(label=label)
        self.logger.info(f"Selected dropdown label: {label}")

    def select_dropdown_by_index(self, locator: str, index: int):
        """Select dropdown option by index"""
        self.page.locator(locator).select_option(index=index)
        self.logger.info(f"Selected dropdown index: {index}")

    # ==================== CHECKBOX/RADIO METHODS ====================

    def check_checkbox(self, locator: str):
        """Check a checkbox"""
        self.page.locator(locator).check()
        self.logger.info(f"Checked: {locator}")

    def uncheck_checkbox(self, locator: str):
        """Uncheck a checkbox"""
        self.page.locator(locator).uncheck()
        self.logger.info(f"Unchecked: {locator}")

    def is_checked(self, locator: str) -> bool:
        """Check if checkbox/radio is checked"""
        return self.page.locator(locator).is_checked()

    # ==================== VERIFICATION METHODS ====================

    def is_element_visible(self, locator: str) -> bool:
        """Check if element is visible"""
        return self.page.locator(locator).is_visible()

    def is_element_enabled(self, locator: str) -> bool:
        """Check if element is enabled"""
        return self.page.locator(locator).is_enabled()

    def get_element_text(self, locator: str) -> str:
        """Get text content of element"""
        text = self.page.locator(locator).text_content()
        self.logger.info(f"Got text from {locator}: {text}")
        return text

    def get_element_attribute(self, locator: str, attribute: str) -> str:
        """Get attribute value of element"""
        value = self.page.locator(locator).get_attribute(attribute)
        self.logger.info(f"Got attribute {attribute} from {locator}: {value}")
        return value

    def get_element_count(self, locator: str) -> int:
        """Get count of matching elements"""
        count = self.page.locator(locator).count()
        self.logger.info(f"Element count for {locator}: {count}")
        return count

    def get_all_texts(self, locator: str) -> List[str]:
        """Get all text contents from matching elements"""
        return self.page.locator(locator).all_text_contents()

    # ==================== ASSERTION METHODS ====================

    def verify_element_visible(self, locator: str):
        """Assert element is visible"""
        expect(self.page.locator(locator)).to_be_visible()
        self.logger.info(f"Verified visible: {locator}")

    def verify_element_hidden(self, locator: str):
        """Assert element is hidden"""
        expect(self.page.locator(locator)).to_be_hidden()
        self.logger.info(f"Verified hidden: {locator}")

    def verify_text_present(self, locator: str, expected_text: str):
        """Assert element contains expected text"""
        expect(self.page.locator(locator)).to_contain_text(expected_text)
        self.logger.info(f"Verified text '{expected_text}' in {locator}")

    def verify_element_enabled(self, locator: str):
        """Assert element is enabled"""
        expect(self.page.locator(locator)).to_be_enabled()
        self.logger.info(f"Verified enabled: {locator}")

    def verify_element_disabled(self, locator: str):
        """Assert element is disabled"""
        expect(self.page.locator(locator)).to_be_disabled()
        self.logger.info(f"Verified disabled: {locator}")

    def verify_url_contains(self, expected_url_part: str):
        """Assert URL contains expected text"""
        expect(self.page).to_have_url(re.compile(f".*{expected_url_part}.*"))
        self.logger.info(f"Verified URL contains: {expected_url_part}")

    def verify_title(self, expected_title: str):
        """Assert page title"""
        expect(self.page).to_have_title(expected_title)
        self.logger.info(f"Verified title: {expected_title}")

    # ==================== NAVIGATION METHODS ====================

    def navigate_to(self, url: str):
        """Navigate to URL"""
        self.page.goto(url)
        self.logger.info(f"Navigated to: {url}")

    def refresh_page(self):
        """Refresh current page"""
        self.page.reload()
        self.logger.info("Page refreshed")

    def go_back(self):
        """Navigate back"""
        self.page.go_back()
        self.logger.info("Navigated back")

    def go_forward(self):
        """Navigate forward"""
        self.page.go_forward()
        self.logger.info("Navigated forward")

    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.page.url

    def get_page_title(self) -> str:
        """Get current page title"""
        return self.page.title()

    # ==================== FRAME METHODS ====================

    def switch_to_frame(self, frame_locator: str):
        """Switch to iframe"""
        return self.page.frame_locator(frame_locator)

    # ==================== SCREENSHOT METHODS ====================

    def take_screenshot(self, filename: str = None) -> str:
        """Take screenshot and return path"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = f"screenshots/{filename}"
        self.page.screenshot(path=screenshot_path)
        self.logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path

    def take_element_screenshot(self, locator: str, filename: str = None) -> str:
        """Take screenshot of specific element"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"element_{timestamp}.png"

        screenshot_path = f"screenshots/{filename}"
        self.page.locator(locator).screenshot(path=screenshot_path)
        self.logger.info(f"Element screenshot saved: {screenshot_path}")
        return screenshot_path

    # ==================== SCROLL METHODS ====================

    def scroll_to_element(self, locator: str):
        """Scroll element into view"""
        self.page.locator(locator).scroll_into_view_if_needed()
        self.logger.info(f"Scrolled to: {locator}")

    def scroll_to_top(self):
        """Scroll to top of page"""
        self.page.evaluate("window.scrollTo(0, 0)")
        self.logger.info("Scrolled to top")

    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        self.logger.info("Scrolled to bottom")

    # ==================== HOVER METHODS ====================

    def hover_element(self, locator: str):
        """Hover over element"""
        self.page.locator(locator).hover()
        self.logger.info(f"Hovered over: {locator}")

    # ==================== DIALOG METHODS ====================

    def accept_alert(self):
        """Accept alert dialog"""
        self.page.on("dialog", lambda dialog: dialog.accept())
        self.logger.info("Alert accepted")

    def dismiss_alert(self):
        """Dismiss alert dialog"""
        self.page.on("dialog", lambda dialog: dialog.dismiss())
        self.logger.info("Alert dismissed")

    # ==================== FILE UPLOAD ====================

    def upload_file(self, locator: str, file_path: str):
        """Upload file to input element"""
        self.page.locator(locator).set_input_files(file_path)
        self.logger.info(f"Uploaded file: {file_path}")

    # ==================== JAVASCRIPT EXECUTION ====================

    def execute_javascript(self, script: str):
        """Execute JavaScript code"""
        result = self.page.evaluate(script)
        self.logger.info(f"Executed JS: {script[:50]}...")
        return result