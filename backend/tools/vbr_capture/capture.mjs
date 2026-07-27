import { chromium } from 'playwright-core';
import { mkdir, rename, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const appDirectory = path.resolve(scriptDirectory, '../../app');
const captureRoot = path.join(appDirectory, '.vbr-pages');
const outputDirectory = path.join(captureRoot, 'latest');
const profileDirectory = path.join(appDirectory, '.vbr-browser-profile');
const headless = process.argv.includes('--headless');

const catalogs = [
  { category: 'deposit', path: 'deposity' },
  { category: 'credit', path: 'kredity' },
  { category: 'mortgage', path: 'ipoteka' },
  { category: 'credit_card', path: 'kreditnyekarty' },
  { category: 'debit_card', path: 'debetovyekarty' },
];

const supportedBankAliases = new Set([
  'jusan-kz',
  'altyn-bank-kz',
  'bcc-kz',
  'rbk-kz',
  'sberbank-kz',
  'eurasian-bank',
  'fortebank',
  'freedom-finance-bank',
  'halyc-bank',
  'hoym-kredit-kz',
  'kaspi-bank-kz',
  'kzi-bank',
  'nurbank-kz',
  'otbasi-bank-kz',
  'vtb--kazahstan-',
]);

await mkdir(captureRoot, { recursive: true });
if (existsSync(outputDirectory)) {
  const backup = path.join(captureRoot, `previous-${new Date().toISOString().replaceAll(':', '-')}`);
  await rename(outputDirectory, backup);
}
await mkdir(path.join(outputDirectory, 'catalog'), { recursive: true });
await mkdir(path.join(outputDirectory, 'details'), { recursive: true });
await mkdir(profileDirectory, { recursive: true });

const context = await chromium.launchPersistentContext(profileDirectory, {
  channel: 'chrome',
  headless,
  viewport: { width: 1440, height: 1000 },
  locale: 'ru-KZ',
  timezoneId: 'Asia/Almaty',
  ignoreDefaultArgs: ['--enable-automation'],
  args: ['--disable-blink-features=AutomationControlled'],
});
const page = context.pages()[0] || await context.newPage();
const manifest = {
  version: 1,
  source: 'vbr',
  captured_at: new Date().toISOString(),
  completed: false,
  catalogs: [],
  products: [],
};

try {
  const products = new Map();
  for (const catalog of catalogs) {
    const files = [];
    const seenInCategory = new Set();
    for (let pageNumber = 1; pageNumber <= 20; pageNumber += 1) {
      const url = new URL(`https://www.vbr.kz/banki/${catalog.path}/`);
      if (pageNumber > 1) url.searchParams.set('page', String(pageNumber));
      await page.goto(url.href, { waitUntil: 'domcontentloaded', timeout: 60_000 });
      await waitForCatalog(page, headless, pageNumber === 1);

      const cards = await page.locator('.product-card-item[data-product-id][data-organization-id]').evaluateAll(
        (elements) => elements.map((card) => {
          const link = card.querySelector('.product-card-title-link[href]');
          return {
            source_product_id: card.dataset.productId || '',
            source_alias: card.dataset.productAlias || '',
            source_url: link?.href || '',
            external_bank_id: card.dataset.organizationId || '',
            external_bank_alias: card.dataset.organizationAlias || '',
            external_bank_name: card.dataset.organizationName || '',
          };
        }).filter((item) => item.source_product_id && item.source_url),
      );
      const freshCards = cards.filter((item) => !seenInCategory.has(item.source_product_id));
      if (pageNumber > 1 && freshCards.length === 0) break;
      if (pageNumber === 1 && cards.length === 0) {
        throw new Error(`No products found in ${url.href}`);
      }

      const relativeFile = `catalog/${catalog.category}-page-${pageNumber}.html`;
      await writeFile(path.join(outputDirectory, relativeFile), await page.content(), 'utf8');
      files.push(relativeFile);
      for (const item of freshCards) {
        seenInCategory.add(item.source_product_id);
        if (!supportedBankAliases.has(item.external_bank_alias)) continue;
        products.set(`${catalog.category}:${item.source_product_id}`, {
          ...item,
          category: catalog.category,
          detail_file: null,
        });
      }
    }
    manifest.catalogs.push({ category: catalog.category, files });
  }

  let completedDetails = 0;
  for (const product of products.values()) {
    completedDetails += 1;
    process.stdout.write(`\rDetails ${completedDetails}/${products.size}`);
    await page.goto(product.source_url, { waitUntil: 'domcontentloaded', timeout: 60_000 });
    await page.waitForTimeout(800);
    const bodyText = await page.locator('body').innerText();
    if (bodyText.includes('доступ заблокирован')) {
      throw new Error(`VBR blocked the detail page: ${product.source_url}`);
    }
    const relativeFile = `details/${product.category}-${product.source_product_id}.html`;
    await writeFile(path.join(outputDirectory, relativeFile), await page.content(), 'utf8');
    product.detail_file = relativeFile;
  }
  process.stdout.write('\n');

  manifest.products = [...products.values()];
  manifest.completed = true;
  await writeFile(
    path.join(outputDirectory, 'manifest.json'),
    JSON.stringify(manifest, null, 2),
    'utf8',
  );
  console.log(`Capture completed: ${outputDirectory}`);
  console.log(`Products captured: ${manifest.products.length}`);
} finally {
  await context.close();
}

async function waitForCatalog(page, isHeadless, productsRequired) {
  await page.waitForTimeout(1500);
  for (let attempt = 0; attempt < 60; attempt += 1) {
    const bodyText = await page.locator('body').innerText();
    const productCount = await page.locator('.product-card-item[data-product-id]').count();
    if (productCount > 0) return;
    if (!bodyText.includes('доступ заблокирован')) {
      if (!productsRequired) return;
      await page.waitForTimeout(1000);
      continue;
    }
    if (isHeadless) {
      throw new Error('VBR blocked the saved session. Run capture without --headless once.');
    }
    console.log('Complete the VBR browser check in the opened Chrome window.');
    await page.waitForTimeout(2000);
  }
  throw new Error('VBR catalog did not become available within two minutes.');
}
