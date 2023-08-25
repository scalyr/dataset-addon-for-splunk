import {test, expect, Page} from '@playwright/test';
import {searchDataSet} from './utils';
import {setTimeout} from 'timers/promises';

test('Verify SDL addon is deployed properly', async ({page}) => {
    await page.goto('/');
    await page.screenshot({ path: 'playwright-screenshots/splunk-launcher-page.png', fullPage: true });
    const sdlAddonLinks = page.getByLabel('Navigate to Security Data Lake Add-On for Splunk app');
    await expect(sdlAddonLinks).toHaveCount(1);

    console.log("Go to DataSet page")
    await sdlAddonLinks.click();
    await page.screenshot({ path: 'playwright-screenshots/dataset-addon-home.png', fullPage: true });
    const inputLinks = page.getByRole('link', {name: 'Input'});
    await expect(inputLinks).toHaveCount(1);
    await expect(inputLinks.first()).toHaveAttribute('href','/en-US/app/TA_dataset/inputs');
    const configLinks = page.getByRole('link', {name: 'Configuration'});
    await expect(configLinks).toHaveCount(1);
    await expect(configLinks.first()).toHaveAttribute('href','/en-US/app/TA_dataset/configuration');
    const exampleLinks = page.getByRole('link', {name: 'DataSet by Example'});
    await expect(exampleLinks).toHaveCount(1);
    await expect(exampleLinks.first()).toHaveAttribute('href','/en-US/app/TA_dataset/dataset_by_example');
    const searchLinks = page.getByRole('link', {name: 'Search'});
    await expect(searchLinks).toHaveCount(1);
    await expect(searchLinks.first()).toHaveAttribute('href','/en-US/app/TA_dataset/search');
});
