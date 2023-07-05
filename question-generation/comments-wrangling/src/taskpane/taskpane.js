/* global document, Office, Word, console */

Office.onReady((info) => {
  if (info.host === Office.HostType.Word) {
    document.getElementById("sideload-msg").style.display = "none";
    document.getElementById("app-body").style.display = "flex";
    document.getElementById("run").onclick = () => tryCatch(main);
  }
});

async function getCommentContexts(context, commentCollection) {
  const commentArray = commentCollection.items;
  let commentRanges = [];
  let contexts = [];

  for (let i = 0; i < commentArray.length; i++) {
    commentRanges.push(commentArray[i].getRange());
    commentRanges[i].load("text");
  }

  await context.sync();

  for (let i = 0; i < commentRanges.length; i++) {
    contexts.push(commentRanges[i].text);
  }

  return contexts;
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

    const replies = await getCommentReplies(commentCollection);

    console.log(replies);
  });
}

export async function tryCatch(callback) {
  try {
    await callback();
  } catch (error) {
    console.error(error);
  }
}
