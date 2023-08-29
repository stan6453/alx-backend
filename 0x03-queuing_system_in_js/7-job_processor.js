import kue from 'kue';

const queue = kue.createQueue();

const blacklistedPhoneNumbers = ['4153518780', '4153518781'];

queue.process('push_notification_code_2', 2, function (job, done) {
  sendNotification(job.data.phoneNumber, job.data.message, job, done);
});

function sendNotification(phoneNumber, message, job, done) {
  job.progress(0, 100);

  if (blacklistedPhoneNumbers.includes(phoneNumber)) {
    job.failed().error(new Error(`Phone number ${phoneNumber} is blacklisted`));
    return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  }

  job.progress(50, 100);
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);

  done();
}
