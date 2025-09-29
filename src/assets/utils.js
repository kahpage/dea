/*
 * Some useful js definitions.
 */

import IconYouTube from "@/assets/icons/youtube.svg?raw";
import IconX from "@/assets/icons/x.svg?raw";
import IconNiconico from "@/assets/icons/niconico.svg?raw";
import IconBooth from "@/assets/icons/booth.svg?raw";
import IconSoundCloud from "@/assets/icons/soundcloud.svg?raw";
import IconPixiv from "@/assets/icons/pixiv.svg?raw";
import IconFacebook from "@/assets/icons/facebook.svg?raw";
import IconInstagram from "@/assets/icons/instagram.svg?raw";
import IconBandcamp from "@/assets/icons/bandcamp.svg?raw";

const _env_mode = import.meta.env.MODE;
const _is_prod = _env_mode == "production"; // true if build, false if dev

const PATH_PUBLIC = _is_prod ? `/dea` : `/dea`; // Path of public/ folder
const PATH_DB_TO_EXPORT = _is_prod
  ? `https://raw.githubusercontent.com/kahpage/dea_db/refs/heads/master/databases_to_export`
  : `/dea/dea_db/databases_to_export`; // Path of raw databases (media)
const PATH_DB_EXPORTED = _is_prod
  ? `https://raw.githubusercontent.com/kahpage/dea_db/refs/heads/master/databases_exported`
  : `/dea/dea_db/databases_exported`; // Path of exported databases

/*
 * Make URLs in text clickable (raw html output)
 * Will use icons for some common domains.
 */
function makeLinksClickable(text) {
  if (!text && text !== "") return "";

  // Escape characters
  const escapeHtml = (s) =>
    String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;")
      .replace(" ", "%20");
  const escapeAttr = (s) =>
    String(s)
      .replace(/&/g, "&amp;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

  // URL regex
  const urlRegex = /(https?:\/\/[^\s,]+)/g;

  // YouTube
  const isYouTube = (url) =>
    /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be\/)/i.test(url);
  const ytSvg = IconYouTube
    .replace(/width="[^"]*"/g, "")
    .replace(/height="[^"]*"/g, "")
    .replace("<svg", '<svg style="width:1em;height:1em;vertical-align:middle"');

    // x.com / twitter
  const isX = (url) =>
    /(?:https?:\/\/)?(?:www\.)?(?:x\.com\/|twitter\.com\/)/i.test(url);
  const xSvg = IconX.replace(/width="[^"]*"/g, "")
    .replace(/height="[^"]*"/g, "")
    .replace("<svg", '<svg style="width:1em;height:1em;vertical-align:middle"');

  // Niconico
  const isNiconico = (url) =>
    /(?:https?:\/\/)?(?:www\.)?(?:nicovideo\.jp)/i.test(url);
  const nicoSvg = IconNiconico.replace(/width="[^"]*"/g, "")
    .replace(/height="[^"]*"/g, "")
    .replace("<svg", '<svg style="width:1em;height:1em;vertical-align:middle"');

  // Booth.pm
  const isBooth = (url) => /(?:https?:\/\/)?(?:www\.)?(?:booth\.pm)/i.test(url);
  const boothSvg = IconBooth.replace(/width="[^"]*"/g, "")
    .replace(/height="[^"]*"/g, "")
    .replace("<svg", '<svg style="width:1em;height:1em;vertical-align:middle"');

  // SoundCloud
  const isSoundCloud = (url) =>
    /(?:https?:\/\/)?(?:www\.)?(?:soundcloud\.com)/i.test(url);
  const scSvg = IconSoundCloud.replace(/width="[^"]*"/g, "")
    .replace(/height="[^"]*"/g, "")
    .replace("<svg", '<svg style="width:1em;height:1em;vertical-align:middle"');

  // Pixiv
  const isPixiv = (url) =>
    /(?:https?:\/\/)?(?:www\.)?(?:pixiv\.net)/i.test(url);
  const pixivSvg = IconPixiv.replace(/width="[^"]*"/g, "")
    .replace(/height="[^"]*"/g, "")
    .replace("<svg", '<svg style="width:1em;height:1em;vertical-align:middle"');

  // Facebook
  const isFacebook = (url) =>
    /(?:https?:\/\/)?(?:www\.)?(?:facebook\.com)/i.test(url);
  const fbSvg = IconFacebook.replace(/width="[^"]*"/g, "")
    .replace(/height="[^"]*"/g, "")
    .replace("<svg", '<svg style="width:1em;height:1em;vertical-align:middle"');

  // Instagram // TODO: repair
  const isInstagram = (url) =>
    /(?:https?:\/\/)?(?:www\.)?(?:instagram\.com)/i.test(url);
  const igSvg = IconInstagram.replace(/width="[^"]*"/g, "")
    .replace(/height="[^"]*"/g, "")
    .replace("<svg", '<svg style="width:1em;height:1em;vertical-align:middle"');

  // Bandcamp
  const isBandcamp = (url) =>
    /(?:https?:\/\/)?(?:www\.)?(?:bandcamp\.com)/i.test(url);
  const bcSvg = IconBandcamp.replace(/width="[^"]*"/g, "")
    .replace(/height="[^"]*"/g, "")
    .replace("<svg", '<svg style="width:1em;height:1em;vertical-align:middle"');

  // Replace URLs with clickable links
  return String(text).replace(urlRegex, (url) => {
    const display = escapeHtml(url);
    const safeHref = escapeAttr(url);
    if (isYouTube(url)) {
      return `<a href="${safeHref}" target="_blank" rel="noopener noreferrer" style="display:inline-block;text-decoration:none;border-bottom:1px solid transparent;transition:border-bottom-color 0.2s;" onmouseover="this.style.borderBottomColor='currentColor'" onmouseout="this.style.borderBottomColor='transparent'">${ytSvg}<span style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden;">${display}</span></a>`;
    } else if (isX(url)) {
      return `<a href="${safeHref}" target="_blank" rel="noopener noreferrer" title="${safeHref}" style="display:inline-block;text-decoration:none;border-bottom:1px solid transparent;transition:border-bottom-color 0.2s;" onmouseover="this.style.borderBottomColor='currentColor'" onmouseout="this.style.borderBottomColor='transparent'">${xSvg}<span style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden;">${display}</span></a>`;
    } else if (isNiconico(url)) {
      return `<a href="${safeHref}" target="_blank" rel="noopener noreferrer" title="${safeHref}" style="display:inline-block;text-decoration:none;border-bottom:1px solid transparent;transition:border-bottom-color 0.2s;" onmouseover="this.style.borderBottomColor='currentColor'" onmouseout="this.style.borderBottomColor='transparent'">${nicoSvg}<span style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden;">${display}</span></a>`;
    } else if (isBooth(url)) {
      return `<a href="${safeHref}" target="_blank" rel="noopener noreferrer" title="${safeHref}" style="display:inline-block;text-decoration:none;border-bottom:1px solid transparent;transition:border-bottom-color 0.2s;" onmouseover="this.style.borderBottomColor='currentColor'" onmouseout="this.style.borderBottomColor='transparent'">${boothSvg}<span style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden;">${display}</span></a>`;
    } else if (isSoundCloud(url)) {
      return `<a href="${safeHref}" target="_blank" rel="noopener noreferrer" title="${safeHref}" style="display:inline-block;text-decoration:none;border-bottom:1px solid transparent;transition:border-bottom-color 0.2s;" onmouseover="this.style.borderBottomColor='currentColor'" onmouseout="this.style.borderBottomColor='transparent'">${scSvg}<span style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden;">${display}</span></a>`;
    } else if (isPixiv(url)) {
      return `<a href="${safeHref}" target="_blank" rel="noopener noreferrer" title="${safeHref}" style="display:inline-block;text-decoration:none;border-bottom:1px solid transparent;transition:border-bottom-color 0.2s;" onmouseover="this.style.borderBottomColor='currentColor'" onmouseout="this.style.borderBottomColor='transparent'">${pixivSvg}<span style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden;">${display}</span></a>`;
    } else if (isFacebook(url)) {
      return `<a href="${safeHref}" target="_blank" rel="noopener noreferrer" title="${safeHref}" style="display:inline-block;text-decoration:none;border-bottom:1px solid transparent;transition:border-bottom-color 0.2s;" onmouseover="this.style.borderBottomColor='currentColor'" onmouseout="this.style.borderBottomColor='transparent'">${fbSvg}<span style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden;">${display}</span></a>`;
    } else if (isInstagram(url)) {
      return `<a href="${safeHref}" target="_blank" rel="noopener noreferrer" title="${safeHref}" style="display:inline-block;text-decoration:none;border-bottom:1px solid transparent;transition:border-bottom-color 0.2s;" onmouseover="this.style.borderBottomColor='currentColor'" onmouseout="this.style.borderBottomColor='transparent'">${igSvg}<span style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden;">${display}</span></a>`;
    } else if (isBandcamp(url)) {
      return `<a href="${safeHref}" target="_blank" rel="noopener noreferrer" title="${safeHref}" style="display:inline-block;text-decoration:none;border-bottom:1px solid transparent;transition:border-bottom-color 0.2s;" onmouseover="this.style.borderBottomColor='currentColor'" onmouseout="this.style.borderBottomColor='transparent'">${bcSvg}<span style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden;">${display}</span></a>`;
    }
    // other link
    return `<a href="${safeHref}" target="_blank" rel="noopener noreferrer">${display}</a>`;
  });
}

/*
 * Sleep for given duration in async contexts. This should be awaited.
 */
async function asyncsleep(duration_ms) {
  await new Promise((resolve) => setTimeout(resolve, duration_ms));
}

/*
 * Fetch given URL, handle callbacks.
 */
async function fetch_url({
  url,
  axiosInstance,
  on_start = () => {},
  on_success = () => {},
  on_error = () => {},
  verbose = true,
}) {
  if (verbose) console.log(`Fetching ${url}...`);

  try {
    on_start();
    const response = await axiosInstance.get(url);
    if (verbose) console.log(`NEW FETCHED ${url}:\n`, response.data); // Log the fetched data
    on_success(response.data);
  } catch (error) {
    if (verbose) console.error(`Error fetching ${url}:`, error); // Log any errors that occur during the fetch
    on_error(error);
  }
}

export {
  makeLinksClickable,
  // makeLinksClickableWithIcons,
  asyncsleep,
  PATH_PUBLIC,
  PATH_DB_TO_EXPORT,
  PATH_DB_EXPORTED,
  fetch_url,
};
