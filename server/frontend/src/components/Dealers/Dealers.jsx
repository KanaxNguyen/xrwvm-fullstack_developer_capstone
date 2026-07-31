import React, { useState, useEffect } from 'react';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';
import review_icon from "../assets/reviewicon.png"
import { useNavigate, useParams } from "react-router-dom";

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [states, setStates] = useState([]);
  const navigate = useNavigate();
  const { state: selectedState } = useParams();

  const filterDealers = async (state) => {
    const endpoint = state === "All"
      ? "/djangoapp/get_dealers"
      : `/djangoapp/get_dealers/${encodeURIComponent(state)}`;
    const res = await fetch(endpoint, {
      method: "GET"
    });
    const retobj = await res.json();
    if (retobj.status === 200) {
      setDealersList(Array.from(retobj.dealers));
      navigate(state === "All" ? "/dealers" : `/dealers/${encodeURIComponent(state)}`);
    }
  };

  const getDealers = async () => {
    const res = await fetch("/djangoapp/get_dealers", {
      method: "GET"
    });
    const retobj = await res.json();
    if (retobj.status === 200) {
      const allDealers = Array.from(retobj.dealers);
      setStates(Array.from(new Set(allDealers.map((dealer) => dealer.state))));
      if (selectedState) {
        const stateResponse = await fetch(
          `/djangoapp/get_dealers/${encodeURIComponent(selectedState)}`
        );
        const stateResult = await stateResponse.json();
        setDealersList(Array.from(stateResult.dealers || []));
      } else {
        setDealersList(allDealers);
      }
    }
  };

  useEffect(() => {
    getDealers();
  }, [selectedState]);


let isLoggedIn = sessionStorage.getItem("username") != null ? true : false;
return(
  <div>
      <Header/>

     <table className='table'>
      <thead>
      <tr>
      <th>ID</th>
      <th>Dealer Name</th>
      <th>City</th>
      <th>Address</th>
      <th>Zip</th>
      <th>
      <select name="state" id="state" value={selectedState || ""} onChange={(e) => filterDealers(e.target.value)}>
      <option value="" disabled>State</option>
      <option value="All">All States</option>
      {states.map(state => (
          <option key={state} value={state}>{state}</option>
      ))}
      </select>        

      </th>
      {isLoggedIn ? (
          <th>Review Dealer</th>
         ):<></>
      }
      </tr>
      </thead>
      <tbody>
     {dealersList.map(dealer => (
        <tr key={dealer.id}>
          <td>{dealer['id']}</td>
          <td><a href={'/dealer/'+dealer['id']}>{dealer['full_name']}</a></td>
          <td>{dealer['city']}</td>
          <td>{dealer['address']}</td>
          <td>{dealer['zip']}</td>
          <td>{dealer['state']}</td>
          {isLoggedIn ? (
            <td><a href={`/postreview/${dealer['id']}`}><img src={review_icon} className="review_icon" alt="Post Review"/></a></td>
           ):<></>
          }
        </tr>
      ))}
      </tbody>
     </table>
  </div>
)
}

export default Dealers
