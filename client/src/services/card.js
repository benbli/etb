async function getCards() {
  return await fetch('https://api.magicthegathering.io/v1/cards?set=m20')
    .then(response => response.json())
    .catch(error => console.log(error));
}

export { getCards };
