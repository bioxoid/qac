const sheetApiKey = "AIzaSyBdL0RhpII9R136Nj5rI0D3Z06oLsdFuLM";
const sheetId = "1l9SPiF7Nlavvrex5_YNlsfL9thhAxclVopLoC0PfhrE";
const sheetName = "Sheet1";
export async function loadCstl() {
  let txt = "";
  const res = await fetch(`https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values/${sheetName}?key=${sheetApiKey}`)
  const json = await res.json()
  return json
}
