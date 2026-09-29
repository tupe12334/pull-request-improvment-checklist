// Parse every flow.mmd with the Mermaid version installed, so a label that
// breaks GitHub's renderer fails CI instead of the rendered diagram.
import { JSDOM } from 'jsdom';
import fs from 'node:fs';
import path from 'node:path';

const dom = new JSDOM('<body></body>');
globalThis.window = dom.window;
globalThis.document = dom.window.document;
const { default: mermaid } = await import('mermaid');

const root = '.steplock/checklists';
let failed = false;
for (const name of fs.readdirSync(root)) {
  const file = path.join(root, name, 'flow.mmd');
  if (!fs.existsSync(file)) continue;
  try {
    await mermaid.parse(fs.readFileSync(file, 'utf8'));
    console.log(`ok   ${file}`);
  } catch (e) {
    console.log(`FAIL ${file}\n${e.message}`);
    failed = true;
  }
}
process.exit(failed ? 1 : 0);
