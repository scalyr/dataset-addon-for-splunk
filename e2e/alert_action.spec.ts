import {test, expect, Page} from '@playwright/test';
import {searchDataSet} from './utils';
import {setTimeout} from 'timers/promises';

test('Alert action - create and delete alert with results propagation to DataSet', async ({page}) => {
    test.setTimeout(120000); //default 60s may time out since job are scheduled for every 60s
    const serverHost = 'dataset_addon_for_splunk_playwright_CI_CD_e2e_test_host';
    const alertName = 'splunk_addon_test_alert_'+ Math.random().toString(36).substring(2,7);
    await removeAlertIfExists(page, alertName);

    await searchDataSet(page, "| dataset");
    await saveAsAlertWithDataSetTrigger(page, alertName, serverHost);

    // verify splunk alert results in DataSet
    await setTimeout(60000); // wait for alert job to be triggered (cron job every 1 minute)
    await searchDataSet(page, "| dataset search=\"serverHost='" + serverHost + "' '" + alertName + "'\"");
    await page.screenshot({path: `playwright-screenshots/page-search-query-splunk-alert-results-from_dataset.png`, fullPage: true});

    await removeAlertIfExists(page, alertName);
});

async function saveAsAlertWithDataSetTrigger(page: Page, alertName: string, serverHost: string) {
    console.log("Open Save As Alert Dialog")
    await page.getByText("Save As").click();
    await page.getByRole('link', {name: 'Alert'}).click();

    console.log("Fill in Alert Dialog - general");
    await page.locator('[name="name"]').fill(alertName);
    await page.getByRole('link', {name: 'Run every week'}).click();
    await page.getByRole('link', {name: 'Run on Cron Schedule'}).click();
    await page.locator('[name="cron_schedule"]').fill("*/1 * * * *"); // run every minute
    // by default triggered if num of results > 0
    await page.screenshot({path: `playwright-screenshots/page-alert-dialog-general.png`, fullPage: true});

    console.log("Add trigger action - Dataset");
    await page.getByText("+ Add Actions").click();
    await page.getByText("Send to DataSet").click();
    await page.screenshot({path: `playwright-screenshots/page-alert-dialog-dataset-trigger.png`, fullPage: true});
    await expect(page.getByLabel(`ServerHost`)).toBeVisible();
    await expect(page.getByLabel(`DataSet Message`)).toBeVisible();
    await expect(page.getByLabel(`Severity`)).toBeVisible();

    console.log("Fill in Alert Dialog - trigger DataSet event");
    await setTimeout(500); // wait for select option to be populated
    await page.locator('[name="action.dataset_event.param.account"]').locator('button').click();
    await page.locator('[data-test="option"]').first().click(); // select first account
    await page.locator('[name="action.dataset_event.param.dataset_serverhost"]').fill(serverHost)
    await page.screenshot({path: `playwright-screenshots/page-alert-dialog-dataset-trigger-filled.png`, fullPage: true});

    await page.getByRole('button', {name: 'Save'}).click();
    await page.screenshot({path: `playwright-screenshots/page-alert-dialog-saved.png`, fullPage: true});
}

async function removeAlertIfExists(page: Page, alertName: string) {
    console.log("View Alerts");
    await page.goto('/en-US/app/TA_dataset/saved/searches');
    await page.screenshot({path: `playwright-screenshots/page-alerts-list.png`, fullPage: true});

    const alertRow = page.getByRole("row").filter({hasText: alertName})
    if (await alertRow.count() == 0) {
        console.log(alertName + " alert does not exists")
    } else {
        console.log("Deleting " + alertName + " alert")
        await alertRow.getByRole('link', {name: 'Edit'}).click();
        await page.getByRole('link', {name: 'Delete'}).click();
        await page.getByRole('link', {name: 'Delete'}).click();
        await page.screenshot({path: `playwright-screenshots/page-alerts-deleted.png`, fullPage: true});
    }
}
