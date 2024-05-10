import {test, expect} from '@playwright/test';
import {searchDataSet} from './utils';

test('Simple search - dataset', async ({ page }) => {
  await searchDataSet(page, "| dataset maxcount=5");
  await page.screenshot({ path: 'playwright-screenshots/page-search-simple-search-dataset.png', fullPage: true });
  await expect(page.getByText(`Events (5)`)).toHaveCount(0);
});

test('Simple search - s1query', async ({ page }) => {
  await searchDataSet(page, "| s1query maxcount=5");
  await page.screenshot({ path: 'playwright-screenshots/page-search-simple-search-s1query.png', fullPage: true });
  await expect(page.getByText(`Events (5)`)).toHaveCount(0);
});
