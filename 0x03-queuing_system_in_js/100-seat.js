import { createClient } from "redis";
import kue from 'kue';
import express from "express";
import { promisify } from 'util'

const app = express();
const port = 1245;
const queue = kue.createQueue();
const client = createClient();
const getAsync = promisify(client.get).bind(client);

reserveSeat(50);
let reservationEnabled = true;

function reserveSeat(number) {
  client.set('available_seats', number);
}

async function getCurrentAvailableSeats() {
  return Number(await getAsync('available_seats'));
}

app.get('/available_seats', async (req, res) => {
  res.json({ "numberOfAvailableSeats": await getCurrentAvailableSeats() })
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) return res.json({ "status": "Reservation are blocked" });

  const job = queue.create('reserve_seat', { 'count': 1 })

  job.on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  })
    .on('complete', () => {
      console.log(`Seat reservation job ${job.id} completed`);
    });

  job.save((err) => {
    if (err) return res.json({ "status": "Reservation failed" });
    return res.json({ "status": "Reservation in process" });
  });
});

app.get('/process', async (req, res) => {
  queue.process('reserve_seat', handleReserveSeat);
  queue.removeListener('reserve_seat', handleReserveSeat);

  res.json({ "status": "Queue processing" });
});

app.listen(port)


// Utility functions 
async function handleReserveSeat(job, done) {
  const availableSeats = (await getCurrentAvailableSeats()) - 1;
  reserveSeat(availableSeats)
  if (availableSeats === 0) {
    reservationEnabled = false;
  } else if (availableSeats < 0) {
    job.failed().error(new Error('Not enough seats available'));
    return done(new Error('Not enough seats available'));
  }
  done();
}
