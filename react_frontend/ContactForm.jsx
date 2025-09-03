import { useState } from 'react';

const ContactForm = () => {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');

    const onSubmit = async (e) => {
        e.preventDefault();

        const data = { firstName, lastName, email };
        const url = "http://127.0.0.1:5000/contacts"; // Make sure this matches your Flask route

        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        };

        try {
            const response = await fetch(url, options);
            const result = await response.json();

            if (response.status !== 201 && response.status !== 200) {
                alert(result.message || "Something went wrong.");
            } else {
                console.log(result);
                alert("Contact created successfully!");
            }
        } catch (err) {
            console.error("Error:", err);
            alert("An error occurred.");
        }
    };

    return (
        <form onSubmit={onSubmit}>
            <div>
                <label htmlFor="firstName">First Name</label>
                <input
                    type="text"
                    id="firstName"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                />
            </div>

            <div>
                <label htmlFor="lastName">Last Name</label>
                <input
                    type="text"
                    id="lastName" // ✅ FIXED typo from "lastsName"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                />
            </div>

            <div>
                <label htmlFor="email">Email</label>
                <input
                    type="email" // better validation than text
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
            </div>

            <button type="submit">Create Contact</button> {/* ✅ FIXED syntax */}
        </form>
    );
};

export default ContactForm;
