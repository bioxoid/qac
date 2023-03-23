import { supabase } from "./supabaseClient"

export async function startQA(json: JSON) {
  const json_text = JSON.stringify(json);
  const res = await fetch('https://qca-api.onrender.com/', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    },
    body: json_text
  });
  const content = await res.json();
  return content
};

export async function loadCstl() {
  let { data: Zodiac } = await supabase.from('Zodiac').select('*')

  return Zodiac
};

export async function saveCstl(star_name: string, stars_connection: JSON, image: string, coord: JSON, size: JSON) {
  const { data, error } = await supabase
    .from('Zodiac')
    .insert([
      { name: star_name, image: image, image_coord: coord, image_size: size, connected_stars: stars_connection },
  ])
  return {data, error}
};
