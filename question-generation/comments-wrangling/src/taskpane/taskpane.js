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

async function post(url, data) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("HTTP request failed with status " + response.status);
  }
}

export async function tryCatch(callback) {
  try {
    await callback();
  } catch (error) {
    console.error(error);
  }
}

async function main() {
  await Word.run(async (context) => {
    const commentCollection = context.document.body.getComments();
    commentCollection.load("items");
    await context.sync();

    const contexts = await getCommentContexts(commentCollection);
    const replies = await getCommentReplies(commentCollection);

    const data = [];

    for (let i = 0; i < commentCollection.items.length; i++) {
      const comments = [commentCollection.items[i].content];
      if (replies[i].length > 0) {
        comments.push(...replies[i]);
      }
      data.push({ context: contexts[i], comments: comments });
    }

    const url = "https://dev0.kenarnold.org/data";
    post(url, data);
  });
}
