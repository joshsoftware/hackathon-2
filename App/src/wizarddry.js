// this file is used to read error logs
import { wizarddryHelper } from "./helper.js";

/**
 * @param {Object} message, source, lineno, colno
 * @returns {void}
 * @description will intercept the error logs here
 */
window.onerror = function (message = "", source) {
  if (message.includes("Uncaught")) {
    wizarddryHelper({ message, source });
  }
};
