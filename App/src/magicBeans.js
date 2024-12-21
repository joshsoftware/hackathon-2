import { magicBeansHelper } from "./helper.js";

(function () {
  const originalFetch = window.fetch;

  window.fetch = async function (...args) {
    try {
      const res = await originalFetch.apply(this, args);
      magicBeansHelper(args, false);
      return res;
    } catch (err) {
      magicBeansHelper(args, true);
      throw err;
    }
  };

  const originalXHR = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (method, url) {
    this.addEventListener("error", () => magicBeansHelper([url, method], true));
    this.addEventListener("load", () => {
      if (this.status === 0) {
        magicBeansHelper([url, method], true);
      } else {
        magicBeansHelper([url, method], false);
      }
    });
    originalXHR.apply(this, arguments);
  };
})();
