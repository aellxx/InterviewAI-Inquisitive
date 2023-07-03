/* global document, Office, Word, console */

Office.onReady((info) => {
  if (info.host === Office.HostType.Word) {
    document.getElementById("sideload-msg").style.display = "none";
    document.getElementById("app-body").style.display = "flex";
    document.getElementById("run").onclick = () => tryCatch(main);
  }
});

async function main() {
  await Word.run(async (context) => {
    const comments = [];

    const commentCollection = context.document.body.getComments();
    commentCollection.load("items");
    await context.sync();

    for (let i = 0; i < commentCollection.items.length; i++) {
      let comment = Array(commentCollection.items[i].content);

      const commentReplyCollection = commentCollection.items[i].replies;
      commentReplyCollection.load("items");
      await context.sync();

      for (let j = 0; j < commentReplyCollection.items.length; j++) {
        comment.push(commentReplyCollection.items[j].content);
      }

      const commentRange = commentCollection.items[i].getRange();
      commentRange.load("text");
      await context.sync();

      comments.push({
        context: commentRange.text,
        comments: comment,
      });
    }

    console.log(comments);
  });
}

export async function tryCatch(callback) {
  try {
    await callback();
  } catch (error) {
    console.error(error);
  }
}
