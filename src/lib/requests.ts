import axios from "axios";

export async function startQA(json: JSON) {
  const json_text = JSON.stringify(json);
  const res = await fetch('http://localhost:8000/', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: json_text
  });
  const content = await res.json();
  return content
};

export async function loadCstl() {
  const sheetApiKey = "AIzaSyBdL0RhpII9R136Nj5rI0D3Z06oLsdFuLM";
  const sheetId = "1l9SPiF7Nlavvrex5_YNlsfL9thhAxclVopLoC0PfhrE";
  const sheetName = "Sheet1";
  const res = await fetch(`https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values/${sheetName}?key=${sheetApiKey}`)
  const json = await res.json()
  return json
};

export async function saveCstl(name: any, myth: any, stars_connection: any, image: any, coord: any, size: any) {
  const params = `name=${name}&myth=${myth}&stars_connection=${stars_connection}&image_coord=${coord}&image_size=${size}`
  fetch(`https://script.google.com/macros/s/AKfycbzGKiSRQbwGocfmZyvN3yzK5nblyaIUx_YjahAD67EqDSit5ErLqgvacRgEl2Nkg5XH/exec?${params}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded',
      "Access-Control-Allow-Origin": "*",
    },
    mode: 'no-cors',
  });
  // console.log(`https://script.google.com/macros/s/AKfycbzGKiSRQbwGocfmZyvN3yzK5nblyaIUx_YjahAD67EqDSit5ErLqgvacRgEl2Nkg5XH/exec?${params}`)
  // const content = res.json();
  // return content
};
