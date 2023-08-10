import { Page } from '@playwright/test';

export async function goToDataSet(page: Page) {
    console.log("Go to DataSet page")
    await page.getByLabel('Navigate to Security Data Lake Add-On for Splunk app').click()
    await page.screenshot({ path: 'playwright-screenshots/page-home.png', fullPage: true });
}
