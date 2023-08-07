import { test, expect } from '@playwright/test';
test.beforeEach(async ({ page }) => {
  const { SPLUNK_USER: user, SPLUNK_PASSWORD: password, CREATE_ACCOUNT: createAccount } = process.env;

  // Login
  await page.goto('/');
  await page.getByPlaceholder('Username').fill(user || 'AAAA');
  await page.getByPlaceholder('Password',  { exact: true }).fill(password || 'BBBB');
  await page.getByRole('button', { name: 'Sign In' }).click();

  await page.getByLabel('Security Data Lake Add-On for Splunk').click()

  console.log("Create account: ", createAccount, ", set to true to create account")
  if ( createAccount == 'true') {
    // Go to configuration
    await page.goto('/en-GB/app/TA_dataset/configuration');

    // Check that we are on the configuration page
    await expect(page).toHaveTitle(/Configuration/);

    // Open dialog
    const locAddDialog = page.locator('#accountTab').getByRole('button', { name: 'Add' });
    await locAddDialog.click();

    // Setup locators
    const locAccount = page.locator('div').filter({ hasText: /^Account nameEnter a unique name for this account\.$/ }).locator('[data-test="textbox"]');
    const locUrl = page.locator('div').filter({ hasText: /^URLEnter DataSet URL\.$/ }).locator('[data-test="textbox"]');
    const locReadKey = page.locator('[data-test="body"] form div').filter({ hasText: 'DataSet Log Read Access KeyRequired to enable inputs and SPL comand. Include tra' }).locator('[data-test="textbox"]');
    const locWriteKey = page.locator('[data-test="body"] form div').filter({ hasText: 'DataSet Log Write Access KeyRequired to enable alert action. Include trailing hy' }).locator('[data-test="textbox"]');

    // Read env with values
    const { DATASET_URL: datasetUrl, DATASET_LOG_ACCESS_READ: datasetReadKey, DATASET_LOG_ACCESS_WRITE: datasetWriteKey } = process.env;

    // Fill in values
    const accountName = 'QaTr' + (Math.random() * 1e18)
    await locAccount.fill(accountName);
    await locUrl.fill(datasetUrl || '');
    await locReadKey.fill(datasetReadKey || '');
    await locWriteKey.fill(datasetWriteKey || '');

    // Click on Add
    const locAddConfirm = page.locator('[data-test="footer"]').getByRole('button', { name: 'Add' })
    await locAddConfirm.click();

    // await page.getByLabel(accountName).click()
  }
});

test('Check example page', async ({ page }) => {
  await page.goto('en-GB/app/TA_dataset/dataset_by_example');


  await expect(page).toHaveTitle(/DataSet by Example/);

  // Wait for the "Waiting for data..." text to disappear
  await page.waitForFunction(() => {
    const element = document.querySelector('body');
    return !element.textContent.includes('Waiting for data...');
  });

  // Wait for few seconds more
  await page.waitForTimeout(2000);

  // Check if the page does not contain the text "No results found."
  const containsNoResults = await page.$eval('body', (element) => {
    return element.textContent.includes('No results found.');
  });

  if (containsNoResults) {
    test.fail();
  }

  const containsSearchFailed = await page.$eval('body', (element) => {
    return element.textContent.includes('External search command exited unexpectedly');
  });


  if (containsSearchFailed) {
    test.fail();
  }

  const { WAIT_FOR_HUMAN_TO_CHECK_IN_MS: waitForHumanStr} = process.env
  const waitForHumanMs = parseInt(waitForHumanStr || '0');
  console.log("Waiting for human for: ", waitForHumanMs);

  await page.waitForTimeout(waitForHumanMs);
});
