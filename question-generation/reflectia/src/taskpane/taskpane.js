/* global document, Office, Word, console */

Office.onReady((info) => {
  if (info.host === Office.HostType.Word) {
    document.getElementById('sideload-msg').style.display = 'none';
    document.getElementById('app-body').style.display = 'flex';
    document.querySelector('.ms-welcome__header').style.display = 'none';
    document.getElementById('run').onclick = () => tryCatch(main);
  }
});

async function post(url, data) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok)
    throw new Error('HTTP request failed with status ' + response.status);
}

export async function tryCatch(callback) {
  try {
    await callback();
  }
  catch (error) {
    console.error(error);
  }
}

// Function to create a new paragraph element as a child of a card
function createParagraph(card, text) {
  const paragraph = document.createElement('p');
  
  paragraph.textContent = text;
  card.appendChild(paragraph);
}

// Function to create a new card element
function createCard(index, text) {
  const card = document.createElement('div');

  card.id = index;
  card.className = 'card';
  createParagraph(card, text);

  return card;
}

async function main() {
  await Word.run(async (context) => {
    const paragraphs = context.document.body.paragraphs;

    paragraphs.load();
    await context.sync();

    let cardContainer = document.getElementById('card-container');
    cardContainer.innerHTML = '';
    let cardsFragment = document.createDocumentFragment();

    for (let i = 0; i < paragraphs.items.length; i++) {
      const card = createCard(i, paragraphs.items[i].text);
      cardsFragment.appendChild(card);
    }

    cardContainer.appendChild(cardsFragment);
  });
}
