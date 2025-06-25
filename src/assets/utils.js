/*
 * Some useful js definitions.
 */

function makeLinksClickable(text) {
  const urlRegex = /(https?:\/\/[^\s]+)/g;
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

export default makeLinksClickable;