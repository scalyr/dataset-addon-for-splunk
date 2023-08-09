import { test, expect } from '@playwright/test';
import exp from 'constants';
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
  await page.waitForTimeout(5000);

  await page.screenshot({ path: 'playwright-screenshots/page-after-login-before-pop-up.png', fullPage: true });

  // Confirm some pop-up
  const locGotIt = page.getByTestId('instrumentation-opt-in-modal').locator('[data-test="button"]');
  const countGotIt = await locGotIt.count()
  console.log("Check for popup: ", countGotIt);
  if (countGotIt > 0) {
    await locGotIt.click();
  }

  await page.screenshot({ path: 'playwright-screenshots/page-after-login-after-pop-up.png', fullPage: true });

  await page.getByLabel('Navigate to Security Data Lake Add-On for Splunk app').click()
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
  while (true) {
    const waitingCount = await page.getByText(/Waiting for data/).count();
    console.log("Waiting for data: ", waitingCount);
    if (waitingCount == 0) {
      break;
    }

    await page.waitForTimeout(1000);
  }
  await page.screenshot({ path: 'playwright-screenshots/page-examples-before-checks.png', fullPage: true });

  // Check if the page does not contain the text "No results found."
  const noResultsCount = await page.getByText(/No results found/).count();
  console.log("Page contains 'No results found': ", noResultsCount)
  expect(noResultsCount).toBe(0);

  // Check if the page does not contain the text "No results found."
  const searchFailedCount = await page.getByText(/External search command exited unexpectedly/).count();
  console.log("Page contains 'External search command exited unexpectedly': ", noResultsCount)
  expect(searchFailedCount).toBe(0);

  const { WAIT_FOR_HUMAN_TO_CHECK_IN_MS: waitForHumanStr} = process.env
  const waitForHumanMs = parseInt(waitForHumanStr || '0');
  console.log("Waiting for human for: ", waitForHumanMs);

  await page.waitForTimeout(waitForHumanMs);

  await page.screenshot({ path: 'playwright-screenshots/page-examples-after-checks.png', fullPage: true });
});
