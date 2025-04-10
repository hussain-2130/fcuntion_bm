console.log("Taskpane JS loaded!");

Office.onReady(() => {
  console.log("Office Add-in Ready ✅");

  const runButton = document.getElementById("run");
  if (runButton) {
    runButton.addEventListener("click", () => {
      const startIndex = parseInt(document.getElementById("startIndex").value, 10);
      const offset = parseInt(document.getElementById("offset").value, 10);
      highlightTextByIndex(startIndex, offset);
    });
  } else {
    console.log("❌ Run button not found!");
  }
});

function safeNotify(message) {
  console.log("Notify:", message);
  const output = document.getElementById("debugOutput");
  if (output) output.innerText = message;
}

async function highlightTextByIndex(startIndex, offset, color = "#FFFF00") {
  await Word.run(async (context) => {
    const body = context.document.body;
    body.load("text");
    await context.sync();

    const fullText = body.text;
    const endIndex = startIndex + offset;

    if (startIndex < 0 || offset <= 0 || endIndex > fullText.length) {
      safeNotify("❌ Invalid start index or offset.");
      return;
    }

    const selectedText = fullText.substring(startIndex, endIndex);

    // Step 1: Search all instances of selected text
    const ranges = body.search(selectedText, {
      matchCase: true,
      matchWholeWord: false,
      ignorePunct: false,
    });
    context.load(ranges, "items");
    await context.sync();

    // Step 2: Find the correct one by matching character position
    let matchedRange = null;
    let charCount = 0;

    for (const range of ranges.items) {
      range.load("text");
    }
    await context.sync();

    for (const range of ranges.items) {
      const index = fullText.indexOf(range.text, charCount);
      if (index === startIndex) {
        matchedRange = range;
        break;
      }
      charCount = index + 1;
    }

    if (!matchedRange) {
      safeNotify("❌ Could not match text at specified index.");
      return;
    }

    matchedRange.font.highlightColor = color;
    matchedRange.font.bold = true;
    await context.sync();

    safeNotify(`✅ Highlighted exact text: "${selectedText}"`);
  }).catch((error) => {
    console.error("❌ Word.run error:", error);
    safeNotify("❌ Error: " + error.message);
  });
}
