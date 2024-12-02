import React, {useState, useEffect} from "react"
import "./Dashboard.css"
import Clock from "./Clock.jsx"
import TimeOptions from "./TimeOptions.jsx"
import {host} from "../../../../env"

const Dashboard = () => {
    const [temperature, setTemperature] = useState(0.0);
    const [tempInput, setTempInput] = useState(0.0);
    const [fanStatus, setFanStatus] = useState(false); // note: set fan status will be based on fan reading
    const [lightStatus, setLightStatus] = useState(false);
    const [startTime, setStartTime] = useState("01:00"); //used for turning on the light
    const [endTime, setEndTime] = useState("01:00");
    const [goalTemp, setGoalTemp] = useState(80.6);

    // read data and set the temperature to be displayed (so far set to default 50.0)
    useEffect(() => {
        const fetchTemperature = async () => {
            try {
                fetch(`http://${host}:80/api/get_temperature`)
                .then((resp) => resp.json())
                .then((data) => {
                    //console.log("data:", data);
                    setTemperature(data.temperature);
                })
            } catch (e) {
                console.error("Error fetching temperature data:", e);
            }
        };
    
        fetchTemperature();
        const intervalId = setInterval(fetchTemperature, 1000); // calls fetchTemperature every 10 seconds
        return () => clearInterval(intervalId);
    }, []);

    
    useEffect(() => {
        const temperatureBarFill = document.querySelector(".temperature-bar-fill");
        if (temperatureBarFill) {
            temperatureBarFill.style.width = temperature + "%";
        }
    }, [temperature])

    useEffect(() => {
        const currentDate = new Date();
        const hours = currentDate.getHours();
        const startHours = startTime.substring(0, 2);
        const endHours = endTime.substring(0, 2);
        
        // 0-24, check time range
        if(startHours < endHours) { // if start < end, then check if hours is between range
            if(hours >= startHours && hours <= endHours) {
                setLightStatus(true);
            }
            else {
                setLightStatus(false);
            }
        }
        else if(startHours > endHours) { //if start > end
            if(hours >= startHours) { //check if hours is between start hours -> 24:00
                setLightStatus(true);
            }
            else if(hours <= startHours && hours <= endHours){  //check if hours is between 00:00 -> endHours
                setLightStatus(true);
            }
            else {
                setLightStatus(false);
            }
        }
        else {
            setLightStatus(false);
        }

        try {
            // Send POST request with goal_temp in the body
            fetch(`http://${host}:80/api/light`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ light_status: lightStatus}),  // Sending goal_temp as JSON
            })
            .then((resp) => {
                if (!resp.ok) {
                    throw new Error(`HTTP error! status: ${resp.status}`);
                }
                return resp.json();  // Get response in JSON format
            })
            .catch((e) => {
                console.error("Error updating light:", e);
            });
        } catch (e) {
            console.error("Unexpected error:", e);
        }
    })

    const processSubmit = () => {
        let temp = parseFloat(tempInput);  // Convert input to a float
        if (!isNaN(temp)) {
            // Limit the temperature range between 0 and 100, and round to two decimal places
            temp = Math.max(0, Math.min(temp, 100));
            temp = Math.round(temp * 100) / 100;
    
            console.log("Temperature set:", temp);
            setFanStatus(temp <= temperature ? true : false);
            try {
                console.log("Using host:", host);  // Log the host for debugging
    
                // Send POST request with goal_temp in the body
                fetch(`http://${host}:80/api/goal`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ goal_temp: temp }),  // Sending goal_temp as JSON
                })
                .then((resp) => {
                    if (!resp.ok) {
                        throw new Error(`HTTP error! status: ${resp.status}`);
                    }
                    return resp.json();  // Get response in JSON format
                })
                .then(setGoalTemp(temp))
                .catch((e) => {
                    console.error("Error setting temperature:", e);
                });
            } catch (e) {
                console.error("Unexpected error:", e);
            }
        } else {
            alert("Please enter a valid temperature value");
        }
    };
    
    return (
        <div>
            <div className="container"> 
                <h1>Current Temperature</h1>
                <div className="temperature-bar">
                    <div className="temperature-bar-fill"></div> 
                </div>
                <div className="scale">
                        <div>0</div><div>10</div><div>20</div><div>30</div><div>40</div>
                        <div>50</div><div>60</div><div>70</div><div>80</div><div>90</div>
                        <div>100</div>
                </div>

                <div className="input-container">
                    <input
                        name="temperature-input"
                        type="number"
                        value={tempInput}
                        onChange={(e) => setTempInput(e.target.value)
                        }
                        style={{width: "20%", marginRight: "5%"}}
                    />
                    <button onClick={processSubmit}>Set Temperature</button>
                </div>

                <div style={{marginTop: "2.5%"}}>
                        Detected Temperature: {temperature}
                </div>
                <div style={{marginTop: "2.5%"}}>
                        Goal Temperature: {goalTemp}
                </div>
                <div style={{marginTop: "2.5%"}}>
                        Fan Status: {fanStatus ? "On" : "Off"}
                </div>
            </div>
            
            <div className="container"> 
                <h1>Light Settings</h1>
                <Clock/>
                <div className="input-container">     
                    <label style={{marginRight: "5%"}}>Start Time:</label>               
                    <TimeOptions value={startTime} onChange={setStartTime} />

                </div>
                <div className="input-container">
                    <label style={{marginRight: "5%"}}> End Time:</label>
                    <TimeOptions value={endTime} onChange={setEndTime} />
                </div>

                <p1 style={{marginTop: "2.5%"}}>Light Time Range: {startTime}-{endTime}</p1>

                <div style={{marginTop: "2.5%"}}>
                        Light Status: {lightStatus ? "On" : "Off"}
                </div>
            </div>
        </div>
    );
}

export default Dashboard