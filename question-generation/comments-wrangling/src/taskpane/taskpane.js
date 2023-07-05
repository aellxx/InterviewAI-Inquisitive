/* global document, Office, Word, console */

Office.onReady((info) => {
  if (info.host === Office.HostType.Word) {
    document.getElementById("sideload-msg").style.display = "none";
    document.getElementById("app-body").style.display = "flex";
    document.getElementById("run").onclick = () => tryCatch(main);
  }
});

async function getCommentContexts(commentCollection) {
  const commentArray = commentCollection.items;
  const commentRanges = commentArray.map((comment) => comment.getRange().load("text"));
  await commentCollection.context.sync();
  return commentRanges.map((range) => range.text);
}

async function getCommentReplies(commentCollection) {
  const commentArray = commentCollection.items;
  const replyCollections = commentArray.map((comment) => comment.replies.load("items"));
  await commentCollection.context.sync();
  return replyCollections.map((reply) => reply.items.map((item) => item.content));
}

async function main() {
  await Word.run(async (context) => {
    const commentCollection = context.document.body.getComments();
    commentCollection.load("items");
    await context.sync();

    const contexts = await getCommentContexts(commentCollection);
    const replies = await getCommentReplies(commentCollection);

    console.log(contexts);
  });
}

export async function tryCatch(callback) {
  try {
    await callback();
  } catch (error) {
    console.error(error);
  }
}
