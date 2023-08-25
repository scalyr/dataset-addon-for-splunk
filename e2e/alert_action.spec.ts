import {test, expect, Page} from '@playwright/test';
import {searchDataSet} from './utils';
import {setTimeout} from 'timers/promises';

test('Alert action - create and delete alert with results propagation to DataSet', async ({page}) => {
    const serverHost = 'host_splunk';
    const alertName = 'test_alert';
    await removeAlertIfExists(page, alertName);

    await searchDataSet(page, "| dataset");
    await saveAsAlertWithDataSetTrigger(page, alertName, serverHost);
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
    await page.goto('/en-GB/app/TA_dataset/saved/searches');
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
