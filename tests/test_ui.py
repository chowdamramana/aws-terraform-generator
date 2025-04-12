import pytest
from playwright.async_api import async_playwright

@pytest.mark.asyncio
async def test_config_wizard():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://localhost:8000/config")
        await page.fill('input[name="config_name"]', "Test Config")
        await page.select_option('select[name="region"]', "us-east-1")
        await page.click('button[type="submit"]')
        await page.wait_for_selector('#step2')
        assert "Add Resources" in await page.content()
        await browser.close()