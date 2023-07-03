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
    const comments = context.document.body.getComments();
    comments.load("items");
    await context.sync();
    return comments.items;
  });
}

async function get

async function main() {
    // Get comments from the Word document
    // const comments = context.document.body.getComments();
    // comments.load("items");
    // await context.sync();

    // // Store them as an array
    // const commentItems = comments.items;

    // const range = commentItems[0].getRange();
    // range.load("text");
    // await context.sync();

    // console.log(range.text);
    // console.log("Comment: " + commentItems[0].content);

    // const commentItemReplies = commentItems[3].replies;
    // commentItemReplies.load("items");
    // await context.sync();

    // const commentItemReplyItems = commentItemReplies.items;

    // console.log(commentItemReplyItems);
}

export async function tryCatch(callback) {
  try {
    await callback();
  } catch (error) {
    console.error(error);
  }
}
