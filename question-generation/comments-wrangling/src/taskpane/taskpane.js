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

async function getReplies(comment) {
  await Word.run(async (context) => {
    const replies = comment.replies;
    replies.load("items");
    await context.sync();
    return replies.items;
  });
}

async function getContext(comment) {
  await Word.run(async (context) => {
    const commentContext = comment.getRange();
    commentContext.load("text");
    await context.sync();
    return commentContext.text;
  });
}

async function main() {
  const comments = getComments();
}

export async function tryCatch(callback) {
  try {
    await callback();
  } catch (error) {
    console.error(error);
  }
}
