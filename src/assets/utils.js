/*
 * Some useful js definitions.
 */

const _env_mode = import.meta.env.MODE;
const _is_prod = _env_mode == "production" // true if build, false if dev 

const PATH_PUBLIC = _is_prod ? `/dea` : `/dea`; // Path of public/ folder
const PATH_DB_PUBLIC = `${PATH_PUBLIC}/databases`; // Path of public/databases/ folder
const PATH_DB_SERVED = _is_prod ? `https://raw.githubusercontent.com/kahpage/dea/refs/heads/master/databases_management/databases_served` : `/dea/served`; // Path of served databases

/* 
 * Make URLs in text clickable (raw html output)
 */
function makeLinksClickable(text) {
  const urlRegex = /(https?:\/\/[^\s,]+)/g;
  return text.replace(urlRegex, function (url) {
    return (
      '<a class="embedded-link" href="' +
      url +
      '" target="_blank">' +
      url +
      "</a>"
    );
  });
}

/* 
 * Sleep for given duration in async contexts. This should be awaited.
 */
async function asyncsleep(duration_ms) {
  await new Promise((resolve) => setTimeout(resolve, duration_ms));
}

export {makeLinksClickable, asyncsleep, PATH_PUBLIC, PATH_DB_PUBLIC, PATH_DB_SERVED};