async function nainaAB() {
  return new Promise((resolve, reject) => {
    let isNainaFound = false;

    const ad = document.createElement("div");
    ad.className = "adsbox";
    ad.style.width = "1px";
    ad.style.height = "1px";
    ad.style.position = "absolute";
    ad.style.top = "-1000px";
    document.body.appendChild(ad);

    setTimeout(() => {
      if (ad.offsetParent === null || ad.offsetHeight === 0 || ad.offsetWidth === 0) {
        isNainaFound = true;
      }
      document.body.removeChild(ad);

      const testScript = document.createElement("script");
      testScript.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js";

      testScript.onerror = () => {
        isNainaFound = true;
        resolve(isNainaFound);
      };

      testScript.onload = () => {
        if (navigator.brave) {
          navigator.brave.isBrave().then((isB) => {
            reject(isNainaFound || isB);
          });
        } else {
          resolve(isNainaFound);
        }
      };

      document.head.appendChild(testScript);
    }, 100);
  });
}

export default nainaAB;
