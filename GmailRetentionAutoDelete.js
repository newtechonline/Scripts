/*
Script to autodelete old emails on Gmail
*/

function deleteOldEmails() {
  const LABEL_NAME = 'LABED/NESTED'; // change to filtered label
  const RETENTION_DAYS = 30; // change to desired retention

  const label = GmailApp.getUserLabelByName(LABEL_NAME);

  if (!label) {
    throw new Error('Gmail label not found: ' + LABEL_NAME);
  }

  const cutoffTime = Date.now() - (RETENTION_DAYS * 24 * 60 * 60 * 1000);

  // Search only messages with the dedicated label.
  // Pagination prevents processing an unnecessarily large result set.
  const threads = GmailApp.search('label:"' + LABEL_NAME + '"', 0, 100);

  let deletedMessages = 0;

  for (const thread of threads) {
    const messages = thread.getMessages();

    for (const message of messages) {
      if (message.getDate().getTime() < cutoffTime) {
        message.moveToTrash();
        deletedMessages++;
      }
    }
  }

  console.log('Moved to Trash: ' + deletedMessages + ' messages');
}
