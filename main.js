import { getCards } from './src/services/card.js';
import { renderCards } from './src/components/cards/Card.js';
const { render } = lighterhtml;

// dom elements
const cardContainer = document.querySelector('.card-container');

getCards().then(res => render(cardContainer, () => renderCards(res)));
