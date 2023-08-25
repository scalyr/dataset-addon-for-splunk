import {test, expect, Page} from '@playwright/test';
import {searchDataSet} from './utils';
import {setTimeout} from 'timers/promises';

test('Verify SDL addon is deployed properly', async ({page}) => {
    await page.goto('/');
    await page.screenshot({ path: 'playwright-screenshots/splunk-launcher-page.png', fullPage: true });
    const sdlAddonLink = page.getByLabel('Navigate to Security Data Lake Add-On for Splunk app');
    await expect(sdlAddonLink).toHaveCount(1);

    console.log("Go to DataSet page")
    await sdlAddonLink.click();
    await page.screenshot({ path: 'playwright-screenshots/dataset-addon-home.png', fullPage: true });
    await expect(page.getByLabel('Inputs')).toHaveCount(1);
    await expect(page.getByLabel('Configuration')).toHaveCount(1);
    await expect(page.getByLabel('DataSet by Example')).toHaveCount(1);
    await expect(page.getByLabel('Search')).toHaveCount(1);
});
