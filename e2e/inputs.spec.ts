import { test, expect } from '@playwright/test';
import { goToDataSet, goToInputs, waitForData } from './utils';

test.beforeEach(async ({ page }) => {
  await page.goto('/');

  await goToDataSet(page);
  await goToInputs(page);
});


test('Check inputs page', async ({ page }) => {
  await page.screenshot({ path: 'playwright-screenshots/page-inputs-after-checks.png', fullPage: true });
});
