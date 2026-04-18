import sys
import os
# Add project root to Python path - MUST BE BEFORE OTHER IMPORTS
project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root_path)

import pytest
import logging
from datetime import datetime
from pathlib import Path
# Now this import will work
from utilities.email_pytest_report import EmailPytestReport
from playwright.sync_api import Playwright

# Project root path
project_root = Path(__file__).parent.parent


# ==================== PYTEST HOOKS ====================

def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--browser_name", action="store", default="chrome",
        help="Browser selection: chrome, firefox, webkit"
    )
    parser.addoption(
        "--headless", action="store", default="false",
        help="Run in headless mode: true/false"
    )
    parser.addoption(
        "--env", action="store", default="qa",
        help="Environment: dev, qa, staging, prod"
    )
    parser.addoption(
        "--slow_mo", action="store", default="0",
        help="Slow down execution by milliseconds"
    )
    #Email-option
    parser.addoption(
        "--email_report",
        action="store",
        default="N",
        help="Send email report: Y or N"
    )


def pytest_configure(config):
    """Called after command line options are parsed"""
    # Create directories if they don't exist
    os.makedirs(project_root / 'logs', exist_ok=True)
    os.makedirs(project_root / 'screenshots', exist_ok=True)
    os.makedirs(project_root / 'Testdata' / 'reports', exist_ok=True)

    # Configure logging
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = project_root / 'logs' / f'test_run_{timestamp}.log'

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    # Add custom markers
    config.addinivalue_line("markers", "sanity: mark test as sanity test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "critical: mark test as critical test")


def pytest_collection_modifyitems(config, items):
    """Modify test collection - add markers dynamically"""
    for item in items:
        # Add browser marker based on test name
        if "chrome" in item.name.lower():
            item.add_marker(pytest.mark.chrome)
        elif "firefox" in item.name.lower():
            item.add_marker(pytest.mark.firefox)


def pytest_runtest_setup(item):
    """Called before each test setup"""
    logging.info(f"\
{'=' * 60}")
    logging.info(f"STARTING TEST: {item.name}")
    logging.info(f"{'=' * 60}")


def pytest_runtest_teardown(item, nextitem):
    """Called after each test teardown"""
    logging.info(f"COMPLETED TEST: {item.name}")
    logging.info(f"{'=' * 60}\
")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results and take screenshots on failure"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Get the page fixture if available
        page = item.funcargs.get('browserInstance')
        if page:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_path = project_root / 'screenshots' / f'{item.name}_{timestamp}.png'
            page.screenshot(path=str(screenshot_path))
            logging.error(f"Screenshot saved: {screenshot_path}")


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Add custom summary to terminal output"""
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))

    terminalreporter.write_sep("=", "CUSTOM TEST SUMMARY")
    terminalreporter.write_line(f"Passed: {passed}")
    terminalreporter.write_line(f"Failed: {failed}")
    terminalreporter.write_line(f"Skipped: {skipped}")
    terminalreporter.write_line(f"Total: {passed + failed + skipped}")

    # ← EMAIL REPORT LOGIC ADDED HERE (was duplicate before)
    # In pytest_terminal_summary function:
    email_option = config.getoption("--email_report")
    if email_option and email_option.upper() == 'Y':
        report_path = str(project_root / 'reports' / 'pytest_report.html')
        email_obj = EmailPytestReport()

        # Check return value - only show success if True
        if email_obj.send_report(
                report_file_path=report_path,
                subject='Playwright Test Results'
        ):
            terminalreporter.write_line("📧 Email report sent successfully!")
        else:
            terminalreporter.write_line("⚠️ Email report failed to send")

# ==================== FIXTURES ====================

@pytest.fixture
def user_credentials(request):
    """Return parametrized user credentials"""
    return request.param


@pytest.fixture(scope="function")
def browserInstance(playwright, request):
    """Browser instance fixture with enhanced configuration"""
    browser_name = request.config.getoption("browser_name")
    headless = request.config.getoption("headless").lower() == "true"
    slow_mo = int(request.config.getoption("slow_mo"))

    browser_options = {
        "headless": headless,
        "slow_mo": slow_mo,
        "args": ["--start-maximized"]
    }

    # Browser selection
    if browser_name == "chrome":
        browser = playwright.chromium.launch(**browser_options)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(**browser_options)
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(**browser_options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    # Context with viewport and other settings
    context = browser.new_context(
        no_viewport=True,  # CHANGE THIS - allows window to use full size
        record_video_dir=str(project_root / 'Testdata' / 'reports' / 'videos') if not headless else None
    )

    # Enable tracing for debugging
    context.tracing.start(screenshots=True, snapshots=True)

    page = context.new_page()

    logging.info(f"Browser launched: {browser_name} (headless={headless})")

    yield page

    # Teardown
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    trace_path = project_root / 'Testdata' / 'reports' / f'trace_{timestamp}.zip'
    context.tracing.stop(path=str(trace_path))

    context.close()
    browser.close()
    logging.info("Browser closed")


@pytest.fixture(scope="session")
def test_config(request):
    """Load test configuration based on environment"""
    import json
    env = request.config.getoption("env")
    config_path = project_root / 'Testdata' / 'config.json'

    with open(config_path) as f:
        config = json.load(f)

    return config.get(env, config.get('qa'))

