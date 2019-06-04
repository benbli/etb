async function getCards() {
  return await fetch(
    'https://api.magicthegathering.io/v1/cards?supertypes=legendary&set=WAR'
  )
    .then(response => response.json())
    .catch(error => console.log(error));
}

export { getCards };
