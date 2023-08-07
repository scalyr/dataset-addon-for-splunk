import { test as setup, expect } from '@playwright/test';

setup('do login', async ({ page }) => {

    const { SPLUNK_USER: user, SPLUNK_PASSWORD: password } = process.env;

    await page.goto('/');
    await page.getByLabel('User Name').fill('user');
    await page.getByLabel('Password').fill('password');
    await page.getByText('Sign in').click();

    // Wait until the page actually signs in.
    await expect(page.getByText('Hello, user!')).toBeVisible();
  });
