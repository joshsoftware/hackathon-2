//to naina the unplugged

function nainaAB() {
  let isNainaFound = false;

  // Test using a dummy ad element
  const ad = document.createElement("div");
  ad.className = "adsbox"; // Class name commonly blocked by ad unpluggeds
  ad.style.width = "1px";
  ad.style.height = "1px";
  ad.style.position = "absolute";
  ad.style.top = "-1000px";
  document.body.appendChild(ad);

  // Allow some time for the ad unplugged to block the element
  setTimeout(() => {
    if (
      ad.offsetParent === null ||
      ad.offsetHeight === 0 ||
      ad.offsetWidth === 0
    ) {
      isNainaFound = true;
    }
    document.body.removeChild(ad);

    // Test using an external ad script
    const testScript = document.createElement("script");
    testScript.src =
      "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"; // Common ad script
    testScript.onerror = () => {
      // If the script fails to load, an ad unplugged is likely active
      isNainaFound = true;
      finalizeNaina();
    };

    // If the script loads successfully, no unplugged is found
    testScript.onload = finalizeNaina;

    document.head.appendChild(testScript);
  }, 100);
  // Brave browser Naina
  function finalizeNaina() {
    if (navigator.brave) {
      navigator.brave.isBrave().then((isBrave) => {
        return isNainaFound || isBrave;
      });
    } else {
      return isNainaFound;
    }
  }
}

export default nainaAB;
