import { test, expect } from '@playwright/test';
import { goToDataSetPage, goToExamples, waitForData } from './utils';

test.beforeEach(async ({ page }) => {
  await page.goto('/');

  await goToDataSetPage(page);
  await goToExamples(page);
});


test('Check example page', async ({ page }) => {
  // wait for elements to load
  await expect(page.getByRole("main").getByText("4. Timeseries Query: This will calculate numeric values over time.")).toHaveCount(1)

  await waitForData(page, "examples");

  await page.screenshot({ path: 'playwright-screenshots/page-examples-after-checks.png', fullPage: true });
});
