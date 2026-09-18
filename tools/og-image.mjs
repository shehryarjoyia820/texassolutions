// Builds assets/og-image.png (1200x630) for social sharing.
// Needs sharp: run from a folder where it is installed, e.g.
//   node --experimental-default-type=module tools/og-image.mjs
import sharp from 'sharp';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const logo = await sharp(join(root, 'assets/logo/texas-solutions-logo.png')).resize({ width: 460 }).png().toBuffer();

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630">
  <rect width="1200" height="630" fill="#f3f2f2"/>
  <rect x="0" y="0" width="18" height="630" fill="#ec3013"/>
  <rect x="80" y="470" width="1040" height="2" fill="#201e1d" opacity="0.35"/>
  <text x="80" y="300" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="64" fill="#201e1d">TRUCK DISPATCH SERVICES</text>
  <text x="80" y="378" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="46" fill="#ec3013">FOR OWNER-OPERATORS &amp; SMALL FLEETS</text>
  <text x="80" y="530" font-family="Arial, sans-serif" font-size="28" fill="#201e1d">Dry van · Reefer · Flatbed · Hotshot · Box truck · Power only</text>
  <text x="80" y="576" font-family="Arial, sans-serif" font-size="26" fill="#605d5d">dispatch.texassolutions.co  ·  (838) 910-3147  ·  No upfront cost</text>
</svg>`;

await sharp(Buffer.from(svg))
  .composite([{ input: logo, left: 80, top: 60 }])
  .png()
  .toFile(join(root, 'assets/og-image.png'));
console.log('assets/og-image.png written');
