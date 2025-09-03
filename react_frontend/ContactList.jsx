import React, { useEffect, useState } from "react";
import ContactList from "./ContactList"; // adjust the path as needed

const App = () => {
    const [contacts, setContacts] = useState([]);

    useEffect(() => {
        fetch("http://localhost:5000/contacts") // adjust if hosted differently
            .then((res) => res.json())
            .then((data) => {
                setContacts(data.contacts); // from Flask's JSON structure
            })
            .catch((err) => {
                console.error("Failed to load contacts:", err);
            });
    }, []);

    return (
        <div>
            <h1>My Contact Manager</h1>
            <ContactList contacts={contacts} />
        </div>
    );
};

export default App;
