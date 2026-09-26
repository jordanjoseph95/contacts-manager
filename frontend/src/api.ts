const API_URL = "http://localhost:8000";

export interface Group {
  id: number;
  name: string;
}

export interface Person {
  id: number;
  name: string;
  phone: string | null;
  email: string | null;
  group_id: number | null;
}

export async function getPeople(): Promise<Person[]> {
  const res = await fetch(`${API_URL}/people`);
  return res.json();
}

export async function getGroups(): Promise<Group[]> {
  const res = await fetch(`${API_URL}/groups`);
  return res.json();
}

export async function createPerson(person: Omit<Person, "id">): Promise<Person> {
  const res = await fetch(`${API_URL}/people`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(person),
  });
  return res.json();
}

export async function deletePerson(id: number): Promise<void> {
  await fetch(`${API_URL}/people/${id}`, { method: "DELETE" });
}