import { useState } from 'react';
import './App.css'
function App() {
   const [contacts, setContacts] = useState([]);

   useEffect (() => {
       fetchContacts();
   }, [])
   const fetchContacts = async () => {
       const response = await fetch('https://jsonplaceholder.typicode.com/users');
       const data = await response.json();
       setContacts(data.contacts);
       console.log(data.contacts)
   }
    return <><ContactList contacts={contacts}/>
<ContactForm />
        </>
}

export default App;
