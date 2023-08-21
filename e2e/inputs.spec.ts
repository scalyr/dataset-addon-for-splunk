import { test, expect } from '@playwright/test';
import { goToDataSet, goToInputs, waitForData } from './utils';

test.beforeEach(async ({ page }) => {
  await page.goto('/');

  await goToDataSet(page);
  await goToInputs(page);
});


test('Check inputs page', async ({ page }) => {
  await page.screenshot({ path: 'playwright-screenshots/page-inputs-after-checks.png', fullPage: true });

  while ( 1 == 1 ) {
    const queryCount = await page.getByRole("main").getByRole("row").getByText(/QuErY/).count();
    console.log("Number of queries: ", queryCount);

    if (queryCount > 100) {
      await page.getByRole("main").getByRole("row").locator('[data-test="button-group"]').first().getByRole("button").nth(3).click();
      await page.getByRole("button").click();
    } else {
      break;
    }
  }

  console.log("Open Create New Input Dialog")
  await page.getByText("Create New Input").click()
  await page.getByText("DataSet Query").click()

  console.log("Fill the form")
  const queryName = 'QuErY' + (Math.random() * 1e18)
  console.log("Create query: ", queryName);

  await page.locator('div').filter({ hasText: /^\*?NameEnter a unique name for the data input$/ }).locator('[data-test="textbox"]').fill(queryName);
  await page.locator('div').filter({ hasText: /^\*?IntervalTime interval of input in seconds\.$/ }).locator('[data-test="textbox"]').fill("60")
  await page.locator('form div').filter({ hasText: '*Start TimeRelative time to query back. Use short form relative time, e.g.: 24h ' }).locator('[data-test="textbox"]').fill("60m")
  await page.locator('form div').filter({ hasText: 'End TimeIf left blank, present time at query execution is used. If defined, use ' }).locator('[data-test="textbox"]').fill("1m")
  await page.locator('form div').filter({ hasText: 'DataSet Query StringIf left blank, all records (limited by max count) are retrie' }).locator('[data-test="textbox"]').fill("serverHost = *")
  await page.locator('div').filter({ hasText: /^ColumnsIf left blank, all columns are returned\.$/ }).locator('[data-test="textbox"]').fill("")
  await page.locator('form div').filter({ hasText: 'Max CountSpecifies the maximum number of records to return. If left blank, the d' }).locator('[data-test="textbox"]').fill("13")

  await page.getByLabel("Select a value").click();
  await page.locator('[data-test="option"]').first().click();

  await page.screenshot({ path: 'playwright-screenshots/page-inputs-filled-form.png', fullPage: true });

  // Click on Add
  console.log("Submit the form");
  const locAddConfirm = page.locator('[data-test="footer"]').getByRole('button', { name: 'Add' })
  await locAddConfirm.click();

  // check that the account is there
  console.log("Check that query is there: ", queryName);
  await page.getByRole('cell', { name: queryName }).click()
  await page.screenshot({ path: 'playwright-screenshots/page-inputs-added.png', fullPage: true });

  // go to the Splunk search App
  console.log("Go to the Splunk search page");
  await page.getByRole('button', { name: 'Apps ▾' }).click();
  await page.getByText("Search & Reporting").click()

  await expect(page).toHaveURL(/search\/search/);
  await expect(page).toHaveTitle(/Search/);
  await page.waitForTimeout(5000);
  await page.screenshot({ path: 'playwright-screenshots/page-inputs-search-page.png', fullPage: true });

  const locPopup1 = page.getByRole("link", {name: "Skip", exact: true})
  const popup1Count = await locPopup1.count()
  console.log("Is there popup - 'Skip'? " + popup1Count);
  if (popup1Count > 0) {
    locPopup1.click()
  }

  const locPopup2 = page.getByRole("button", {name: "Skip tour", exact: true})
  const popup2Count = await locPopup2.count()
  console.log("Is there popup - 'Skip tour'? " + popup2Count);
  if (popup2Count > 0) {
    locPopup2.click()
  }

  await page.getByRole('textbox', { name: 'Search' }).fill(`source="dataset_query://${queryName}"`);

  await page.getByLabel("Search Button").click();

  await page.waitForTimeout(5000)

  expect(page.getByText("sourcetype")).toHaveCount(14);

});
