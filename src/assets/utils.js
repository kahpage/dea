/*
 * Some useful js definitions.
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

const _env_mode = import.meta.env.MODE;
const _is_prod = _env_mode == "production" // true if build, false if dev 

const PATH_PUBLIC = _is_prod ? `/dea` : `/dea`; // Path of public/ folder
const PATH_DB_PUBLIC = `${PATH_PUBLIC}/databases`; // Path of public/databases/ folder
const PATH_DB_SERVED = _is_prod ? `https://raw.githubusercontent.com/kahpage/dea/refs/heads/master/databases_management/databases_served` : `/dea/served`; // Path of served databases

export {makeLinksClickable, PATH_PUBLIC, PATH_DB_PUBLIC, PATH_DB_SERVED};