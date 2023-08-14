import { Page } from '@playwright/test';
import { test, expect } from '@playwright/test';

export async function goToDataSet(page: Page) {
    console.log("Go to DataSet page")
    await page.getByLabel('Navigate to Security Data Lake Add-On for Splunk app').click()
    await page.screenshot({ path: 'playwright-screenshots/page-home.png', fullPage: true });
}

export async function goToExamples(page: Page) {
    console.log("Go to example page");
    await page.getByText("DataSet by Example").click();

    await expect(page).toHaveTitle(/DataSet by Example /);
}

export async function goToSearch(page: Page) {
    console.log("Go to search page");
    await page.getByRole('link', { name: 'Search' }).click();

    await expect(page).toHaveTitle(/Search /);
}

export async function waitForData(page: Page, key: string) {
    // Wait for the "Waiting for data..." text to disappear
    console.log("Wait for 'Waiting for data' to disappear")
    await page.screenshot({ path: `playwright-screenshots/page-${ key }-before-waiting-for-data.png`, fullPage: true });
    await expect(page.getByText(/Waiting for data/)).toHaveCount(0, {timeout: 15000});

    await page.screenshot({ path: `playwright-screenshots/page-${ key }-before-checks.png`, fullPage: true });

    // Check if the page does not contain the text "No results found."
    const noResultsCount = await page.getByText(/No results found/).count();
    console.log("Page contains 'No results found': ", noResultsCount)
    expect(noResultsCount).toBe(0);

    // Check if the page does not contain the text "No results found."
    const searchFailedCount = await page.getByText(/External search command exited unexpectedly/).count();
    console.log("Page contains 'External search command exited unexpectedly': ", searchFailedCount)
    expect(searchFailedCount).toBe(0);

    const { WAIT_FOR_HUMAN_TO_CHECK_IN_MS: waitForHumanStr} = process.env
    const waitForHumanMs = parseInt(waitForHumanStr || '0');
    console.log("Waiting for human for: ", waitForHumanMs);

    await page.waitForTimeout(waitForHumanMs);
}
