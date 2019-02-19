const { render, html, svg } = lighterhtml;

const button = name => html`
  <div class="clas">does this nice ${name}</div>
`;

document.body.append(button('now wwww'));
