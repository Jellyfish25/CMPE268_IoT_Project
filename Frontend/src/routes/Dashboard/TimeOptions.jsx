import React, { useState } from 'react';

function TimeOptions({value, onChange}) {
    const times = [];
    const date = new Date();
    date.setHours(0, 0, 0, 0);

    for (let i = 0; i < 24; i++) {
        const timeString = date.toTimeString().slice(0, 5);
        times.push(timeString);
        date.setHours(date.getHours() + 1); // Increment by one hour
    }

    return(
        <select
            value={value} onChange={(e) => onChange(e.target.value)}>
            {times.map((time) => (
                <option key = {time} value={time}>{time}</option>
            ))}
        </select>
    );
}
export default  TimeOptions;