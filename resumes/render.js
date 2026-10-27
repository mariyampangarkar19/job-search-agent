// Renders each resume HTML to a one-page A4 PDF, shrinking the font until it fits.
const { chromium } = require('playwright');
const fs = require('fs');

const MM = 96 / 25.4;
const PAGE_W = (210 - 26) * MM; // A4 minus left/right @page margins
const PAGE_H = (297 - 22) * MM; // A4 minus top/bottom @page margins

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: Math.floor(PAGE_W), height: 1200 } });
  for (const { src, dst } of jobs) {
    await page.goto('file://' + src);
    let fs_ = 11.4;
    while (fs_ > 9.0) {
      await page.evaluate(v => document.documentElement.style.setProperty('--fs', v + 'pt'), fs_);
      const h = await page.evaluate(() => document.body.scrollHeight);
      if (h <= PAGE_H - 4) break;
      fs_ = Math.round((fs_ - 0.1) * 10) / 10;
    }
    await page.emulateMedia({ media: 'print' });
    await page.pdf({ path: dst, format: 'A4', preferCSSPageSize: true, printBackground: true });
    console.log(`${dst.split('/').slice(-2).join('/')}  font ${fs_}pt`);
  }
  await browser.close();
})();
