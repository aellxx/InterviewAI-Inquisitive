/* global document, Office, Word, console */

const SERVER_URL = "http://localhost:8000";

let presetPrompts = [
  {
    name: "Summary: phrases",
    prompt: "What are 3 of the most important concepts described by this paragraph? Respond as a bulleted list of 2 or 3 words."
  },
  {
    name: "Summary: sentences",
    prompt: "What are 3 of the most important concepts described by this paragraph? Respond as a bulleted list of 2 or 3 sentences."
  },
  {
    name: "Summary: questions",
    // TODO: Improve this prompt
    prompt: "List 2 or 3 questions that the writer was attempting to answer in this paragraph."
  },
  {
    name: "Reactions: questions",
    prompt: "As a reader, ask the writer 2 or 3 questions about definitions, logical connections, or some needed background information."
  }
]

Office.onReady((info) => {
  if (info.host === Office.HostType.Word) {
    document.getElementById("sideload-msg").style.display = "none";
    document.getElementById("app-body").style.display = "flex";
    document.querySelector(".ms-welcome__header").style.display = "none";
    document.getElementById("run").onclick = () => tryCatch(main);
    // make a radio button for each preset prompt
    let presetPromptsContainer = document.getElementById("preset-prompts");
    presetPrompts.forEach((presetPrompt) => {
      let radio = document.createElement("input");
      radio.type = "radio";
      radio.name = "prompt";
      radio.value = presetPrompt.prompt;
      radio.id = presetPrompt.name;
      radio.onclick = () => {
        document.getElementById("prompt").value = presetPrompt.prompt;
      }
      let label = document.createElement("label");
      label.style.display = "block";
      label.textContent = presetPrompt.name;
      label.insertBefore(radio, label.firstChild);
      presetPromptsContainer.appendChild(label);
    }
  )
    
  }
});

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
function createCard(text) {
  const card = document.createElement("div");

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

async function getCurrentParagraph(context) {
  let selectedParagraphs = context.document.getSelection().paragraphs;
  context.load(selectedParagraphs);
  await context.sync();

  // A selection can span multiple paragraphs, but we only want the first one
  return selectedParagraphs.items[0];
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
    let prompt = document.getElementById('prompt').value;

    if(prompt.length === 0)
      prompt = "Using only the text from the user, what are 3 of the most important concepts in this paragraph?";

    // FIXME: Get the prompt from the user.

    const paragraphs = context.document.body.paragraphs;

    paragraphs.load();
    await context.sync();

    let cardContainer = document.getElementById("card-container");
    cardContainer.innerHTML = "Loading...";
    let cardsFragment = document.createDocumentFragment();

    // Get the desired reflections for the current paragraph
    const currentParagraph = await getCurrentParagraph(context);
    const reflections = await getReflections(currentParagraph.text, prompt);
    cardContainer.innerHTML = "";

    const card = createCard(reflections);
    cardsFragment.appendChild(card);

    cardContainer.appendChild(cardsFragment);
    
  });
}
