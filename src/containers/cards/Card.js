const { html } = lighterhtml;

const renderCards = data => html`
  ${data.cards.map(
    card => html`
      <div class="card-wrapper flex row-wrap">
        <img src=${card.imageUrl} alt=${card.name} />
        <div class="card-description">
          <p>${card.name} ${card.manaCost}</p>
          <span>${card.type}</span>
          <span>${card.rarity}</span>
          <p>${card.text}</p>
        </div>
      </div>
    `
  )}
`;

export { renderCards };
