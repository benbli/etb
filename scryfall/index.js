const download = require('image-downloader').image;
const json = require('./data.json');

function downloadImage(url, dest) {
  return download({ url, dest });
}

function main() {
  const artists = {};
  const uniques = json.reduce((acc, card) => {
    const { name, artist, image_uris } = card;

    if (!artists[artist]) {
      artists[artist] = {};
      artists[artist][name] = image_uris ? image_uris.art_crop : '';
      if (artists[artist][name] !== '') {
        downloadImage(artists[artist][name], './art_crop/')
          .then(({ filename }) => {
            console.log('saved to', filename);
          })
          .catch((err) => console.error(err));
      }
    } else {
      if (!artists[artist][name]) {
        artists[artist][name] = image_uris ? image_uris.art_crop : '';
        if (artists[artist][name] !== '') {
          downloadImage(artists[artist][name], './art_crop/')
            .then(({ filename }) => {
              console.log('saved to', filename);
            })
            .catch((err) => console.error(err));
        }
      }
    }

    return acc;
  }, artists);

  console.log('uniques', uniques);
}

main();
