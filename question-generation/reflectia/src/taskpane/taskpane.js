/* global document, Office, Word, console */

const SERVER_URL = "http://localhost:8000";

Office.onReady((info) => {
  if (info.host === Office.HostType.Word) {
    document.getElementById("sideload-msg").style.display = "none";
    document.getElementById("app-body").style.display = "flex";
    document.querySelector(".ms-welcome__header").style.display = "none";
    document.getElementById("run").onclick = () => tryCatch(main);
  }
});

async function post(url, data) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) throw new Error("HTTP request failed with status " + response.status);
}

export async function tryCatch(callback) {
  try {
    await callback();
  } catch (error) {
    console.error(error);
  }
}

// Function to create a new paragraph element as a child of a card
function createParagraph(card, text) {
  const paragraph = document.createElement("p");

  paragraph.textContent = text;
  card.appendChild(paragraph);
}

// Function to create a new card element
function createCard(index, text) {
  const card = document.createElement("div");

  card.id = index;
  card.className = "card";
  createParagraph(card, text);

  return card;
}

async function getReflections(paragraph, prompt) {
  const data = {
    paragraph, prompt
  };

  const req = await fetch(`${ SERVER_URL }/reflections`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const res = await req.json();
  console.log(res);

  return res.response;
}

async function getCurrentParagraph() {
  return Word.run(async (context) => {
    let selectedParagraph = context.document.getSelection().paragraphs;
    context.load(selectedParagraph);
    await context.sync();

    return selectedParagraph.items[0];
  });
}

async function detectParagraphChange() {
  let initialParagraph = await getCurrentParagraph()();

  while (true) {
    let currentParagraph = await getCurrentParagraph();
    if (initialParagraph.text != currentParagraph.text) {
      try {
        console.log("paragraph changed")
      } catch (error) {
        console.log(error);
      }

      initialParagraph = currentParagraph;
    }

    // Add a delay between checks (e.g., 1 second) to avoid excessive API calls
    await delay(1000);
  }
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function main() {
  await Word.run(async (context) => {
    // FIXME: Get the prompt from the user.
    const prompt = "3 most important concepts in very short phrases";

    const paragraphs = context.document.body.paragraphs;

    paragraphs.load();
    await context.sync();

    let cardContainer = document.getElementById("card-container");
    cardContainer.innerHTML = "";
    let cardsFragment = document.createDocumentFragment();

    for (let i = 0; i < paragraphs.items.length; i++) {
      // Get the desired reflections for this paragraph
      const reflections = await getReflections(paragraphs.items[i].text, prompt);

      const card = createCard(i, reflections);
      cardsFragment.appendChild(card);

      break;
    }

    cardContainer.appendChild(cardsFragment);
  });
}
