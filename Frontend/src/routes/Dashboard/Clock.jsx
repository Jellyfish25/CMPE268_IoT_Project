import React, { useState, useEffect } from 'react';

const Clock = () => {
    const[time, setTime] = useState(new Date());
    
    useEffect(() => {
        const updateTime = () => {
            setTime(new Date());
        }
        const intervalId = setInterval(updateTime, 1000); //update the clock every second
        return () => clearInterval(intervalId);
    });

    return(
        <div>
            {time.toLocaleTimeString()}
        </div>
    );
}
export default Clock;