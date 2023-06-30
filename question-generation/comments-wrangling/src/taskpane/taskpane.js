/* global document, Office, Word, console */

Office.onReady((info) => {
  if (info.host === Office.HostType.Word) {
    document.getElementById("sideload-msg").style.display = "none";
    document.getElementById("app-body").style.display = "flex";
    document.getElementById("run").onclick = () => tryCatch(getComments);
  }
});

async function getComments() {
  await Word.run(async (context) => {
    // Get comments from the Word document
    const comments = context.document.body.getComments();
    comments.load("items");
    await context.sync();

    // Store them as an array
    const commentItems = comments.items;

    console.log(commentItems[0]);
  });
}

export async function tryCatch(callback) {
  try {
    await callback();
  } catch (error) {
    console.error(error);
  }
}
