import { test, expect, Page } from '@playwright/test';
import {waitForData, query2file, searchDataSet, goToDataSetSearchPage} from './utils';

test.beforeEach(async ({ page }) => {
  await goToDataSetSearchPage(page);
});


test('Simple search - dataset', async ({ page }) => {
  await searchDataSet(page, "| dataset");

  await page.screenshot({ path: 'playwright-screenshots/page-search-simple-search-dataset.png', fullPage: true });
});

test('Simple search - s1query', async ({ page }) => {
  await searchDataSet(page, "| s1query");

  await page.screenshot({ path: 'playwright-screenshots/page-search-simple-search-s1query.png', fullPage: true });
});

async function searchFor(page: Page, query: string, maxCount: number | undefined = undefined) {
  if (maxCount === undefined) {
    maxCount = Math.ceil(1000 * Math.random()) % 10 + 5;
  }

  const finalQuery = `${query} maxcount=${maxCount}`

  console.log(`Searching for '${finalQuery}', original was: ${query}`);

  await page.getByRole('textbox', { name: 'Search' }).fill(finalQuery);

  await page.getByLabel("Search Button").click();

  await waitForData(page, query2file(query))

  await expect(page.getByText(`Events (${maxCount})`)).toHaveCount(1);
}
