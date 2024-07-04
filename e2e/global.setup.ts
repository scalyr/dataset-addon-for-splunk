import { join as pjoin } from 'path';
import { test as setup, expect } from '@playwright/test';
import { goToDataSetPage, goToDataSetConfigurationPage } from './utils';

export const STORAGE_STATE = pjoin(__dirname, '.auth.json');

// TODO: this file is ignored, a
setup('login and create account', async ({ page }) => {
  const { SPLUNK_USER: user, SPLUNK_PASSWORD: password, CREATE_ACCOUNT: createAccount } = process.env;

  console.log("Check whether credentials were provided");
  expect(user).toBeTruthy();
  expect(password).toBeTruthy();

  console.log("Go to homepage");
  await page.goto('/');
  await page.screenshot({ path: 'playwright-screenshots/page-login.png', fullPage: true });

  console.log("Fill in login form");
  await page.getByPlaceholder('Username').fill(user || 'SPLUNK_USER env is empty');
  await page.getByPlaceholder('Password',  { exact: true }).fill(password || 'SPLUNK_PASSWORD env is empty');
  await page.getByRole('button', { name: 'Sign In' }).click();

  console.log("Wait for homepage to load");
  await expect(page).toHaveTitle(/Home/);

  await page.screenshot({ path: 'playwright-screenshots/page-after-login-before-pop-up.png', fullPage: true });

  console.log("Store state to be able to reuse login");
  await page.context().storageState({ path: STORAGE_STATE });

  await page.waitForTimeout(2000);
  // Confirm some pop-up
  const locGotIt = page.getByTestId('instrumentation-opt-in-modal').locator('[data-test="button"]');
  const countGotIt = await locGotIt.count()
  console.log("Check for popup: ", countGotIt);
  if (countGotIt > 0) {
    console.log("Close the popup");
    await locGotIt.click();
  }

  await page.screenshot({ path: 'playwright-screenshots/page-after-login-after-pop-up.png', fullPage: true });

  await goToDataSetPage(page);

  await page.screenshot({ path: 'playwright-screenshots/page-home.png', fullPage: true });

  await goToDataSetConfigurationPage(page);

  const accountCount = await page.getByRole("main").getByRole("row").getByText(/E2E_T/).count();
  console.log("Number of accounts: ", accountCount);
  if (accountCount == 0) {
    // Open dialog
    console.log("Open dialog for adding an account");
    const locAddDialog = page.locator('#accountTab').getByRole('button', { name: 'Add' });
    await locAddDialog.click();

    // Setup locators
    const locAccount = page.locator('div').filter({ hasText: /^\*?Account NameEnter a unique name for this account\.$/ }).locator('[data-test="textbox"]')
    const locUrl = page.locator('div').filter({ hasText: /^\*?URLEnter DataSet URL\.$/ }).locator('[data-test="textbox"]')
    const locReadKey = page.locator('[data-test="body"] form div').filter({ hasText: 'SDL Read Access Key (Legacy)Required (if no AuthN token provided) to enable' }).locator('[data-test="textbox"]');
    const locWriteKey = page.locator('[data-test="body"] form div').filter({ hasText: 'SDL Write Access Key (Legacy)Required (if no AuthN token provided) to enable alert action.' }).locator('[data-test="textbox"]');

    // Read env with values
    const { DATASET_URL: datasetUrl, DATASET_LOG_ACCESS_READ: datasetReadKey, DATASET_LOG_ACCESS_WRITE: datasetWriteKey } = process.env;

    // Fill in values
    const accountName = (('E2E_T_' + (Math.random() * 1e18))).slice(0, 15);
    console.log("Create account: ", accountName);
    await locAccount.fill(accountName);
    await locUrl.fill(datasetUrl || '');
    await locReadKey.fill(datasetReadKey || '');
    await locWriteKey.fill(datasetWriteKey || '');


    // Click on Add
    console.log("Submit the form");
    const locAddConfirm = page.locator('[data-test="footer"]').getByRole('button', { name: 'Add' })
    await locAddConfirm.click();

    // check that the account is there
    console.log("Check that account is there: ", accountName);
    await page.getByRole('cell', { name: accountName }).click()

  }
});
