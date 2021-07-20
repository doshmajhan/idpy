
export async function fetchApi(endpoint: string): Promise<string> {
  const res: Response = await fetch(endpoint);
  const json: string = await res.json();

  if (res.ok) {
    return json;
  } else {
    throw new Error(json);
  }
}