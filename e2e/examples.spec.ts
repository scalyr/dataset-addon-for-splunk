import { test, expect } from '@playwright/test';
import { goToDataSet } from './utils';

test.beforeEach(async ({ page }) => {
  await page.goto('/');

  await goToDataSet(page);
});


test('Check example page', async ({ page }) => {
  console.log("Go to example page");
  await page.locator('[title="DataSet by Example"]').click();


  await expect(page).toHaveTitle(/DataSet by Example/);

  // wait for elements to load
  await expect(page.getByRole("main").getByText("4. Timeseries Query: This will calculate numeric values over time.")).toHaveCount(1)

  // Wait for the "Waiting for data..." text to disappear
  console.log("Wait for 'Waiting for data' to disappear")
  await page.screenshot({ path: 'playwright-screenshots/page-examples-before-waiting-for-data.png', fullPage: true });
  await expect(page.getByText(/Waiting for data/)).toHaveCount(0, {timeout: 15000});

  await page.screenshot({ path: 'playwright-screenshots/page-examples-before-checks.png', fullPage: true });

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

  await page.screenshot({ path: 'playwright-screenshots/page-examples-after-checks.png', fullPage: true });
});
