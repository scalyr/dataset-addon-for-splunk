import { Locator, Page } from '@playwright/test';
import { test, expect } from '@playwright/test';

export async function goToDataSet(page: Page) {
    console.log("Go to DataSet page")
    await page.getByLabel('Navigate to Security Data Lake Add-On for Splunk app').click()
    await page.screenshot({ path: 'playwright-screenshots/page-home.png', fullPage: true });
}

export async function goToInputs(page: Page) {
    console.log("Go to inputs page");

    await page.getByRole('link', { name: "Inputs" }).click();
    const responsePromise = page.waitForResponse('**/TA_dataset_*');
    await expect(page).toHaveTitle(/Inputs/);

    const response = await responsePromise;
    expect({'u': response.url(), 's': response.status()}).toBe("AAA");


    await expectWithoutErrors(page);
}

export async function goToExamples(page: Page) {
    console.log("Go to example page");
    await page.getByRole('link', { name: "DataSet by Example" }).click();

    await expect(page).toHaveTitle(/DataSet by Example/);

    await expectWithoutErrors(page);
}

export async function goToSearch(page: Page) {
    console.log("Go to search page");
    await page.getByRole('link', { name: 'Search' }).click();

    await expect(page).toHaveTitle(/Search/);

    await expectWithoutErrors(page);
}

export async function waitForData(page: Page, key: string) {
    await page.waitForTimeout(5000);

    let pic = 0

    await page.screenshot({ path: `playwright-screenshots/page-${ key }-wait-for-data-${ pic++ }.png`, fullPage: true });

    console.log("Wait for 'Waiting for queued job to start' to disappear")
    await expect(page.getByText(/Waiting for queued job to start/)).toHaveCount(0, {timeout: 50000})
    await page.screenshot({ path: `playwright-screenshots/page-${ key }-wait-for-data-${ pic++ }.png`, fullPage: true });

    console.log("Wait for 'Waiting for data' to disappear")
    await expect(page.getByText(/Waiting for data/)).toHaveCount(0, {timeout: 50000})
    await page.screenshot({ path: `playwright-screenshots/page-${ key }-wait-for-data-${ pic++ }.png`, fullPage: true });

    console.log("Wait for 'No results yet found' to disappear")
    await expect(page.getByText(/No results yet found/)).toHaveCount(0, {timeout: 50000})
    await page.screenshot({ path: `playwright-screenshots/page-${ key }-wait-for-data-${ pic++ }.png`, fullPage: true });

    // It looks that No results found element is still there, but not visible
    console.log("Wait for 'No results found' to disappear");
    const locNoResults = page.getByText(/No results found/);
    if (await locNoResults.count() > 0) {
        if (await locNoResults.isVisible()) {
            await expect(locNoResults).toHaveCount(0, {timeout: 50000})
            await page.screenshot({ path: `playwright-screenshots/page-${ key }-wait-for-data-${ pic++ }.png`, fullPage: true });
        }
    }

    console.log("Page contains 'External search command exited unexpectedly'")
    await expect(page.getByText(/External search command exited unexpectedly/)).toHaveCount(0, {timeout: 50000});
    await page.screenshot({ path: `playwright-screenshots/page-${ key }-wait-for-data-${ pic++ }.png`, fullPage: true });

    const { WAIT_FOR_HUMAN_TO_CHECK_IN_MS: waitForHumanStr} = process.env
    const waitForHumanMs = parseInt(waitForHumanStr || '0');
    console.log("Waiting for human for: ", waitForHumanMs);

    await page.waitForTimeout(waitForHumanMs);
}

async function expectWithoutErrors(page: Page) {
    expect(page.getByRole("heading").getByText(/Failed to load/)).toHaveCount(0);
}
