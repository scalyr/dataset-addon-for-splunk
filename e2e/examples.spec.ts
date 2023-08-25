import { test, expect } from '@playwright/test';
import { goToDataSetExamplesPage, waitForSearchResults } from './utils';

test('Check example page', async ({ page }) => {
  await goToDataSetExamplesPage(page);
  // wait for elements to load
  await expect(page.getByRole("main").getByText("4. Timeseries Query: This will calculate numeric values over time.")).toHaveCount(1)

  await waitForSearchResults(page, "examples");

  await page.screenshot({ path: 'playwright-screenshots/page-examples-after-checks.png', fullPage: true });
});
