// Cloudflare Pages Function: send every *.pages.dev hostname (production alias and
// deployment previews) to the custom domain with a permanent redirect, so the
// pages.dev copy is neither indexed nor counted as site traffic.
const CANONICAL_HOST = "cflien.me";

export const onRequest = async ({ request, next }) => {
  const url = new URL(request.url);
  if (url.hostname.endsWith(".pages.dev")) {
    url.hostname = CANONICAL_HOST;
    url.protocol = "https:";
    url.port = "";
    return Response.redirect(url.toString(), 301);
  }
  return next();
};
