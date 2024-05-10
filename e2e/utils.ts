import { Locator, Page } from '@playwright/test';
import { test, expect } from '@playwright/test';
import {setTimeout} from "timers/promises";

export async function goToDataSetSearchPage(page: Page) {
    console.log("Go to DataSet search page")
    await page.goto('/app/TA_dataset/search');
    await expect(page).toHaveTitle(/Search/);
    await expectWithoutErrors(page);
}

export async function goToDataSetPage(page: Page) {
    console.log("Go to DataSet page")
    await page.goto('/app/TA_dataset');
    await page.screenshot({ path: 'playwright-screenshots/page-home.png', fullPage: true });
}

export async function goToDataSetInputsPage(page: Page) {
    console.log("Go to DataSet inputs page");

    await page.goto('/app/TA_dataset/inputs');
    const respQueryPromise = page.waitForResponse('**/TA_dataset_dataset_query*');
    const respPowerqueryPromise = page.waitForResponse('**/TA_dataset_dataset_powerquery*');
    const respAlertsPromise = page.waitForResponse('**/TA_dataset_dataset_alerts*');

    await expect(page).toHaveTitle(/Inputs/);

    const respQuery = await respQueryPromise;
    const respPowerquery = await respPowerqueryPromise;
    const respAlerts = await respAlertsPromise;
    expect(respQuery.status()).toBe(200);
    expect(respPowerquery.status()).toBe(200);
    expect(respAlerts.status()).toBe(200);

    await expectWithoutErrors(page);
}

export async function goToDataSetConfigurationPage(page: Page) {
    console.log("Go to DataSet configuration page");

    await page.goto('/app/TA_dataset/configuration');
    const respAccountPromise = page.waitForResponse('**/TA_dataset_account*');

    await page.screenshot({ path: 'playwright-screenshots/page-configuration.png', fullPage: true });

    const respAccount = await respAccountPromise;
    expect(respAccount.status()).toBe(200);


    // wait for table to appear
    await page.getByText(/Account name/).click()

    await expectWithoutErrors(page);
}

export async function goToDataSetExamplesPage(page: Page) {
    console.log("Go to DataSet example page");
    await page.goto('/app/TA_dataset/sdl_by_example');

    await expect(page).toHaveTitle(/Singularity Data Lake by Example/);

    await expectWithoutErrors(page);
}

export async function searchDataSet(page: Page, query: string) {
    await goToDataSetSearchPage(page);
    console.log(`Search in DataSet for: ${query}`);
    await page.getByRole('textbox', {name: 'Search'}).fill(query);
    await page.getByLabel("Search Button").click();

    const queryScreenshotKey = query2file(query);
    await page.screenshot({path: `playwright-screenshots/page-search-query-${queryScreenshotKey}.png`, fullPage: true});
    await waitForSearchResults(page, queryScreenshotKey)
    await expect(page.getByText("sourcetype").first()).toBeHidden();
}

export async function waitForSearchResults(page: Page, key: string) {
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
    await expect(page.getByText(/No results yet found/, { exact: true })).toHaveCount(0, {timeout: 50000})
    await page.screenshot({ path: `playwright-screenshots/page-${ key }-wait-for-data-${ pic++ }.png`, fullPage: true });

    // It looks that No results found element is still there, but not visible
    console.log("Wait for 'No results found' to disappear");
    const locNoResults = page.getByText('No results found.', { exact: true });
    if (await locNoResults.count() > 0 && key != 'examples') {
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

export function query2file(query: string): string {
    return query.replace(/[| )(.,"'/\\:]/g, '_')
}

export async function checkRowExists(page: Page, value: string) {
  // check that the account is there
  console.log("Check that it is there: ", value);
  await page.getByRole('cell', { name: value }).click()

}
