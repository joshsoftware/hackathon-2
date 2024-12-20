//to detect the blocker

function detectAB() {
  let abDetected = false;

  // Test using a dummy ad element
  const ad = document.createElement("div");
  ad.className = "adsbox"; // Class name commonly blocked by ad blockers
  ad.style.width = "1px";
  ad.style.height = "1px";
  ad.style.position = "absolute";
  ad.style.top = "-1000px";
  document.body.appendChild(ad);

  // Allow some time for the ad blocker to block the element
  setTimeout(() => {
    if (
      ad.offsetParent === null ||
      ad.offsetHeight === 0 ||
      ad.offsetWidth === 0
    ) {
      abDetected = true;
    }
    document.body.removeChild(ad);

    // Test using an external ad script
    const testScript = document.createElement("script");
    testScript.src =
      "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"; // Common ad script
    testScript.onerror = () => {
      // If the script fails to load, an ad blocker is likely active
      abDetected = true;
      finalizeDetection();
    };

    // If the script loads successfully, no ad blocker is detected
    testScript.onload = finalizeDetection;

    document.head.appendChild(testScript);
  }, 100);
  // Brave browser detection
  function finalizeDetection() {
    if (navigator.brave) {
      navigator.brave.isBrave().then((isBrave) => {
        return abDetected || isBrave;
      });
    } else {
      return abDetected;
    }
  }
}

export default detectAB;
