import {test, expect, Page} from '@playwright/test';
import {searchDataSet} from './utils';
import {setTimeout} from 'timers/promises';

test('Verify SDL addon is deployed properly', async ({page}) => {
    await page.goto('/');
    await page.screenshot({ path: 'playwright-screenshots/splunk-launcher-page.png', fullPage: true });
    const sdlAddonLinks = page.getByLabel('Navigate to Singularity Data Lake Add-On for Splunk app');
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

    // Now that add-on contains multiple dashboards, they don't show under main menu item anymore, but
    // under "Dashboards" meni item which on click opens a new menu bar
    const dashboardsLinks = page.getByRole('link', {name: 'Dashboards'});
    await expect(dashboardsLinks).toHaveCount(1);

    const searchLinks = page.getByRole('link', {name: 'Search'});
    await expect(searchLinks).toHaveCount(1);
    await expect(searchLinks.first()).toHaveAttribute('href','/en-US/app/TA_dataset/search');

    // Verify all built-in dashboards are present
    console.log("Go to Dashboards page");
    await page.goto('/app/TA_dataset/dashboards');

    await expect(page.getByRole('link', {name: 'Ingestion Summary'})).toHaveCount(1);
    await expect(page.getByRole('link', {name: 'SentinelOne Use Case Query Examples'})).toHaveCount(1);
    await expect(page.getByRole('link', {name: 'Singularity Data Lake by Example'})).toHaveCount(1);
    await expect(page.getByRole('link', {name: 'SOC Search Examples'})).toHaveCount(1);
    await expect(page.getByRole('link', {name: 'Splunk App Usage'})).toHaveCount(1);
});
