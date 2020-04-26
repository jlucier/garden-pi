import React, { useState, useEffect } from 'react';
import axios from 'axios';
import * as  _ from 'lodash';
import moment from 'moment';
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

import './App.css';

function App() {
  const [currentReading, updateReading] = useState(null);
  const [historicalData, updateHistory] = useState(null);

  useEffect(() => {
    const interval = setInterval(async () => {
      const resp = await axios.get('/current');
      updateReading(_.keyBy(resp.data.data, 'type'));
    }, 5000);

    return () => {
      clearInterval(interval);
    }
  });

  useEffect(() => {
    async function fetchData() {
      const resp = await axios.get('/all');

      let data = _.groupBy(resp.data.data, 'type');
      _.forEach(data, (series, type) => {
        data[type] = _.groupBy(series, datum => moment(datum.timestamp).startOf('hour'));
        data[type] = _.map(data[type], (miniSeries, mom) => ({
          type,
          value: _.meanBy(miniSeries, 'value'),
          timestamp: moment(mom).format('LTS'),
        }));
      });

      data = _.map(_.zip(..._.values(data)), ([r1, r2]) => ({
        [r1.type]: _.round(r1.value, 2),
        [r2.type]: _.round(r2.value, 2),
        timestamp: r1.timestamp,
      }));

      updateHistory(data);
    }
    fetchData();
  }, []);

  return (
    <div className="App">
      <h1>Live</h1>
      {currentReading !== null &&
        <div>
          <h2>
            Temp: {_.round(currentReading.AIR_TEMP.value * 9/5 + 32, 2)}&#176;F
            <br/>
            Hum: {_.round(currentReading.AIR_HUMIDITY.value, 2)}%
          </h2>
          <h2>TS: {moment(currentReading.AIR_TEMP.timestamp).format('L LTS')}</h2>
        </div>
      }

      {historicalData &&
        <LineChart
          width={1600}
          height={900}
          data={historicalData}
          margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
        >
          <XAxis dataKey="timestamp" interval={0} angle={30} />
          <YAxis />
          <YAxis yAxisId="right" orientation="right" />
          <Legend />
          <Tooltip contentStyle={{backgroundColor: '#282c34'}} />
          <CartesianGrid stroke="#f5f5f5" />
          <Line type="monotone" dataKey={d => d.AIR_TEMP * 9/5 + 32} stroke="#8884d8" yAxisId={0} unit='F'/>
          <Line type="monotone" dataKey="AIR_HUMIDITY" stroke="#82ca9d" yAxisId='right' unit='%'/>
        </LineChart>
      }
    </div>
  );
}

export default App;
