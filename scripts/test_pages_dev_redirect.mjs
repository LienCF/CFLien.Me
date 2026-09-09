// Behaviour test for functions/_middleware.js: *.pages.dev must 301 to cflien.me,
// the custom domain must pass through untouched. Run with: node scripts/test_pages_dev_redirect.mjs
import assert from "node:assert/strict";
import { onRequest } from "../functions/_middleware.js";

const passThrough = new Response("origin");
const next = async () => passThrough;

async function run(url) {
  return onRequest({ request: new Request(url), next });
}

let response = await run("https://cflien-me.pages.dev/2026/07/aws-summit/?utm=1");
assert.equal(response.status, 301);
assert.equal(
  response.headers.get("location"),
  "https://cflien.me/2026/07/aws-summit/?utm=1",
  "path and query must be preserved",
);

response = await run("https://cb0e281.cflien-me.pages.dev/tags/cursor/");
assert.equal(response.status, 301, "deployment preview hostnames must redirect too");
assert.equal(response.headers.get("location"), "https://cflien.me/tags/cursor/");

response = await run("https://cflien.me/");
assert.equal(response, passThrough, "custom domain must not be redirected");

response = await run("http://localhost:8788/");
assert.equal(response, passThrough, "local wrangler dev must not be redirected");

console.log("pages.dev redirect middleware: all assertions passed");
