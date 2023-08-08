import { test, expect } from '@playwright/test';
test.beforeEach(async ({ page }) => {
  const { SPLUNK_USER: user, SPLUNK_PASSWORD: password, CREATE_ACCOUNT: createAccount } = process.env;


  // Login
  await page.goto('/');
  await page.screenshot({ path: 'playwright-screenshots/page-login.png', fullPage: true });

  console.log("Fill in login form");
  await page.getByPlaceholder('Username').fill(user || 'SPLUNK_USER env is empty');
  await page.getByPlaceholder('Password',  { exact: true }).fill(password || 'SPLUNK_PASSWORD env is empty');
  await page.getByRole('button', { name: 'Sign In' }).click();

    // Wait for few seconds more
  await page.waitForTimeout(10000);

  await page.screenshot({ path: 'playwright-screenshots/page-after-login-before-pop-up.png', fullPage: true });

  // Confirm some pop-up
  const locGotIt = page.getByRole('button', {name: 'Got it!'});
  const countGotIt = await locGotIt.count()
  console.log("Check for popup: ", countGotIt);
  if (countGotIt > 0) {
    await locGotIt.click();
  }

  await page.screenshot({ path: 'playwright-screenshots/page-after-login-after-pop-up.png', fullPage: true });

  await page.getByLabel('Security Data Lake Add-On for Splunk', { exact: true }).click()
  await page.screenshot({ path: 'playwright-screenshots/page-home.png', fullPage: true });

  console.log("Create account: ", createAccount, ", set to true to create account")
  if ( createAccount == 'true') {
    // Go to configuration
    console.log("Go to configuration page");
    await page.locator('[title="Configuration"]').click();
    await page.screenshot({ path: 'playwright-screenshots/page-configuration.png', fullPage: true });

    // Check that we are on the configuration page
    await expect(page).toHaveTitle(/Configuration/);

    // Open dialog
    console.log("Open dialog for adding an account");
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
    console.log("Fill in account information");
    const accountName = 'QaTr' + (Math.random() * 1e18)
    await locAccount.fill(accountName);
    await locUrl.fill(datasetUrl || '');
    await locReadKey.fill(datasetReadKey || '');
    await locWriteKey.fill(datasetWriteKey || '');


    // Click on Add
    console.log("Submit the form");
    const locAddConfirm = page.locator('[data-test="footer"]').getByRole('button', { name: 'Add' })
    await locAddConfirm.click();

    // await page.getByLabel(accountName).click()
  }
});

test('Check example page', async ({ page }) => {
  console.log("Go to example page");
  await page.locator('[title="DataSet by Example"]').click();


  await expect(page).toHaveTitle(/DataSet by Example/);

  // Wait for text to appear
  await page.waitForTimeout(2000);

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

  await page.screenshot({ path: 'playwright-screenshots/page-examples.png', fullPage: true });
});
