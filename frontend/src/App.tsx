import { useEffect, useState } from "react";
import { getPeople, getGroups, createPerson, deletePerson, type Person, type Group } from "./api";

function App() {
  const [people, setPeople] = useState<Person[]>([]);
  const [groups, setGroups] = useState<Group[]>([]);
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [groupId, setGroupId] = useState<string>("");

  async function loadData() {
    const [peopleData, groupsData] = await Promise.all([getPeople(), getGroups()]);
    setPeople(peopleData);
    setGroups(groupsData);
  }

  app = 

  useEffect(() => {
    loadData();
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    await createPerson({
      name,
      phone: phone || null,
      email: email || null,
      group_id: groupId ? parseInt(groupId) : null,
    });
    setName("");
    setPhone("");
    setEmail("");
    setGroupId("");
    loadData();
  }

  async function handleDelete(id: number) {
    await deletePerson(id);
    loadData();
  }

  return (
    <div style={{ maxWidth: 500, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>Contacts</h1>

      <form onSubmit={handleSubmit} style={{ marginBottom: "2rem" }}>
        <input
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          style={{ display: "block", marginBottom: 8, width: "100%" }}
        />
        <input
          placeholder="Phone"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          style={{ display: "block", marginBottom: 8, width: "100%" }}
        />
        <input
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ display: "block", marginBottom: 8, width: "100%" }}
        />
        <select
          value={groupId}
          onChange={(e) => setGroupId(e.target.value)}
          style={{ display: "block", marginBottom: 8, width: "100%" }}
        >
          <option value="">No group</option>
          {groups.map((g) => (
            <option key={g.id} value={g.id}>
              {g.name}
            </option>
          ))}
        </select>
        <button type="submit">Add contact</button>
      </form>

      <ul style={{ listStyle: "none", padding: 0 }}>
        {people.map((person) => (
          <li key={person.id} style={{ marginBottom: 8, borderBottom: "1px solid #333", paddingBottom: 8 }}>
            <strong>{person.name}</strong>
            {person.phone && <span> · {person.phone}</span>}
            {person.email && <span> · {person.email}</span>}
            <button onClick={() => handleDelete(person.id)} style={{ marginLeft: 8 }}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;