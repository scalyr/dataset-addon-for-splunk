import { test, expect, Page } from '@playwright/test';
import { goToDataSetInputsPage, query2file, checkRowExists } from './utils';

test.beforeEach(async ({ page }) => {
  await goToDataSetInputsPage(page);
  await clearInputs(page);
});


test('New Input - DataSet Query', async ({ page }) => {

  await openDialog(page, "DataSet Query");

  console.log("Fill the form")
  const queryName = ('QuErY_Q_' + (Math.random() * 1e18)).slice(0, 15)
  console.log("Create query: ", queryName);

  await page.locator('div').filter({ hasText: /^\*?NameEnter a unique name for the data input$/ }).locator('[data-test="textbox"]').fill(queryName);
  await page.locator('div').filter({ hasText: /^\*?IntervalTime interval of input in seconds\.$/ }).locator('[data-test="textbox"]').fill("60")
  await page.locator('form div').filter({ hasText: /^\*?Start TimeRelative time to query back. Use short form relative time, e.g.: 24h/ }).locator('[data-test="textbox"]').fill("60m")
  await page.locator('form div').filter({ hasText: /^\*?End TimeIf left blank, present time at query execution is used. If defined, use/ }).locator('[data-test="textbox"]').fill("1m")
  await page.locator('form div').filter({ hasText: /^\*?DataSet Query StringIf left blank, all records \(limited by max count\) are retrie/ }).locator('[data-test="textbox"]').fill("serverHost = *")
  await page.locator('div').filter({ hasText: /^\*?ColumnsIf left blank, all columns are returned\.$/ }).locator('[data-test="textbox"]').fill("")
  await page.locator('form div').filter({ hasText: /^\*?Max CountSpecifies the maximum number of records to return. If left blank, the d/ }).locator('[data-test="textbox"]').fill("13")

  await page.getByLabel("Select...").click();
  await page.locator('[data-test="option"]').first().click();

  await page.screenshot({ path: 'playwright-screenshots/page-inputs-query-01-filled-form.png', fullPage: true });

  await confirmDialog(page);

  await checkRowExists(page, queryName);

  await goToSplunkSearch(page);

  await searchSplunk(page, `source="dataset_query://${queryName}"`)
});

test('New Input - DataSet PowerQuery', async ({ page }) => {
  await openDialog(page, "DataSet PowerQuery");

  console.log("Fill the form")
  const queryName = ('QuErY_PQ_' + (Math.random() * 1e18)).slice(0, 15)
  console.log("Create query: ", queryName);

  await page.locator('div').filter({ hasText: /^\*?NameEnter a unique name for the data input$/ }).locator('[data-test="textbox"]').fill(queryName);
  await page.locator('div').filter({ hasText: /^\*?IntervalTime interval of input in seconds\.$/ }).locator('[data-test="textbox"]').fill("60")
  await page.locator('form div').filter({ hasText: /^\*?Start TimeRelative time to query back. Use short form relative time, e.g.: 24h/ }).locator('[data-test="textbox"]').fill("60m")
  await page.locator('form div').filter({ hasText: /^\*?End TimeIf left blank, present time at query execution is used. If defined, use/ }).locator('[data-test="textbox"]').fill("1m")
  await page.locator('form div').filter({ hasText: /^\*?DataSet PowerQuery String/ }).locator('[data-test="textbox"]').fill("serverHost=* | group count=count() by tag")

  await page.getByLabel("Select...").click();
  await page.locator('[data-test="option"]').first().click();

  await page.screenshot({ path: 'playwright-screenshots/page-inputs-powerquery-01-filled-form.png', fullPage: true });

  await confirmDialog(page);

  await checkRowExists(page, queryName);

  await goToSplunkSearch(page);

  await searchSplunk(page, `source="dataset_powerquery://${queryName}"`)
});

test('New Input - DataSet Alerts', async ({ page }) => {
  test.setTimeout(3 * 60 * 1000);

  await openDialog(page, "DataSet Alerts");

  console.log("Fill the form")
  const queryName = ('QuErY_A_' + (Math.random() * 1e18)).slice(0, 15)
  console.log("Create query: ", queryName);

  await page.locator('div').filter({ hasText: /^\*?NameEnter a unique name for the data input$/ }).locator('[data-test="textbox"]').fill(queryName);
  await page.locator('div').filter({ hasText: /^\*?IntervalTime interval of input in seconds\.$/ }).locator('[data-test="textbox"]').fill("20")
  await page.locator('form div').filter({ hasText: /^\*?Start TimeRelative time to query back. Use short form relative time, e.g.: 24h/ }).locator('[data-test="textbox"]').fill("60m")

  await page.getByLabel("Select...").click();
  await page.locator('[data-test="option"]').first().click();

  await page.screenshot({ path: 'playwright-screenshots/page-inputs-alerts-01-filled-form.png', fullPage: true });

  await confirmDialog(page);

  await checkRowExists(page, queryName);

  // Alerts are evaluated + alert state is reported every 1 minute so we need to wait at least 2 minutes to avoid
  // flaky tests. 3 minutes would be even better
  console.log("Waiting ~2 minutes since alerts are evaluated and state is reported only every 1 minute")
  await page.waitForTimeout(2 * 65 * 1000);

  await goToSplunkSearch(page);

  await searchSplunk(page, `source="dataset_alerts://${queryName}"`)
});

async function clearInputs(page: Page) {
  while ( 1 == 1 ) {
    const queryCount = await page.getByRole("main").getByRole("row").getByText(/QuErY/).count();
    console.log("Number of queries: ", queryCount);

    if (queryCount > 6) {
      const index = Math.floor(Math.random() * queryCount);
      console.log(`Deleting input: ${index}`);
      await page.getByRole("main").getByRole("row").getByRole("menubar").nth(index).getByRole("button").nth(2).click()
      await page.getByRole("button", {name: 'Delete'}).click();
    } else {
      break;
    }
  }
}

async function goToSplunkSearch(page: Page) {
    // go to the Splunk search App
    console.log("Go to the Splunk search page");
    await page.getByRole('button', { name: 'Apps ▾' }).click();
    await page.getByText("Search & Reporting").click()

    await expect(page).toHaveURL(/search\/search/);
    await expect(page).toHaveTitle(/Search/);
    await page.waitForTimeout(3000);

    const locPopup1 = page.getByRole("link", {name: "Skip", exact: true})
    const popup1Count = await locPopup1.count()
    console.log("Is there popup - 'Skip'? " + popup1Count);
    if (popup1Count > 0) {
      locPopup1.click()
    }

    await page.waitForTimeout(2000);
    const locPopup2 = page.getByRole("button", {name: "Skip tour", exact: true})
    const popup2Count = await locPopup2.count()
    console.log("Is there popup - 'Skip tour'? " + popup2Count);
    if (popup2Count > 0) {
      locPopup2.click()
    }
}

async function openDialog(page: Page, option: string) {
  console.log("Open Create New Input Dialog")
  await page.getByText("Create New Input").click()
  await page.getByText(option).click()
}

async function confirmDialog(page: Page) {
  console.log("Submit the form");
  const locAddConfirm = page.locator('[data-test="footer"]').getByRole('button', { name: 'Add' })
  await locAddConfirm.click();
}

async function searchSplunk(page: Page, query: string) {
  console.log(`Search in Splunk for: ${query}`);
  await page.getByRole('textbox', { name: 'Search' }).fill(query);
  await page.getByLabel("Search Button").click();

  await page.screenshot({ path: `playwright-screenshots/page-inputs-query-${query2file(query)}.png`, fullPage: true });
  await expect(page.getByText("sourcetype").first()).toBeVisible();
}
